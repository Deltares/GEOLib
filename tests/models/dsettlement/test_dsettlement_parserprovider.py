import pathlib
import os
import pytest

from geolib.models.dsettlement.dsettlement_parserprovider import *
from geolib.models.dsettlement.internal import PiezoLines, PiezoLine
from tests.utils import TestUtils


class Test_DSettlementInputParser:
    @pytest.mark.unittest
    def test_instantiate(self):
        parser = DSettlementInputParser()
        assert parser is not None
        assert len(parser.suffix_list) == 1

    @pytest.mark.systemtest
    def test_given_testfile_when_parse_then_piezovaluesadded(self):
        # 1. Define test data
        geometry_data_key = "geometry_data"
        piezo_lines_key = "piezo_lines"
        piezolines_key = "piezolines"
        expected_piezolines_curves = [[4]]
        test_folder = TestUtils.get_local_test_data_dir("dsettlement")
        test_file = pathlib.Path(os.path.join(test_folder, "bm1-1.sli"))
        parser = DSettlementInputParser()
        parsed_structure = None

        # 2. Verify initial expectations
        assert os.path.exists(test_file), "Test file does not exist."

        # 3. Run test
        parsed_structure = parser.parse(test_file)

        # 4. Verify final expectations.
        assert parsed_structure, "No structure was parsed."

        parsed_struct_asdict = dict(parsed_structure)
        assert geometry_data_key in parsed_struct_asdict.keys(), "" + \
            "Geometry should be wrapping the piezo lines and " + \
            "was not imported."

        geometry_dict = dict(parsed_struct_asdict[geometry_data_key])
        assert piezo_lines_key in geometry_dict.keys(), "" + \
            "The piezo key was not found as parsed structure."
        assert isinstance(geometry_dict[piezo_lines_key], PiezoLines)

        piezo_lines_dict = dict(geometry_dict[piezo_lines_key])
        assert piezolines_key in piezo_lines_dict.keys()
        assert len(piezo_lines_dict[piezolines_key]) == \
            len(expected_piezolines_curves), "" + \
            "The generated piezolines were not as expected."

        for idx, piezoline in enumerate(piezo_lines_dict[piezolines_key]):
            assert piezoline.curves == expected_piezolines_curves[idx]


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
