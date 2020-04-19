import logging
from abc import abstractmethod
from typing import List, get_type_hints, _GenericAlias

from pydantic import BaseModel as DataModel
from pydantic import FilePath

from geolib.models.base_model import BaseModelStructure
from geolib.models.parsers import BaseParser, BaseParserProvider


class DSeriesStructure(BaseModelStructure):

    def __init__(self, *args, **kwargs):
        # TODO Needs a refactor!

        for field, fieldtype in get_type_hints(self).items():
            # If the body is a string, we should check
            # whether we can parse it further.
            if field in kwargs and isinstance(kwargs[field], str):
                body = kwargs[field]

                # Check if it's a union
                if type(fieldtype) == _GenericAlias:  # quite hacky
                    element_type, *_ = fieldtype.__args__  # use getargs in 3.8

                    if element_type.is_parseable():
                        kwargs[field] = element_type.parse_text(body)
                    else:
                        logging.warning(f"Can't parse {element_type} for {field} yet")

                elif type(DSeriesStructure) in type(fieldtype).__mro__:
                    kwargs[field] = fieldtype.parse_text(body)

            # If the body is a list[string], we should check
            # whether we can parse it further.
            elif field in kwargs and isinstance(kwargs[field], list) and isinstance(kwargs[field][0], str):
                body = kwargs[field]
                element_type, *_ = fieldtype.__args__[0].__args__
                if element_type.is_parseable():
                    kwargs[field] = [element_type.parse_text(item) for item in body]
                else:
                    logging.warning(f"Can't parse {element_type} for {field} yet")

        super().__init__(*args, **kwargs)

    @staticmethod
    def is_parseable() -> bool:
        return True

    @classmethod
    def parse_text(cls, data: str):
        """ Creates a DSeriesStructure using the concrete parser.

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_group(data)
        return cls(**parsed_structure)


class DSeriesListSubStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, data: str):
        """ Creates a DSeriesStructure using the concrete parser
        for fields such key=value.

        Arguments:
            data {str} -- Data to parse.
        """
        parsed_structure = DSerieParser.parse_list_group(data)
        return cls(**parsed_structure)

class DSeriesNoParseSubStructure(DSeriesStructure):

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

    def parse(self, filename: FilePath):
        logging.warning(f"Parsing {filename}")

        with open(filename) as io:
            datastructure = self.dserie_structure.parse_text(io.readlines())

        return datastructure

    # def parse_collection(self, parsed_text: str) -> List[DSeriesStructure]:
    #     """Parses a given text into a collection of DSeriesStructure

    #     Arguments:
    #         parsed_text {str} -- Text containing collection of structures.

    #     Returns:
    #         List[DSeriesStructure] -- Result parsed structures
    #     """
    #     text_fields = [pt + "\n" for pt in filter(None, parsed_text.split("\n"))]
    #     value_list = []
    #     for _, value in self.parse_group(text_fields):
    #         value_list.append(value)
    #     return value_list

    @staticmethod
    def parse_group(text_lines: List[str]) -> dict:
        """Parses a text containing fields of type key=value into a dictionary

        Arguments:
            text {str} -- List of fields

        Returns:
            dict -- Parsed dictionary.
        """
        parsed_dictionary = {}
        currentkey = ""
        data = ""
        for i, line in enumerate(text_lines):
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
                        f"Can't parse duplicate key at line {i} without first encountering and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    parsed_dictionary[currentkey] = data
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data += line

            # dataline
            else:
                data += line
        
        return parsed_dictionary

    @staticmethod
    def parse_list_group(text: str) -> list:
        parsed_list = []
        currentkey = ""
        collection_key = ""
        data = ""
        text_lines = list(filter(None, text.split("\n")))
        for i, line in enumerate(text_lines):
            sline = line.strip()
            # keyline
            if sline.startswith("[") and sline.endswith("]"):
                # [ key name ] => key_name
                key = make_key(sline[1:-1])

                # new group
                if currentkey == "":
                    currentkey = key
                    collection_key = key
                    data = ""

                # duplicate group before end
                elif currentkey == key:
                    raise Exception(
                        f"Can't parse duplicate key at line {i} without first encountering and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    parsed_list.append(data)
                    data = ""
                    currentkey = ""

                elif collection_key != key:
                    raise Exception(
                        f"Can't parse list with different keys: {key} is different from collection key: {collection_key}."
                    )

                # sub group that is eaten for now
                else:
                    data += line + "\n"

            # dataline
            else:
                data += line + "\n"
        
        return {collection_key: parsed_list}

    @staticmethod
    def parse_name_key_value(text: str) -> dict:
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
            if len(fields) == 1:
                parsed_dictionary["name"] = fields[0]
                continue
            parsed_dictionary[make_key(fields[0])] = fields[1]
        return parsed_dictionary

    @staticmethod
    def parse_key_value(text: str) -> dict:
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
