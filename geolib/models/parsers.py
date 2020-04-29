import abc

from typing import List

from pydantic import FilePath

from geolib.models.base_model_structure import BaseModelStructure


class BaseParser(abc.ABC):
    @property
    @abc.abstractmethod
    def suffix_list(self) -> List[str]:
        raise NotImplementedError("Should be implemented in concrete class.")

    @abc.abstractmethod
    def parse(self, filename: FilePath):
        raise NotImplementedError("Should be implemented in concrete class.")

    def can_parse(self, filename: FilePath) -> bool:
        """Verifies if a file or directory can be parsed with this instance.

        :param filename: File path to the file or directory to parse.
        :type filename: FilePath
        :return: True if it can be parsed, False otherwise.
        :rtype: bool
        """
        if not filename:
            return False

        return (filename.suffix == "" and filename.name in self.suffix_list) or (
            filename.suffix in self.suffix_list
        )


class BaseParserProvider(abc.ABC):
    """Basic class for parser providers."""

    @property
    @abc.abstractmethod
    def input_parser(self) -> BaseParser:
        raise NotImplementedError("Should be implemented in concrete class.")

    @property
    @abc.abstractmethod
    def output_parser(self) -> BaseParser:
        raise NotImplementedError("Should be implemented in concrete class.")

    @property
    @abc.abstractmethod
    def parser_name(self) -> str:
        raise NotImplementedError("Should be implemented in concrete class.")

    def parse(self, filename: FilePath) -> BaseModelStructure:
        if self.input_parser.can_parse(filename):
            return self.input_parser.parse(filename)
        elif self.output_parser.can_parse(filename):
            return self.output_parser.parse(filename)
        else:
            raise Exception(
                f"Unknown extension {filename.suffix} for {self.parser_name}."
            )

        # compare_suffix = filename.suffix

        # if filename.suffix == '':
        #     compare_suffix = filename.name

        # if compare_suffix in self.input_parser.suffix_list:
        #     return self.input_parser.parse(filename)
        # elif compare_suffix in self.output_parser.suffix_list:
        #     return self.output_parser.parse(filename)
        # else:
        #     raise Exception(
        #         f"Unknown extension {compare_suffix} for {self.parser_name}."
        #     )
