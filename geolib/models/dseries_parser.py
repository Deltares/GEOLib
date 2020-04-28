from __future__ import annotations
import logging
from abc import abstractmethod
from typing import List, get_type_hints, _GenericAlias, _SpecialForm, Dict, Type
from pydantic import FilePath, BaseModel as DataClass

from .parsers import BaseParser
from geolib.models.base_model_structure import BaseModelStructure
from .utils import get_args, is_union, is_list


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
                f"Got more fields {kwargs.keys()} than defined on model {self.__name__}"
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


class EvilVerticalSubstructure(DSeriesStructure):
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


def make_key(key: str) -> str:
    return key.strip().replace(" ", "_").replace("-", "__").lower()


def strip_line_first_element(text: str):
    stext = text.strip().split(" ")[0]
    return stext


def split_line_elements(text: str):
    parts = text.strip().split(" ")
    values = list(filter(lambda part: part != "", parts))
    return values
