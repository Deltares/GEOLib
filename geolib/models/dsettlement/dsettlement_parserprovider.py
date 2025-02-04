from pydantic import FilePath

from geolib.models.dseries_parser import DSerieParser, DSeriesStructure
from geolib.models.parsers import BaseParserProvider

from .internal import DSettlementOutputStructure, DSettlementStructure


class DSettlementInputParser(DSerieParser):
    """DSettlement parser of input files."""

    @property
    def suffix_list(self) -> list[str]:
        return [".sli"]

    @property
    def dserie_structure(self) -> type[DSettlementStructure]:
        return DSettlementStructure


class DSettlementOutputParser(DSerieParser):
    """DSettlement parser of input files."""

    @property
    def suffix_list(self) -> list[str]:
        return [".sld"]

    @property
    def dserie_structure(self) -> type[DSettlementOutputStructure]:
        return DSettlementOutputStructure


class DSettlementParserProvider(BaseParserProvider):
    __input_parsers = None
    __output_parsers = None

    @property
    def input_parsers(self) -> tuple[DSettlementInputParser]:
        if not self.__input_parsers:
            self.__input_parsers = (DSettlementInputParser(),)
        return self.__input_parsers

    @property
    def output_parsers(self) -> tuple[DSettlementOutputParser]:
        if not self.__output_parsers:
            self.__output_parsers = (DSettlementOutputParser(),)
        return self.__output_parsers

    @property
    def parser_name(self) -> str:
        return "DSettlement"
