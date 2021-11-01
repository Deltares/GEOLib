from __future__ import annotations

import inspect
import logging
import re
import shlex
from abc import abstractclassmethod, abstractmethod
from itertools import groupby
from math import isfinite
from typing import (
    Dict,
    Iterable,
    List,
    Tuple,
    Type,
    Union,
    _GenericAlias,
    _SpecialForm,
    get_type_hints,
)

from pydantic import FilePath

from geolib.errors import ParserError
from geolib.models import BaseDataClass as DataClass
from geolib.models.base_model_structure import BaseModelStructure

from .parsers import BaseParser
from .utils import (
    get_args,
    get_filtered_type_hints,
    get_required_class_field,
    is_list,
    is_union,
    unpack_if_union,
)

logger = logging.getLogger(__name__)


class DSeriesStructure(BaseModelStructure):
    def __init__(self, *args, **kwargs):
        """The base class for all DSerie structures.

        It's parent is a BaseModel from Pydantic, which expects
        all its fields named as kwargs.

        Here we check, using the type annotations stored for each
        field, whether we can parse/convert a field, passed as string,
        to a more concrete implementation.

        When we have a class:
        ```
        Test(DSeriesStructure):
            field_a: Union[OtherClass, str]
        ```
        and we receive field_a as a `str`, we check the attributes
        of `OtherClass` to see if it (also) has a `is_parseable` method.
        If so, we convert it from `str` to `OtherClass` using its
        `parse_text` method.

        If `OtherClass` is a child of `DSeriesStructure`, this process
        is recursive.

        Note that the heuristics of checking type hints such as
        `Optional` and `List` or `Union` are still archaic.
        In later versions of Python this is improved.
        """
        # Remove fields that are None so defaults will be used
        kwargs = {field: value for field, value in kwargs.items() if value is not None}

        if len(kwargs) > len(get_type_hints(self)):
            a = set(kwargs.keys())
            b = set(get_type_hints(self).keys())
            raise ValueError(
                f"""Got more fields than defined on model {self.__class__.__name__}:
                parser has {a.difference(b)} fields and
                model has {b.difference(a)} fields not set.
                """
            )

        for field, fieldtype in get_type_hints(self).items():

            # If the body is a string, we should check
            # whether we can parse it further.
            if field in kwargs and isinstance(kwargs[field], str):
                body = kwargs[field]

                # Optional, Union, etc.
                if is_union(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                if is_list(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                    logger.debug(f"Changed {field} to {fieldtype}")
                    kwargs[field] = fieldtype.parse_text(body)
                else:
                    if DataClass in fieldtype.__mro__:
                        logger.debug(f"Can't parse {fieldtype} for {field} yet")

            # If the body is a List[string], we should check
            # whether we can parse it further.
            elif (
                field in kwargs
                and isinstance(kwargs[field], list)
                and len(kwargs[field]) > 0
                and isinstance(kwargs[field][0], str)
            ):
                body = kwargs[field]

                # We need to decompose a possible Union
                if is_union(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                # And then the list
                if is_list(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                    # Check whether we can parse and if so, parse the strings
                    if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                        logger.debug(f"Changed {field} to multiple {fieldtype}")
                        kwargs[field] = [fieldtype.parse_text(item) for item in body]
                    else:
                        if DataClass in fieldtype.__mro__:
                            logger.debug(f"Can't parse {fieldtype} for {field} yet")

                else:
                    # Check whether we can parse and if so, parse the strings
                    if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                        logger.debug(
                            f"Changed {field} to single {fieldtype} for list of str."
                        )
                        kwargs[field] = fieldtype.parse_text(body)
                    else:
                        if DataClass in fieldtype.__mro__:
                            logger.debug(f"Can't parse {fieldtype} for {field} yet")

            else:
                # Ignore other fields
                continue

        super().__init__(**kwargs)

    @staticmethod
    def is_parseable() -> bool:
        return True

    @classmethod
    def parse_text(cls, data: str) -> DSeriesStructure:
        """Creates a DSeriesStructure using the concrete parser.

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_group_as_dict(data)
        return cls(**parsed_structure)

    @classmethod
    def get_structure_required_fields(cls) -> List[Tuple[str, Type]]:
        """Allows concrete classes to filter out fields that would normally be
        parsed.

        Returns:
            List[Tuple[str, Type]]: List of Tuples[FieldName, FieldType]
        """
        return get_filtered_type_hints(cls)

    def dict(_, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        for __, value in data.items():
            if isinstance(value, float) and not isfinite(value):
                raise ValueError(
                    "Only finite values are supported, don't use nan, -inf or inf."
                )
        return data


class DSerieListGroupNextStructure(DSeriesStructure):
    """Creates a DSeriesStructure that can parse fields like this:

    [NUMBER OF STRUCTURES]
    2
    -------
    [STRUCTURE VALUE]
    42
    [END STRUCTURE VALUE]
    [NEXT NUMBER OF STRUCTURES]
    [STRUCTURE VALUE]
    24
    [END STRUCTURE VALUE]
    [END NUMBER OF STRUCTURES]

    into:

    wrapper = [
        "2\n-------\n[STRUCTURE VALUE...",
        "[STRUCTURE VALUE...",
    ]

    Note the "NEXT NUMBER OF STRUCTURES" element that makes this different
    from a normal ListGroup structure. The extra strings at the beginning
    of the first element should be ignored by the child parser.
    """

    @abstractclassmethod
    def group_delimiter() -> str:
        raise NotImplementedError("Implement in derived classes.")

    @classmethod
    def parse_text(cls, text: str):
        # Strip outer wrapper
        body = list(DSerieParser.parse_group(text))[0][1]

        num_elements = int(body.strip().split("\n")[0])
        elements = body.split(cls.group_delimiter())
        # Check whether we find the number of elements
        # as stated in the header.
        if num_elements == 0:
            # Even if there are zero elements, the split() method will still return a list of length 1
            # "a".split("b") -> ["a"]
            if not len(elements) - 1 == num_elements:
                raise ParserError(f"Error in parsing in number of elements for {cls}")
            elements = []
        else:
            if not len(elements) == num_elements:
                raise ParserError(f"Error in parsing in number of elements for {cls}")

        collection_property_name = list(cls.__fields__.items())[0][0]
        return cls(**{collection_property_name: elements})


class DSeriesTableStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure that can parse fields like

        [GROUP]
        [COLUMN INDICATION]
        A
        B
        C
        [END OF COLUMN INDICATION]
        [GROUP DATA]
        3
        1 1 1
        2 2 2
        2 3 4
        [END OF GROUP DATA]
        [END OF GROUP]

        returning:
        [
            {"A": 1, "B": 1, "C": 1},
            {"A": 1, "B": 1, "C": 1},
            {"A": 2, "B": 3, "C": 4}
        ]

        The group name can differ and is not parsed,
        but the classname is used as fieldname.

        Arguments:
            data {str} -- Data to parse.
        """
        groups = DSerieParser.parse_group_as_dict(text)
        if not len(groups) == 2:
            raise ParserError(f"Error parsing for {cls}, expected only 2 elements.")
        for groupname, text in groups.items():
            if groupname == "column_indication":
                columns = [make_key(line) for line in text.split("\n") if line != ""]
            else:
                lines = [
                    split_line_elements(line) for line in text.split("\n") if line != ""
                ]
                cls.validate_number_of_rows(lines)
        lines = [dict(zip(columns, parts)) for parts in lines]

        d = {cls.__name__.lower(): lines}
        return cls(**d)

    @classmethod
    def validate_number_of_rows(cls, lines: List[List[str]]):
        """Validates whether the number of lines matched the expected rows to be read.

        Args:
            lines (List[List[str]]): Lines representing rows of data.
        Raises:
            ParserError: When the expectations are not met.
        """
        count = int(lines.pop(0)[0])
        if not count == len(lines):
            raise ParserError(
                f"Error parsing for {cls}, header indicates {count} lines, while there are {len(lines)} lines."
            )


class DSeriesWrappedTableStructure(DSeriesTableStructure):
    @classmethod
    def validate_number_of_rows(cls, lines):
        """These sort of tables do not contain information of the number of rows
        contained in the file. Therefore they are not validated.

        Args:
            lines (List[str]): Parsed rows.
        """
        pass

    @classmethod
    def parse_text(cls, text):
        unwrapped_text = DSerieParser.parse_group_as_dict(text)
        return super().parse_text(list(unwrapped_text.values())[0])


class DSerieOldTableStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure that can parse fields like

        [GROUP]
        [COLUMN INDICATION]
        A
        B
        C
        [END OF COLUMN INDICATION]
        [DATA COUNT]
        3
        [END OF DATA COUNT]
        [GROUP DATA]
        1 1 1
        2 2 2
        2 3 4
        [END OF GROUP DATA]
        [END OF GROUP]

        returning:
        [
            {"A": 1, "B": 1, "C": 1},
            {"A": 1, "B": 1, "C": 1},
            {"A": 2, "B": 3, "C": 4}
        ]

        The group name can differ and is not parsed,
        but the classname is used as fieldname.

        Arguments:
            data {str} -- Data to parse.
        """
        groups = DSerieParser.parse_group_as_dict(text)
        if not len(groups) == 3:
            raise ParserError(f"Error parsing for {cls}, expected only 3 elements.")
        for groupname, text in groups.items():
            if groupname == "column_indication":
                columns = [make_key(line) for line in text.split("\n") if line != ""]
            elif groupname == "data_count":
                lines = [
                    split_line_elements(line) for line in text.split("\n") if line != ""
                ]
                count = int(lines[0][0])
            else:
                lines = [
                    split_line_elements(line) for line in text.split("\n") if line != ""
                ]
                if not count == len(lines):
                    raise ParserError(
                        f"Error parsing for {cls}, header indicates {count} lines, while there are {len(lines)} lines."
                    )

        lines = [dict(zip(columns, parts)) for parts in lines]
        d = {cls.__name__.lower(): lines}
        return cls(**d)


class DSerieListStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure that can parse fields like

        [GROUP]
        3
        1
        1
        1
        [END OF GROUP]

        returning:
        [1,1,1]

        Arguments:
            data {str} -- Data to parse.
        """
        lines = [
            strip_line_first_element(line) for line in text.split("\n") if line != ""
        ]
        nrow = int(lines.pop(0))
        if not nrow == len(lines):
            raise ParserError(
                f"Error parsing for {cls}, header indicates {nrow} lines, while there are {len(lines)} lines."
            )
        d = {cls.__name__.lower(): lines}
        return cls(**d)

    @classmethod
    def parse_text_lines(cls, lines: List[List[str]]):
        d = {cls.__name__.lower(): [line[0] for line in lines]}
        return cls(**d), 1


class DSerieMatrixStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure that can parse fields like

        [GROUP]
        3
        1 2
        1 2
        1 2
        [END OF GROUP]

        returning:

        [[1,2], [1,2], [1,2]]

        Arguments:
            data {str} -- Data to parse.
        """
        lines = [split_line_elements(line) for line in text.split("\n") if line != ""]
        nrow = int(lines.pop(0)[0])
        ncol = int(lines.pop(0)[0]) + 1
        if not nrow == len(lines):
            raise ParserError(
                f"Error parsing for {cls}, header indicates {nrow} lines, while there are {len(lines)} lines."
            )
        if not ncol == len(lines[0]):
            raise ParserError(
                f"Error parsing for {cls}, header indicates {ncol} columns, while there are {len(lines[0])} columns."
            )
        d = {cls.__name__.lower(): lines}
        return cls(**d)


class DSeriesInlineProperties(DSeriesStructure):
    """Generates a structure where the properties are assumed to be
    in the same order as define in the concrete implementation.
    Hence, only the read value field is relevant here.
    Use when properties are in order.
    Example:
        Given class my_structure(DSeriesInlineProperties):
            property_one: int
        and text, text_to_parse:
            [InlineStructure]
            dummy_text: 42 some unit/and scale
            [END OF InlineStructure]
        When ms = my_structure.parse_text(text)
        Then:
            parsed_structure.property_one = 42

    Returns:
        DSeriesStructure: Parsed structure.
    """

    @classmethod
    def header_lines(cls) -> int:
        """Returns the amount of header lines expected for the text.
        Concrete classes can override this method.

        Returns:
            int: Number of header lines to skip.
        """
        return 0

    @classmethod
    def get_property_key_value(cls, text: str, expected_property: str) -> Tuple[str, str]:
        """Gets the property key and value for a given text line.
        It allows concrete classes to override it and either use the expected property
        name or another value.

        Args:
            text (str): Text line to parse.
            expected_property (str): The expected property key if parsing the structure properties in order.

        Returns:
            Tuple[str, str]: Property name and property value text.
        """
        # If there's no key it's because this is actually a property,
        # the real key and values are stored in the second item of the tuple.
        if text:
            # If the value is not empty, extract its value (assume it's on the first position)
            # Note: If that is the case, you should be using other structure such as:
            # DSeriesRepeatedGroupsWithInlineMappedProperties
            _, value = get_line_property_key_value(text, reversed_key=False)
            return expected_property, value
        return expected_property, text

    @classmethod
    def get_properties_in_text(cls, text: str):
        required_properties_names = [
            structure_name for structure_name, _ in cls.get_structure_required_fields()
        ]
        header_lines = cls.header_lines()
        for idx, (key, value) in enumerate(
            DSerieParser.parse_group(text, loose_properties=True)
        ):
            if idx < header_lines:
                continue
            if not key:
                # Only loose properties would get through here.
                # So a grouped property enclosed like [PROPERTY][END OF PROPERTY].
                key, value = cls.get_property_key_value(
                    value, required_properties_names[idx - header_lines]
                )
            yield key, value

    @classmethod
    def parse_text(cls, text: str) -> DSeriesStructure:
        """Parses a text containing a list of inline properties which are
        mapped to the properties of the concrete class.
        Example:
            Given:
                [group]
                4.2 = property_one
                2.4 : property_two
                [property_in_group]
                42
                [end of property_in_group]
                [end of group]
            Returns:
                {
                    property_one: "4.2",
                    property_two: "2.4",
                    property_in_group: "42",
                }
        Args:
            text (str): Inline properties list.

        Returns:
            DSeriesStructure: Parsed structure.
        """
        return cls(**{key: value for key, value in cls.get_properties_in_text(text)})


class DSeriesInlineMappedProperties(DSeriesInlineProperties):
    """Specialization of DSeriesInlineProperties, use this class when the
    properties in the text are the same as in the concrete class definition:
    Example:
        Given class my_structure(DSeriesInlineMappedProeprties):
            property_dummy_int: int
            property_dummy_str: str
        and text, text_to_parse:
            [STRUCTURE]
            property dummy int = 42 some unit/scale
            [PROPERTY DUMMY STR]
            It also works with mixed groups.
            [END OF PROPERTY DUMMY STR]
            [END OF STRUCTURE]
        When ms = my_structure.parse_text(text_to_parse)
        Then:
            ms.property_dummy_int = 42
            ms.proeprty_dummy_str = "It also works with mixed groups."
    """

    @classmethod
    def get_property_key_value(cls, text: str, expected_property: str) -> Tuple[str, str]:
        """Gets both property key and value from the text line.

        Args:
            text (str): Text containing key and value.
            expected_property (str): The expected property if there was no key.

        Returns:
            Tuple[str, str]: Parsed key and value.
        """
        key = expected_property
        unformatted_key, value = get_line_property_key_value(text, reversed_key=False)
        if unformatted_key:
            key = make_key(unformatted_key)
        return key, value


class DSerieVersion(DSeriesInlineMappedProperties):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.dict().items():
            if self.__fields__.get(k).get_default() != v:
                logger.warning(
                    """The version of the input file is unsupported.
                Check the documentation on how to prevent this warning in the future."""
                )
                break


class DSeriesInlineReversedProperties(DSeriesInlineProperties):
    @classmethod
    def get_property_key_value(cls, text: str, expected_property: str) -> Tuple[str, str]:
        """Returns the value content for a line of format:
        value : key || value = key

        Args:
            text (str): Text line with value-key

        Returns:
            str: Filtered value.
        """
        if text:
            # If the value is not empty, extract its value (assume it's on the first position)
            _, value = get_line_property_key_value(text, reversed_key=True)
            return expected_property, value
        return expected_property, text


class DSeriesUnmappedNameProperties(DSeriesInlineMappedProperties):
    """Specialization of DSeriesInlineMappedProperties, use this class when the
    properties in the text are the same as in the concrete class definition except
    for "name", which has not been declared as a key in the input text:
    Example:
        Given class my_structure(DSeriesInlineMappedProeprties):
            name: str
            property_dummy_int: 42
        and text, text_to_parse:
            [STRUCTURE]
            This is a name
            property dummy int = 42 some unit/scale
            [END OF STRUCTURE]
        When ms = my_structure.parse_text(text_to_parse)
        Then:
            ms.name: "This is a name"
            ms.property_dummy_int = 42
    """

    @classmethod
    def get_property_key_value(cls, text: str, expected_property: str) -> Tuple[str, str]:
        """Gets both property key and value from the text line.

        Args:
            text (str): Text containing key and value.
            expected_property (str): The expected property if there was no key.

        Returns:
            Tuple[str, str]: Parsed key and value.
        """

        if expected_property == "name":
            return expected_property, text.strip()
        return super().get_property_key_value(text, expected_property)


class DSeriesStructureCollection(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str) -> DSeriesStructure:
        """Parses a text containing a collection of DSeriesStructure.
        Example:
            Given:
                [STRUCTURE COLLECTION]
                    2 = Number of items
                    [STRUCTURE]
                    Property 1 = 1
                    Property 2 = 2
                    [END OF STRUCTURE]
                    [STRUCTURE]
                    Property 1 = 3
                    Property 2 = 4
                    [END OF STRUCTURE]
                [END OF STRUCTURE]
            Returns:
                [
                    structure({property_1: 1, property_2: 2}),
                    structure({property_1: 3, property_2: 3}),
                ]

        Args:
            text (str): Text containing collection to parse.

        Raises:
            ValueError: When number of read structures does not match declared expectation.
            ValueError: When number of concrete class properties is not equal to 1.

        Returns:
            DSeriesStructure: Parsed structure.
        """
        fields = cls.get_structure_required_fields()
        if len(fields) != 1:
            raise ValueError(
                f"This type of collection is only meant to have one field but {len(fields)} were defined."
            )

        parsed_groups = [
            text_value
            for _, text_value in DSerieParser.parse_group(text, loose_properties=True)
        ]
        number_of_groups = get_line_property_value(
            parsed_groups.pop(0), reversed_key=True
        )

        if len(parsed_groups) != int(number_of_groups):
            raise ValueError(
                f"Expected {number_of_groups} groups, but parsed {len(parsed_groups)}."
            )

        parsed_collection = {fields[0][0]: parsed_groups}
        return cls(**parsed_collection)


class DSeriesRepeatedGroupedProperties(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str) -> DSeriesStructure:
        """Parses a structure which fields are all encapsulated in subgroups,
        some of them might appear repeated and they have to be grouped in lists.
        Example:
            Given input:
                [PROPERTY ONE]
                    42
                    2.4
                [END OF PROPERTY ONE]
                [PROPERTY ONE]
                    24
                    4.2
                [END OF PROPERTY ONE]
            Returns:
                {'property_one': ['42\n2.4\n', '24\n4.2\n']}

        Args:
            text (str): Text to parse.

        Returns:
            DSeriesStructure: Parsed structrure.
        """
        generated_dict = {}
        no_key_group_values = []
        for group_key, group_values in groupby(
            list(DSerieParser.parse_group(text, loose_properties=True)),
            lambda key_value: key_value[0],
        ):
            filtered_values = [value for key, value in group_values]
            if not group_key:
                no_key_group_values.extend(filtered_values)
                continue
            if cls.group_value_is_list(group_key):
                if group_key in generated_dict:
                    generated_dict[group_key].extend(filtered_values)
                else:
                    generated_dict[group_key] = filtered_values
            else:
                generated_dict[group_key] = filtered_values[0]

        generated_dict.update(cls.get_inline_properties(no_key_group_values))
        return cls(**cls.get_validated_mappings(generated_dict))

    @classmethod
    def group_value_is_list(cls, group_key: str) -> bool:
        """Returns whether a group key should be parsed as list or flat value.
        Allows inherited classes to override its behavior.

        Args:
            group_key (str): Property name.

        Returns:
            bool: Whether the key represents a list of values or not.
        """
        return group_key in cls.get_list_field_names()

    @classmethod
    def get_list_field_names(cls) -> List[str]:
        """Returns the field names which are typed as list.
        Allows for extension on concrete classes.

        Returns:
            List[str]: List of field names.
        """
        return [
            field_name
            for field_name, field_type in get_type_hints(cls).items()
            if is_list(field_type)
        ]

    @classmethod
    def get_inline_properties(cls, inline_properties: List[str]) -> Dict[str, str]:
        """Processes all unmapped properties and returns them in a dictionary.
        This method can be replaced in concrete implementations of this class.
        Args:
            inline_properties (List[str]): List of property values which key was not found.
        Returns:
            Dict[str, str]: Returns a dictionary of inline properties.
        """
        logger.debug(
            "The following properties were not mapped because no key was found for them:"
            + "\n".join(inline_properties)
        )
        # This class should not return unmapped properties.
        return {}

    @classmethod
    def get_validated_mappings(cls, generated_dict: Dict[str, str]) -> Dict[str, str]:
        """Validates the input dictionary mapping within this class properties.
        Allows for extension on lower classes.

        Args:
            generated_dict (Dict[str, str]): [description]

        Returns:
            Dict[str, str]: Validated dictionary.
        """
        return generated_dict


class DSeriesRepeatedGroupsWithInlineMappedProperties(DSeriesRepeatedGroupedProperties):
    @classmethod
    def get_inline_properties(cls, inline_properties: List[str]) -> Dict[str, str]:
        """Processes all unmapped properties and returns them in a dictionary.
        This method can be replaced in concrete implementations of this class.
        Follows a philosophy of FIFO for repeated keys.
        Args:
            inline_properties (List[str]): List of property values which key was not found.
        Returns:
            Dict[str, str]: Resulting inline mapped properties.
        """
        result_dict: Dict[str, str] = {}
        for unmapped in inline_properties:
            unformatted_key, value = get_line_property_key_value(
                unmapped, reversed_key=False
            )
            key = make_key(unformatted_key)

            if not key:
                # If no value was found then we just need the stripped remaining.
                value = unmapped.strip()

            if key in result_dict:
                logger.debug(
                    f"Key {key} already mapped, value {value} will not be mapped."
                )
                continue
            result_dict[key] = value
        return result_dict


# region TODO: Deprecate.


class DSeriesTreeStructure(DSeriesStructure):
    # TODO Deprecate.
    # This class is overdoing logic that is later on being handled by its parent (DSeriesStructure).
    # It should therefore only be responsible for generating a dictionary of field name - string values,
    # but not object creation.
    @classmethod
    def parse_text(cls, text: str) -> DSeriesStructure:
        """Parses a text containing listed properties.
        Example:
        1 - structure id
        2 - number of values for property X:
            4 2

        Args:
            text (str): text to parse into properties.

        Returns:
            DSeriesStructure: Structure with parsed properties.
        """
        parsed_structure, _ = cls.parse_text_lines(
            [split_line_elements(line) for line in text.split("\n") if line != ""]
        )
        return parsed_structure

    @classmethod
    def parse_text_lines(
        cls, text_lines: List[List[str]]
    ) -> Tuple[DSeriesStructure, int]:
        """Parses a list of strings into the properties of a structure.
        Example:
            [   ["1", "Property value"],
                ["2", "Values in Property"],
                ["4", "2"]]
        Args:
            text_lines (List[List[str]]): List of properties as strings.

        Raises:
            ValueError: When the number of values for a property does not match its definition.
            ValueError: When the number of properties does not match the text definition.

        Returns:
            DSeriesStructure: Structure with parsed properties.
            int: Index of last line being read as part of current structure.
        """

        def get_list_values(
            struct_idx: int, field_name: str, text_lines: list
        ) -> Tuple[DSeriesStructure, int]:
            """Auxiliar method to either parse as a DSeriesStructure or as a list of
            any different object.

            Args:
                struct_idx (int): Type index in the class definition.
                field_name (str): Name of the field.
                text_lines (list): Lines containing values to parse.

            Returns:
                Tuple[DSeriesStructure, int]: Parsed structure and lines read.
            """
            list_type = get_field_collection_type(cls, struct_idx)
            if issubclass(list_type, DSeriesTreeStructureCollection):
                return list_type.parse_text_lines(text_lines)
            else:
                return read_property_as_list(field_name, list_type, text_lines)

        properties = {}
        required_fields = cls.get_structure_required_fields()

        if len(text_lines) < len(required_fields):
            raise ValueError(
                f"There should be at least {len(required_fields)}"
                + f" fields to correctly initalize object {cls}"
            )
        lines_read = 0
        for struct_idx, (field_name, field) in enumerate(required_fields):
            if lines_read >= len(text_lines):
                raise ValueError(f"Expected text line property for {field_name}.")
            iteration_lines = 1
            field = unpack_if_union(field)
            # if the current property is a list, then extract the next line values.
            if (
                is_list(field)
                or issubclass(field, list)
                or is_structure_collection(field)
            ):
                lines_to_parse = cls.get_next_property_text_lines(text_lines[lines_read:])
                parsed_tuple = get_list_values(struct_idx, field_name, lines_to_parse)
                (
                    properties[field_name],
                    iteration_lines,
                ) = cls.get_tree_structure_read_lines(parsed_tuple)
            elif field == str:  # for names in structures
                properties[field_name] = " ".join(text_lines[lines_read]).strip()
            else:
                properties[field_name] = get_line_property_value(
                    text_lines[lines_read][0], reversed_key=True
                )
            lines_read += iteration_lines
            if len(properties) == len(required_fields):
                break
        return cls(**properties), lines_read

    @classmethod
    def get_next_property_text_lines(cls, text_lines: list) -> list:
        """Allows inherited classes to override the text lines that are fed into other
        structures contained in a list property.

        Args:
            text_lines (list): List containing other lists or flat text to be parsed.

        Returns:
            list: Filtered list of text to be parsed into a property.
        """
        return text_lines

    @classmethod
    def get_tree_structure_read_lines(
        cls, parsed_tuple: Tuple[DSeriesStructure, int]
    ) -> Tuple[DSeriesStructure, int]:
        """Allows inherited classes to override how many lines have been actually been read
        for a given parsed structure based on the cls being instantiated.

        Args:
            parsed_tuple (Tuple[DSeriesStructure, int]): Tuple of parsed structure and read lines for it.

        Returns:
            Tuple[DSeriesStructure, int]: Resulting tuple with real number of parsed lines.
        """
        return parsed_tuple


class DSeriesTreeStructurePropertiesInGroups(DSeriesTreeStructure):
    # TODO Deprecate.
    # This class is overdoing logic that is later on being handled by its parent (DSeriesStructure).
    # It should therefore only be responsible for generating a dictionary of field name - string values,
    # but not object creation.
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure which properties are divided in subgroups.
        Example

        [PROPERTY_1]
        42
        [END OF PROPERTY_1]
        [PROPERTY_2]
        24, 42
        [END OF PROPERTY_2]
        returns:
        DSeriesTreeStructurePropertiesInGroups({
            property_1: 42,
            property_2: [24, 42]
        })

        Arguments:
            data {str} -- Data to parse.
        """
        tuple_lines = [[value, key] for key, value in DSerieParser.parse_group(text)]
        return cls.parse_text_lines(tuple_lines)[0]

    @classmethod
    def get_next_property_text_lines(cls, text_lines: list) -> list:
        """Retrieves the first element of a list of Tuples[PropertyTextValue, PropertyName]
        and splits it into further parseable lines.

        Args:
            text_lines (list): list of Tuples[PropertyTextValue, PropertyName].

        Returns:
            list: List of lines representing a property value (another structure).
        """
        filtered_property_lines = [
            split_line_elements(line)
            for line in text_lines[0][0].split("\n")
            if line != ""
        ]
        return filtered_property_lines

    @classmethod
    def get_tree_structure_read_lines(
        cls, parsed_tuple: Tuple[DSeriesStructure, int]
    ) -> Tuple[DSeriesStructure, int]:
        # Only one line is meant to be read as parsed_text_lines is mapped 1:1 lines-properties.
        return parsed_tuple[0], 1


class DSeriesTreeStructureCollection(DSeriesStructure):
    # TODO Deprecate.
    # This class is overdoing logic that is later on being handled by its parent (DSeriesStructure).
    # It should therefore only be responsible for generating a dictionary of field name - string values,
    # but not object creation.
    @classmethod
    def parse_text(cls, text: str) -> DSeriesStructure:
        """Parses a text into a list of fields that is then
        parsed into the single collection property of this class.
        Example:
            1 - number of structures
                1 - Structure id
                    2 - Number of values in property
                        4 2
        Args:
            text (str): Text to be parsed into collection of structures.

        Raises:
            ValueError: When the number of structures does not match the defined in the text.

        Returns:
            DSeriesStructure: Parsed structure containing collection of other structures.
        """

        parsed_structure, _ = cls.parse_text_lines(
            [split_line_elements(line) for line in text.split("\n") if line != ""]
        )

        return parsed_structure

    @classmethod
    def get_number_of_structures(cls, lines: List[List[str]]) -> int:
        """Provides an overridable method that retrieves the number of
        structures contained in the tree collection.

        Args:
            lines (List[List[str]]): Tree collection lines.

        Returns:
            int: Number of structures expected.
        """
        return int(get_line_property_value(lines[0][0], reversed_key=True))

    @classmethod
    def parse_collection_type(
        cls, collecion_type: Type, lines: list
    ) -> Tuple[DSeriesStructure, int]:
        return collecion_type.parse_text_lines(lines)

    @classmethod
    def parse_text_lines(cls, lines: List[str]) -> Tuple[DSeriesStructure, int]:
        # Get class types
        collection_property_name = list(cls.__fields__.items())[0][0]
        structure_type = get_field_collection_type(cls, 0)
        # Parse elements.
        number_of_structures = cls.get_number_of_structures(lines)
        parsed_structures_collection = []
        read_lines = 1
        for _ in range(number_of_structures):
            if read_lines >= len(lines):
                raise ValueError(
                    f"Expected {number_of_structures} structures,"
                    + " but missing text lines for "
                    + f"{number_of_structures - len(parsed_structures_collection)}."
                )
            parsed_structure, parsed_lines = cls.parse_collection_type(
                structure_type, lines[read_lines:]
            )
            read_lines += parsed_lines
            parsed_structures_collection.append(parsed_structure)

        return cls(**{collection_property_name: parsed_structures_collection}), read_lines


class DSeriesMatrixTreeStructureCollection(DSeriesTreeStructureCollection):
    # TODO Deprecate.
    # This class is overdoing logic that is later on being handled by its parent (DSeriesStructure).
    # It should therefore only be responsible for generating a dictionary of field name - string values,
    # but not object creation.
    @classmethod
    def parse_collection_type(
        cls, collecion_type: Type, lines: list
    ) -> Tuple[DSeriesStructure, int]:
        parsed_structure, _ = collecion_type.parse_text_lines(
            [[line] for line in lines[0]]
        )
        return parsed_structure, 1


# endregion


class DSeriesNoParseSubStructure(DSeriesStructure):
    """DSerie structure that prevents its field from
    being parsed further."""

    @staticmethod
    def is_parseable() -> bool:
        return False


class DSerieParser(BaseParser):
    """Class to parse older DSerie formats in a generic way."""

    def __init__(self, filename: FilePath = None):
        if filename:
            self.datastructure = self.parse(filename)

    @property
    @abstractmethod
    def dserie_structure(self) -> BaseModelStructure:
        raise NotImplementedError("Implement in derived classes.")

    @property
    @abstractmethod
    def suffix_list(self) -> List[str]:
        raise NotImplementedError("Implement in derived classes.")

    def parse(self, filename: FilePath) -> DSeriesStructure:
        logger.debug(f"Parsing {filename}")

        with open(filename) as io:
            datastructure = self.dserie_structure.parse_text(io.read())

        return datastructure

    @staticmethod
    def parse_group_as_dict(text_lines: str) -> Dict[str, str]:
        """Parses a text with headers such as
        [GROUP] and [END OF GROUP] into a dict.

        Arguments:
            text {str} -- List of fields

        Returns:
            dict -- Parsed dictionary.

        Can parse the following:

        [GROUP A]
        data
        more_data
        [END OF GROUP A]

        into:

        {
            "group_a": "data\nmore_data"
        }

        """
        return dict(DSerieParser.parse_group(text_lines=text_lines, unique_keys=True))

    @staticmethod
    def parse_group(
        text_lines: str, loose_properties: bool = False, unique_keys: bool = False
    ) -> Iterable[Tuple[str, str]]:
        """Parses a text with headers such as [GROUP] and [END OF GROUP] and
        yields each property of the group as a Tuple[property name, value].
        Because it is an iterable it may contain repeated elements.
        Delegating responsibility on what to do with such elements to the caller.

        Example:

        [GROUP A]
        data
        more_data
        [END OF GROUP A]

        into:

        (
            "group_a": "data\nmore_data"
        )

        Args:
            text_lines (str): List of fields.
            loose_properties (bool, optional): Properties without a key are yielded.
            unique_keys (bool, optional): Whether elements can be repeated or not.

        Raises:
            Exception: [description]

        Returns:
            Iterable[Tuple[str, str]]: Parsed collection of property values, can include repe.

        Yields:
            Iterator[Iterable[Tuple[str, str]]]: Parsed Tuple[Property name, value]
        """
        currentkey = ""
        data = ""
        for i, line in enumerate(text_lines.split("\n")):
            sline = line.strip()
            # keyline
            if sline.startswith("[") and sline.endswith("]"):
                # [ key name ] => key_name
                key = make_key(sline[1:-1])

                # new group
                if currentkey == "":
                    currentkey = key
                    data = ""

                # duplicate group before end
                elif currentkey == key and unique_keys:
                    raise ValueError(
                        f"Can't parse duplicate key {key} at line {i} without first encountering and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    yield currentkey, data.strip()
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data += line + "\n"

            # dataline
            else:
                if currentkey:
                    data += line + "\n"
                elif not currentkey and loose_properties:
                    yield (currentkey, line)

    @staticmethod
    def parse_list_group(
        text: str,
        exceptions=["vertical", "soil", "residual_settlements"],
        skipped_keys=[],
    ) -> Dict[str, Union[List[str], str]]:
        """Method to parse several groups in a sli/sld file that can include repeated groups.

        Includes an exception to always parse a group as a list.
        Can parse the following:

        [GROUP A]
        data
        [END OF GROUP A]
        [GROUP B]
        [GROUP B1]
        data
        [END OF GROUP B1]
        [END OF GROUP B]
        [GROUP B]
        data
        [END OF GROUP B]

        into

        {
         "group_a": "data\n"
         "group_b: [
            "[GROUP B1]\ndata\n[END OF GROUP B1]",
            "data"
        }

        """

        # Output format
        parsed_dict = {}

        currentkey = ""  # current group we're in
        data = ""  # current collection of lines a group

        text_lines = list(filter(None, text.split("\n")))
        for i, line in enumerate(text_lines):
            sline = line.strip()

            # keyline such as [GROUP]
            if sline.startswith("[") and sline.endswith("]"):
                # [ key name ] => key_name
                key = make_key(sline[1:-1])
                if skipped_keys and any(s_key for s_key in skipped_keys if s_key in key):
                    continue

                # new group
                if currentkey == "":
                    currentkey = key
                    data = ""

                # duplicate group before end
                elif currentkey == key:
                    raise ValueError(
                        f"Can't parse duplicate key at line {i} without first encountering and END OF."
                    )

                # end of current group signaled with [END OF GROUP]
                elif key == "end_of_" + currentkey:

                    # If key already exists, this is a repeated group -> List
                    if currentkey in parsed_dict:
                        # Append in case of a list (2+ elements)
                        if isinstance(parsed_dict[currentkey], list):
                            parsed_dict[currentkey].append(data.strip())
                        # Else create the list first (1 element)
                        else:
                            parsed_dict[currentkey] = [
                                parsed_dict[currentkey],
                                data.strip(),
                            ]
                    # If key doesn't exist yet
                    else:
                        # Check whether the group is always a list
                        if currentkey in exceptions:
                            parsed_dict[currentkey] = [data.strip()]
                        # Otherwise add it in as a single group
                        else:
                            parsed_dict[currentkey] = data.strip()

                    # Reset for next group
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data += line + "\n"

            # dataline
            else:
                data += line + "\n"

        return parsed_dict


def make_key(key: str) -> str:
    return (
        key.strip()
        .replace("(", "")
        .replace(")", "")
        .replace("/", "")
        .replace(" - ", "___")
        .replace(" ", "_")
        .replace("-", "__")
        .replace(".", "____")
        .lower()
    )


def strip_line_first_element(text: str):
    return split_line_elements(text)[0]


def split_line_elements(text: str) -> List[str]:
    """Separates by space and tabulator.

    Args:
        text (str): Text to break into separate fields.

    Returns:
        List[str]: List of formatted values.
    """
    # parts = re.split(" |\t", text.strip())
    parts = shlex.split(text.strip())
    values = list(filter(lambda part: part != "", parts))
    return values


def get_line_property_value(text: str, reversed_key: bool) -> str:
    """Returns the property value representation in the dseries files
    assuming is delimited by either ':' or '='.
    Examples:
        Given (reversed_key = True):
            4.2 : property_value
            4.2 = property_value
        Given (reversed_key = False):
            property_value : 4.2
            property_value = 4.2
        Returns:
            4.2

    Args:
        text (str): Unformatted line of text.
        reversed_key (bool): How the key needs to be extracted.

    Returns:
        str: First field containing value.
    """
    _, value = get_line_property_key_value(text, reversed_key)
    return value


def get_line_property_key_value(text: str, reversed_key: bool) -> Tuple[str, str]:
    """Returns the unformatted key and formatted value for a given line.
    Examples:
        reversed_key = False
        key= value 123 -> key, value
        reversed_key = True
        value 123= key asdf -> key, value

    Args:
        text (str): Text from where to extract key and value.
        reversed_key (bool): Whether the key comes before or after the value.

    Returns:
        Tuple[str, str]: Unformatted key and formatted value.
    """
    key_idx, value_idx = (-1, 0) if reversed_key else (0, -1)
    text_parts = re.split(":|=", text.strip())
    key_part = ""
    if len(text_parts) > 1:
        # Only consider a value if there is more than one field.
        key_part = text_parts[key_idx].strip()
    value_part = text_parts[value_idx].strip()
    if value_part:
        # If there was a value in the first field, clean it.
        return key_part, re.split(" ", value_part)[0].strip()
    return key_part, ""


def get_field_collection_type(class_type: Type, field_idx: int) -> Type:
    """Gets the type wrapped by a collection of a given class.
    Example:
        DummyClass:
            dummycollection: List[SubDummyClass]
        get_field_collection_type(DummyClass, 0) -> SubDummyClass

    Args:
        class_type (Type): Class containing a collection field.
        field_idx (int): Position of the collection field in the class.

    Returns:
        Type: The class for the items in the collection.
    """
    list_type = list(class_type.__fields__.items())[field_idx][1]
    if not list_type.sub_fields:
        return list_type.outer_type_
    return list_type.sub_fields[0].outer_type_


def is_structure_collection(field: Type) -> bool:
    return inspect.isclass(field) and issubclass(field, DSeriesStructure)


def read_property_as_list(
    field_name: str, field: Type, text_lines: list
) -> Tuple[List[DSeriesStructure], int]:
    """Reads a property containing a collection of values represented as
    a list of strings.

    Args:
        field_name (str): Name of the field to parse.
        field (Type): Type to parse the values to.
        text_lines (list): List of list of strings containing values.

    Raises:
        ValueError: If the values given don't match the defined expectations.

    Returns:
        Tuple[List[DSeriesStructure], int]: Returns generated DSeriesStructures and lines read.
    """
    # Assumes the values are separated by spaces.
    list_size = int(get_line_property_value(text_lines[0][0], reversed_key=True))
    lines_read = 1
    list_values = []
    # Fetch values from next lines as it might have been split into different lines
    # See GEOLIB-68 to know more about that problem.
    while len(list_values) < list_size:
        if lines_read >= len(text_lines):
            raise ValueError(f"Expected {list_size} values for property {field_name}.")
        iteration_lines = 1
        lines_to_parse = text_lines[lines_read:]
        if issubclass(field, DSeriesTreeStructureCollection):
            # If its an encapsuled collection, number of lines needs to be given.
            lines_to_parse = text_lines[lines_read - 1 :]

        if is_structure_collection(field):
            parsed_values, iteration_lines = field.parse_text_lines(lines_to_parse)
            list_values.append(parsed_values)
        else:
            parsed_values = text_lines[lines_read]
            list_values.extend(parsed_values)
        lines_read += iteration_lines
    return list_values, lines_read
