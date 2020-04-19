import abc
import logging
from typing import List

from pydantic import FilePath


class BaseParser(abc.ABC):
    @property
    @abc.abstractmethod
    def suffix_list(self) -> List[str]:
        raise NotImplementedError("Should be implemented in concrete class.")

    @abc.abstractmethod
    def parse(self, filename: FilePath):
        raise NotImplementedError("Should be implemented in concrete class.")


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

    def parse(self, filename: FilePath):
        if filename.suffix in self.input_parser.suffix_list:
            return self.input_parser.parse(filename)
        elif filename.suffix in self.output_parser.suffix_list:
            return self.output_parser.parse(filename)
        else:
            raise Exception(
                f"Unknown extension {filename.suffix} for {self.parser_name}."
            )
