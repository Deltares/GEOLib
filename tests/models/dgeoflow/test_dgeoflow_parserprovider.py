import os
from pathlib import Path

import pytest

from geolib.models.dgeoflow import DGeoflowModel
from geolib.models.dgeoflow.dgeoflow_parserprovider import DGeoflowParser, DGeoflowZipParser
from geolib.models.dgeoflow.serializer import DGeoflowInputZipSerializer, DGeoflowInputSerializer

from tests.utils import TestUtils


class TestDGeoflowInputParser:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dgeoflow/Berekening3", id="ex 1"),
        ],
    )
    def test_dgeoflow_parse_directory(self, dir_path: str):
        # 1. Set up test model
        input_parser = DGeoflowParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dgeoflow/serialized")
        )

        # 2. Verify initial expectations
        assert os.path.exists(test_filepath), "Testing directory not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        assert input_structure is not None
        data = input_structure.json(indent=4)
        with open(test_output_filepath / "dstability_parsed_input.json", "w") as io:
            io.write(data)

    @pytest.mark.integrationtest
    def test_dgeoflow_parse_flox(self):
        # 1. Set up test model
        input_parser = DGeoflowZipParser()
        test_filepath = (
                Path(TestUtils.get_local_test_data_dir("dgeoflow"))
                / "Berekening3.flox"
        )
        test_output_dir = Path(
            TestUtils.get_output_test_data_dir("dgeoflow/serialized")
        )
        # 2. Verify initial expectations
        assert test_filepath.exists(), "Test .flox not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        assert input_structure is not None
        data = input_structure.json(indent=4)
        with open(test_output_dir / "dgeoflow_parsed_input_flox.json", "w") as io:
            io.write(data)

    @pytest.mark.integrationtest
    def test_dgeoflow_serialize_flox(self):
        # 1. Set up test model
        input_parser = DGeoflowParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dgeoflow/Berekening3"))
        test_output_filepath = (
                Path(TestUtils.get_output_test_data_dir("dgeoflow"))
                / "Berekening3_serialized.flox"
        )

        # 2. Verify initial expectations
        assert test_filepath.exists(), "Test .flox not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        ds = DGeoflowInputZipSerializer(ds=input_structure)
        ds.write(test_output_filepath)

    @pytest.mark.integrationtest
    def test_dgeoflow_serialize_folders(self):
        # 1. Set up test model
        input_parser = DGeoflowParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dgeoflow/Berekening3"))
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dgeoflow/serialized")
        )

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        ds = DGeoflowInputSerializer(ds=input_structure)
        ds.write(test_output_filepath)

    @pytest.mark.integrationtest
    def test_dgeoflow_parse_serialize_flox_model(self):
        dsm = DGeoflowModel()
        test_filepath = (
                Path(TestUtils.get_local_test_data_dir("dgeoflow"))
                / "Berekening3.flox"
        )
        test_output_filepath = (
                Path(TestUtils.get_output_test_data_dir("dgeoflow"))
                / "Berekening3_serialized.flox"
        )

        dsm.parse(test_filepath)

        assert dsm.datastructure.is_valid
        dsm.serialize(test_output_filepath)
        assert test_output_filepath.exists()
