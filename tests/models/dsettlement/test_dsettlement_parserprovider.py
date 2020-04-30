import pathlib
import os
import pytest

from geolib.models.dsettlement.dsettlement_parserprovider import *
from geolib.models.dsettlement.internal import (
    PiezoLines, PiezoLine,
    Accuracy,
    Points,
    Curves,
    Boundaries,
    Layers)
from tests.utils import TestUtils


class Test_DSettlementInputParser:
    @pytest.mark.unittest
    def test_instantiate(self):
        parser = DSettlementInputParser()
        assert parser is not None
        assert len(parser.suffix_list) == 1

    @pytest.fixture
    def parsed_dsettlement_testfile(self):
        # 1. Define test data
        test_folder = TestUtils.get_local_test_data_dir("dsettlement")
        test_file = pathlib.Path(os.path.join(test_folder, "bm1-1.sli"))
        parser = DSettlementInputParser()
        parsed_structure = None

        # 2. Verify initial expectations
        assert os.path.exists(test_file), "Test file does not exist."

        # 3. Run test
        parsed_structure = parser.parse(test_file)

        # 4. Verify expectations
        assert parsed_structure, 'No structure was parsed.'
        assert isinstance(parsed_structure, DSettlementStructure)

        return parsed_structure

    @pytest.mark.systemtest
    def test_given_testfile_when_parse_then_geometryadded(self, parsed_dsettlement_testfile: DSettlementStructure):
        # 1. Define test data.
        geometry_data_key = "geometry_data"
        parsed_structure = parsed_dsettlement_testfile
        keys_in_structure = {
            "accuracy": Accuracy,
            "points": Points,
            "curves": Curves,
            "boundaries": Boundaries,
            "layers": Layers,
            "world_co__ordinates": str}

        # 2. Verify expectations.
        parsed_struct_asdict = dict(parsed_structure)
        assert geometry_data_key in parsed_struct_asdict.keys(), "" + \
            "Geometry should be wrapping the piezo lines and " + \
            "was not imported."
        geometry_dict: dict = dict(parsed_struct_asdict[geometry_data_key])
        errors: list = []
        for key, key_type in keys_in_structure.items():
            if not (key in geometry_dict.keys()):
                errors.append(f"Key {key} has not been parsed.")
            elif not (isinstance(geometry_dict[key], key_type)):
                errors.append(
                    f"Key type {key_type} expected, " +
                    f"but got {type(geometry_dict[key])}.")

        if errors:
            parsed_errors = "\n".join(errors)
            pytest.fail(
                "Not all properties were parsed correctly: " +
                f"{parsed_errors}")

    @pytest.mark.systemtest
    def test_given_testfile_when_parse_then_piezovaluesadded(self, parsed_dsettlement_testfile: DSettlementStructure):
        # 1. Define test data
        geometry_data_key = "geometry_data"
        piezo_lines_key = "piezo_lines"
        piezolines_key = "piezolines"
        expected_piezolines_curves = [[4]]
        parsed_structure = parsed_dsettlement_testfile

        # 2. Verify final expectations.
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
