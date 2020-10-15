from typing import List, Tuple, Type

from pydantic import FilePath

from geolib.models.dseries_parser import DSerieParser, DSeriesStructure
from geolib.models.parsers import BaseParserProvider

from .internal import (
    DFoundationsDumpfileOutputStructure,
    DFoundationsDumpStructure,
    DFoundationsInputStructure,
    DFoundationsStructure,
)


class DFoundationsInputParser(DSerieParser):
    """DFoundations parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".foi"]

    @property
    def dserie_structure(self) -> Type[DFoundationsStructure]:
        return DFoundationsStructure


class DFoundationsOutputParser(DSerieParser):
    """DFoundations parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".fod"]

    @property
    def dserie_structure(self) -> Type[DFoundationsDumpStructure]:
        return DFoundationsDumpStructure


class DFoundationsParserProvider(BaseParserProvider):

    __input_parsers = None
    __output_parsers = None

    @property
    def input_parsers(self) -> Tuple[DFoundationsInputParser]:
        if not self.__input_parsers:
            self.__input_parsers = (DFoundationsInputParser(),)
        return self.__input_parsers

    @property
    def output_parsers(self) -> Tuple[DFoundationsOutputParser]:
        if not self.__output_parsers:
            self.__output_parsers = (DFoundationsOutputParser(),)
        return self.__output_parsers

    @property
    def parser_name(self) -> str:
        return "DFoundations"
