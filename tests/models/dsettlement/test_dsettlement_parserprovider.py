import pathlib

import pytest

from geolib.models.dsettlement.dsettlement_parserprovider import *


class Test_DSettlementInputParser:
    @pytest.mark.unittest
    def test_instantiate(self):
        parser = DSettlementInputParser()
        assert parser is not None
        assert len(parser.suffix_list) == 1


class Test_DSettlementOutputParser:
    @pytest.mark.unittest
    def test_instantiate(self):
        parser = DSettlementOutputParser()
        assert parser is not None
        assert len(parser.suffix_list) == 1


class Test_DSettlementParserProvider:
    @pytest.mark.integrationtest
    def test_instantiate(self):
        parser_provider = DSettlementParserProvider()
        assert parser_provider
        assert parser_provider.input_parser is not None
        assert isinstance(parser_provider.input_parser, DSettlementInputParser)
        assert parser_provider.input_parser.suffix_list

        assert parser_provider.output_parser is not None
        assert isinstance(parser_provider.output_parser, DSettlementOutputParser)
        assert parser_provider.output_parser.suffix_list
