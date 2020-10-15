import abc
from typing import List

from pydantic import FilePath

from geolib.errors import NotConcreteError
from geolib.models.base_model_structure import BaseModelStructure


class BaseParser(abc.ABC):
    @property
    @abc.abstractmethod
    def suffix_list(self) -> List[str]:
        raise NotConcreteError

    @abc.abstractmethod
    def parse(self, filename: FilePath):
        raise NotConcreteError

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
    def input_parsers(self) -> BaseParser:
        raise NotConcreteError

    @property
    @abc.abstractmethod
    def output_parsers(self) -> BaseParser:
        raise NotConcreteError

    @property
    @abc.abstractmethod
    def parser_name(self) -> str:
        raise NotConcreteError

    def parse(self, filename: FilePath) -> BaseModelStructure:
        for parser in self.input_parsers:
            if parser.can_parse(filename):
                return parser.parse(filename)

        for parser in self.output_parsers:
            if parser.can_parse(filename):
                return parser.parse(filename)
        raise ValueError(f"Unknown extension {filename.suffix} for {self.parser_name}.")
