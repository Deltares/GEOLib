from typing import List, Tuple, Type

from pydantic import FilePath

from geolib.models.dseries_parser import DSerieParser, DSeriesStructure
from geolib.models.parsers import BaseParserProvider

from .internal import DSettlementOutputStructure, DSettlementStructure


class DSettlementInputParser(DSerieParser):
    """DSettlement parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".sli"]

    @property
    def dserie_structure(self) -> Type[DSettlementStructure]:
        return DSettlementStructure


class DSettlementOutputParser(DSerieParser):
    """DSettlement parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return [".sld"]

    @property
    def dserie_structure(self) -> Type[DSettlementOutputStructure]:
        return DSettlementOutputStructure


class DSettlementParserProvider(BaseParserProvider):

    __input_parsers = None
    __output_parsers = None

    @property
    def input_parsers(self) -> Tuple[DSettlementInputParser]:
        if not self.__input_parsers:
            self.__input_parsers = (DSettlementInputParser(),)
        return self.__input_parsers

    @property
    def output_parsers(self) -> Tuple[DSettlementOutputParser]:
        if not self.__output_parsers:
            self.__output_parsers = (DSettlementOutputParser(),)
        return self.__output_parsers

    @property
    def parser_name(self) -> str:
        return "DSettlement"
