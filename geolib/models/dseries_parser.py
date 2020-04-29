from __future__ import annotations
import logging
from abc import abstractmethod
from typing import List, get_type_hints, _GenericAlias, _SpecialForm, Dict, Type, Tuple
from pydantic import FilePath, BaseModel as DataClass

from .parsers import BaseParser
from geolib.models.base_model_structure import BaseModelStructure
from .utils import get_args, is_union, is_list
import re


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
        if len(kwargs) > len(get_type_hints(self)):
            raise Exception(
                f"Got more fields {kwargs.keys()} than defined on model {self.__class__.__name__}"
            )

        for field, fieldtype in get_type_hints(self).items():

            # If the body is a string, we should check
            # whether we can parse it further.
            if field in kwargs and isinstance(kwargs[field], str):
                logging.warning(f"Trying to change for {field}")
                body = kwargs[field]

                # Optional, Union, etc.
                if is_union(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                # check if we can parse and if so, parse the strings
                if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                    logging.warning(f"Changed {field} to {fieldtype}")
                    kwargs[field] = fieldtype.parse_text(body)
                else:
                    logging.warning(f"Can't parse {fieldtype} for {field} yet")

            # If the body is a List[string], we should check
            # whether we can parse it further.
            elif (
                field in kwargs
                and isinstance(kwargs[field], list)
                and len(kwargs[field]) > 0
                and isinstance(kwargs[field][0], str)
            ):
                logging.warning(f"Parsing list for {field}")
                body = kwargs[field]

                # We need to decompose a possible Union
                if is_union(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                # And then the list
                if is_list(fieldtype):
                    fieldtype, *_ = get_args(fieldtype)

                    # Check whether we can parse and if so, parse the strings
                    if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                        logging.warning(f"Changed {field} to multiple {fieldtype}")
                        kwargs[field] = [fieldtype.parse_text(item) for item in body]
                    else:
                        logging.warning(f"Can't parse {fieldtype} for {field} yet")

                else:
                    # Check whether we can parse and if so, parse the strings
                    if hasattr(fieldtype, "is_parseable") and fieldtype.is_parseable():
                        logging.warning(
                            f"Changed {field} to single {fieldtype} for list of str."
                        )
                        kwargs[field] = fieldtype.parse_text(body)
                    else:
                        logging.warning(f"Can't parse {fieldtype} for {field} yet")

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
        parsed_structure = DSerieParser.parse_group(data)
        return cls(**parsed_structure)


class DSerieRepeatedTableStructure(DSeriesStructure):
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
        [GROUP DATA]
        4
        1 1 1
        2 2 2
        2 3 4
        [END OF GROUP DATA]
        [END OF GROUP]

        returning:
        {
            "3": [
                {"A": 1, "B": 1, "C": 1},
                {"A": 1, "B": 1, "C": 1},
                {"A": 2, "B": 3, "C": 4}
            ],
            "4": [
                {"A": 1, "B": 1, "C": 1},
                {"A": 1, "B": 1, "C": 1},
                {"A": 2, "B": 3, "C": 4}
            ]
        } 

        The group name can differ and is not parsed,
        but the classname is used as fieldname.

        Arguments:
            data {str} -- Data to parse.
        """
        out = {}
        groups = DSerieParser.parse_list_group(text)
        assert len(groups) == 2
        for groupname, grouptext in groups.items():
            if groupname == "column_indication":
                columns = [make_key(line) for line in grouptext.split("\n") if line != ""]
            else:
                for subgroup in grouptext:
                    lines = [
                        split_line_elements(line)
                        for line in subgroup.split("\n")
                        if line != ""
                    ]
                    time = float(lines.pop(0)[0])
                    lines = [dict(zip(columns, parts)) for parts in lines]
                    assert time not in out
                    out[time] = lines

        d = {cls.__name__.lower(): out}
        return cls(**d)


class DSerieTableStructure(DSeriesStructure):
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
        groups = DSerieParser.parse_group(text)
        assert len(groups) == 2
        for groupname, text in groups.items():
            if groupname == "column_indication":
                columns = [make_key(line) for line in text.split("\n") if line != ""]
            else:
                lines = [
                    split_line_elements(line) for line in text.split("\n") if line != ""
                ]
                count = int(lines.pop(0)[0])
                assert count == len(lines)

        lines = [dict(zip(columns, parts)) for parts in lines]

        d = {cls.__name__.lower(): lines}
        return cls(**d)


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
        groups = DSerieParser.parse_group(text)
        assert len(groups) == 3
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
                assert count == len(lines)

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
        assert nrow == len(lines)
        d = {cls.__name__.lower(): lines}
        return cls(**d)


class DSerieSingleStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        """Creates a DSeriesStructure that can parse fields like

        [GROUP]
        1
        [END OF GROUP]

        returning:
        1

        Arguments:
            data {str} -- Data to parse.
        """
        value = strip_line_first_element(text)
        d = {cls.__name__.lower(): value}
        return cls(**d)


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
        assert nrow == len(lines)
        assert ncol == len(lines[0])
        d = {cls.__name__.lower(): lines}
        return cls(**d)


class ComplexVerticalSubstructure(DSeriesStructure):
    """Specific Vertical substructure with a dedicated
    parser because of the oddities stored in that group."""

    def __init__(self, *args, **kwargs):
        """Replace unnamed arguments by fieldnames in order.

        Some structure in DSerie files have no names attached
        and are just values. This provides a way to still parse
        them.
        """
        largs = list(args)
        for field, fieldtype in self.__fields__.items():
            if len(largs) == 0:
                break
            if field in kwargs:
                continue
            else:
                value = strip_line_first_element(largs.pop(0))
                logging.warning(f"Setting {field}: {fieldtype} to {value}")
                kwargs[field] = value

        if len(largs) > 0:
            raise Exception(f"Failed to convert args to kwargs: {largs} left unmapped.")

        super().__init__(*args, **kwargs)

    @classmethod
    def parse_text(cls, text: str):
        """Parser that:

        - Knows about structure with fields and subgroups
        - Knows about repeated Vertical fields without a specific collection
        - Knows about the bug of time-dependent data groups that end without the - included
        - Knows about the bug of absence of the second end-tag of time-dependent data

        Arguments:
            data {str} -- Data to parse.
        """
        EXCEPTIONS = ["soil", "vertical", "time__dependent_data"]
        parsed_dict = {}
        currentkey = ""
        data = []
        args = []
        text_lines = list(filter(None, text.split("\n")))
        for i, line in enumerate(text_lines):
            sline = line.strip()
            # keyline
            if sline.startswith("[") and sline.endswith("]"):
                # [ key name ] => key_name
                key = make_key(sline[1:-1])

                # new group
                if currentkey == "":
                    logging.warning(f"Found new {key}")
                    currentkey = key
                    if len(data) > 0:
                        args.extend(data)
                    data = []

                # duplicate group before end
                elif currentkey == key:

                    # If key already exists, this is a group -> List
                    if currentkey in parsed_dict:
                        parsed_dict[currentkey] = parsed_dict[currentkey] + [
                            "".join(data)
                        ]
                    elif currentkey in EXCEPTIONS:
                        parsed_dict[currentkey] = ["".join(data)]
                    else:
                        parsed_dict[currentkey] = "".join(data)

                    data = []

                    logging.warning(
                        f"Duplicate key {key} at line {i} without first encountered and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    logging.warning(f"Found {key}")
                    # If key already exists, this is a group -> List
                    if currentkey in parsed_dict:
                        parsed_dict[currentkey] = parsed_dict[currentkey] + [
                            "".join(data)
                        ]
                    elif currentkey in EXCEPTIONS:
                        parsed_dict[currentkey] = ["".join(data)]
                    else:
                        parsed_dict[currentkey] = "".join(data)
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data.append(line + "\n")

            # dataline
            else:
                data.append(line + "\n")

        # Because no [end] exist for duplicate group...
        parsed_dict[currentkey] = parsed_dict[currentkey] + ["".join(data)]

        return cls(*args, **parsed_dict)


class DSeriesListSubStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, data: str):
        """ Creates a DSeriesStructure that can have repeated
        group names as a list, such as [SOIL]

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_list_group(data)
        return cls(**parsed_structure)


class DSeriesTabbedTreeStructure(DSeriesStructure):
    @classmethod
    def list_of_properties(cls) -> List[str]:
        """Gets the list of properties that need to be mapped in the
        order they are expected to be read.

        :raises NotImplementedError: If not implemented in concrete class.
        :return: Ordered list of property names.
        :rtype: List[str]
        """
        return [k for k, _ in cls.__fields__.items()]

    @staticmethod
    def filter_tab(data: str, separator: str):
        return [
            value.strip()
            for value in data.split(separator)
            if value.strip()]

    @classmethod
    def parse_text(cls, data: str) -> DSeriesStructure:
        """Creates a DSeriesStructure using the concrete parser
            for fields such:
            # Object #1.
                # Number of properties for Object #1.
                    # Value for Number of properties #1.
        :param data: parsed text as string.
        :type data: str
        :return: Parsed structure
        :rtype: DSeriesTabbedTreeLines
        """
        tab_level_lines = [
            (DSerieParser.count_separator(line), line)
            for line in data.split("\n")
            if line]
        return cls.parse_text_lines(tab_level_lines)

    @classmethod
    def parse_text_lines(cls, data_lines: List[Tuple[int, str]]) -> DSeriesStructure:
        """Parses a list of lines into a DSeriesStructure of this type.
        Expects values to be sperated by either tabs or spaces. The identation per line
        will determine the property the values belong to.

        Args:
            data_lines (List[Tuple[int, str]]): Tuple of identation level and line content.

        Returns:
            DSeriesStructure: Generated structure with parsed properties.
        """
        list_of_properties = cls.list_of_properties()
        data_dict = {}
        # Assumption: First property represents the 'id', which is not placed at the same
        # identation level as the rest of properties.
        data_dict[list_of_properties[0]] = cls.filter_tab(data_lines[0][1], "-")[0]
        properties_level = min(data_lines[1:])[0]
        properties_idx = [
            idx
            for idx, (level, line) in enumerate(data_lines[1:])
            if level == properties_level]
        for idx, prop_idx in enumerate(properties_idx):
            next_idx = -1
            if not prop_idx == properties_idx[-1]:
                next_idx = properties_idx[idx + 1]
            property_values = [
                value
                for value in re.split(" |\t", data_lines[next_idx][1])
                if value
            ]
            data_dict[list_of_properties[idx + 1]] = property_values

        return cls(**data_dict)


class DSeriesTabbedTreeStructureCollection(DSeriesStructure):
    @classmethod
    def TabbedTreeStructure(cls) -> Tuple[str, Type[DSeriesTabbedTreeStructure]]:
        """Gets the name of the collection property and its type

        :raises NotImplementedError: When not implemented in concrete class.
        :return: Name and Type to implement.
        :rtype: Tuple[str, Type[DSeriesTabbedTreeStructure]]
        """
        fieldmapping = list(cls.__fields__.items())
        assert len(fieldmapping) == 1
        k, v = fieldmapping[0]
        return (k, v.type_)

    @classmethod
    def parse_text(cls, data: str) -> DSeriesStructure:        
        """Creates a DSeriesStructure using the concrete parser
            for fields such:
            # Number of objects.
                # Object #1.
                    # Number of properties for Object #1.
                        # Value for Number of properties #1.

        Args:
            data (str): Parsed text as a string.

        Returns:
            DSeriesStructure: Parsed structure containing a list of other DSeriesStructure.
        """
        tab_level_lines = [(DSerieParser.count_separator(line), line) for line in data.split("\n") if line]
        initial_tabs, header_line = tab_level_lines[0]
        min_tab = min(tab_level_lines[1:])[0]
        structures_idx = [
            idx
            for idx, (tab_count, line) in enumerate(tab_level_lines)
            if tab_count == min_tab
        ]

        # Verify structures_idx len = expected.
        structures = []
        collection_name, structure_type = cls.TabbedTreeStructure()
        for idx, struct_idx in enumerate(structures_idx):
            # If we are at the last index, get the remaining lines as properties
            # for the current structure.
            next_idx = len(tab_level_lines)
            if not struct_idx == structures_idx[-1]:
                # If we are not at the last structure, get the index of the
                # next one so we fetch all the related properties.
                next_idx = structures_idx[idx + 1]
            parsed_structure = structure_type.parse_text_lines(
                tab_level_lines[struct_idx:next_idx]
            )
            structures.append(parsed_structure)

        return cls(**{collection_name: structures})


class DSeriesNoParseSubStructure(DSeriesStructure):
    """DSerie structure that prevents its field from
    being parsed further."""

    @staticmethod
    def is_parseable() -> bool:
        return False


class DSeriesKeyValueSubStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, data: str):
        """ Creates a DSeriesStructure using the concrete parser
        for fields such key=value.

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_key_value(data)
        return cls(**parsed_structure)


class DSeriesNameKeyValueSubStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, data: str):
        """ Creates a DSeriesStructure using the concrete parser
        for fields such key=value, with lines without = defaulting
        to a name key.

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_name_key_value(data)
        return cls(**parsed_structure)


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
        logging.warning(f"Parsing {filename}")

        with open(filename) as io:
            datastructure = self.dserie_structure.parse_text(io.read())

        return datastructure

    @staticmethod
    def parse_group(text_lines: str) -> Dict[str, str]:
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
        parsed_dictionary = {}
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
                elif currentkey == key:
                    raise Exception(
                        f"Can't parse duplicate key {key} at line {i} without first encountering and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    parsed_dictionary[currentkey] = data.strip()
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data += line + "\n"

            # dataline
            else:
                data += line + "\n"

        return parsed_dictionary

    @staticmethod
    def parse_list_group(
        text: str, exceptions=["vertical", "soil", "residual_settlements"]
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

                # new group
                if currentkey == "":
                    currentkey = key
                    data = ""

                # duplicate group before end
                elif currentkey == key:
                    raise Exception(
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

    @staticmethod
    def parse_name_key_value(text: str) -> Dict[str, str]:
        """Parses a text containing fields of type key=value into a dictionary
        with the addition that if one field has no key, it's set to "name".

        Arguments:
            text {str} -- List of fields

        Returns:
            dict -- Parsed dictionary.
        """
        parsed_dictionary = {}
        text_fields_list = list(filter(None, text.split("\n")))
        for text_fields in text_fields_list:
            fields = text_fields.split("=")
            if len(fields) == 1:
                if "name" in parsed_dictionary:
                    raise Exception("Can't parse more than one field {fields[0]} as name")
                parsed_dictionary["name"] = fields[0]
                continue
            parsed_dictionary[make_key(fields[0])] = fields[1]
        return parsed_dictionary

    @staticmethod
    def parse_key_value(text: str) -> Dict[str, str]:
        """Parses a text containing fields of type key=value into a dictionary

        Arguments:
            text {str} -- List of fields

        Returns:
            dict -- Parsed dictionary.
        """
        parsed_dictionary = {}
        text_fields_list = list(filter(None, text.split("\n")))
        for text_fields in text_fields_list:
            fields = text_fields.split("=")
            parsed_dictionary[make_key(fields[0])] = fields[1]
        return parsed_dictionary

    @staticmethod
    def count_separator(line: str) -> int:
        """Returns the number of occurrences of a separator before
        a valid character is found.

        :param line: Line to count start of line separator.
        :type line: str
        :return: Total occurrences of a separator.
        :rtype: int
        """
        separator_count: int = 0
        separators = [" ", "\t"]
        for char in line:
            if not(char in separators):
                return separator_count
            separator_count += 1


def make_key(key: str) -> str:
    return key.strip().replace(" ", "_").replace("-", "__").lower()


def strip_line_first_element(text: str):
    return split_line_elements(text)[0]


def split_line_elements(text: str):
    parts = text.strip().split(" ")
    values = list(filter(lambda part: part != "", parts))
    return values
