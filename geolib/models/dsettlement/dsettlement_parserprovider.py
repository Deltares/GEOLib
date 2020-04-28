from typing import List, Type

from pydantic import FilePath

from geolib.models.dseries_parser import DSerieParser, DSeriesStructure
from geolib.models.parsers import BaseParserProvider

from .internal import DSettlementStructure, DSettlementOutputStructure


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

    __input_parser = None
    __output_parser = None

    @property
    def input_parser(self) -> DSettlementInputParser:
        if not self.__input_parser:
            self.__input_parser = DSettlementInputParser()
        return self.__input_parser

    @property
    def output_parser(self) -> DSettlementOutputParser:
        if not self.__output_parser:
            self.__output_parser = DSettlementOutputParser()
        return self.__output_parser

    @property
    def parser_name(self) -> str:
        return "DSettlement"
