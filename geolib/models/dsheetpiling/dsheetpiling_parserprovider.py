from typing import List, Tuple, Type

from pydantic import FilePath

from geolib.models.dseries_parser import DSerieParser, DSeriesStructure
from geolib.models.parsers import BaseParserProvider

from .internal import DSheetPilingDumpStructure, DSheetPilingStructure


class DSheetPilingInputParser(DSerieParser):
    """DSheetPiling parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".shi"]

    @property
    def dserie_structure(self) -> Type[DSheetPilingStructure]:
        return DSheetPilingStructure


class DSheetPilingOutputParser(DSerieParser):
    """DSheetPiling parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".shd"]

    @property
    def dserie_structure(self) -> Type[DSheetPilingDumpStructure]:
        return DSheetPilingDumpStructure


class DSheetPilingParserProvider(BaseParserProvider):

    __input_parsers = None
    __output_parsers = None

    @property
    def input_parsers(self) -> Tuple[DSheetPilingInputParser]:
        if not self.__input_parsers:
            self.__input_parsers = (DSheetPilingInputParser(),)
        return self.__input_parsers

    @property
    def output_parsers(self) -> Tuple[DSheetPilingOutputParser]:
        if not self.__output_parsers:
            self.__output_parsers = (DSheetPilingOutputParser(),)
        return self.__output_parsers

    @property
    def parser_name(self) -> str:
        return "DSheetPiling"
