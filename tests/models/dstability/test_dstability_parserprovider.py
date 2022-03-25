import os
from pathlib import Path

import pytest

from geolib.models import BaseModel
from geolib.models.dstability import DStabilityModel
from geolib.models.dstability.dstability_parserprovider import (
    DStabilityParser,
    DStabilityParserProvider,
    DStabilityZipParser,
)
from geolib.models.dstability.serializer import (
    DStabilityInputSerializer,
    DStabilityInputZipSerializer,
)
from tests.utils import TestUtils


class TestDStabilityInputParser:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dstability/example_1", id="Input Structure"),
            pytest.param("dstability/Tutorial_v20_2_1", id="Tutorial DStability 20.2.1"),
        ],
    )
    def test_dstability_parse_directory(self, dir_path: str):
        # 1. Set up test model
        input_parser = DStabilityParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dstability/serialized")
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
    def test_dstability_parse_stix(self):
        # 1. Set up test model
        input_parser = DStabilityZipParser()
        test_filepath = (
            Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
            / "Tutorial.stix"
        )
        test_output_dir = Path(
            TestUtils.get_output_test_data_dir("dstability/serialized")
        )
        # 2. Verify initial expectations
        assert test_filepath.exists(), "Test .stix not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        assert input_structure is not None
        data = input_structure.json(indent=4)
        with open(test_output_dir / "dstability_parsed_input_stix.json", "w") as io:
            io.write(data)

    @pytest.mark.integrationtest
    def test_dstability_serialize_stix(self):
        # 1. Set up test model
        input_parser = DStabilityParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dstability"))
            / "Tutorial_serialized.stix"
        )

        # 2. Verify initial expectations
        assert test_filepath.exists(), "Test .stix not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        ds = DStabilityInputZipSerializer(ds=input_structure)
        ds.write(test_output_filepath)

    @pytest.mark.integrationtest
    def test_dstability_serialize_folders(self):
        # 1. Set up test model
        input_parser = DStabilityParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dstability/serialized")
        )

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        ds = DStabilityInputSerializer(ds=input_structure)
        ds.write(test_output_filepath)

    @pytest.mark.integrationtest
    def test_dstability_parse_serialize_stix_model(self):
        dsm = DStabilityModel()
        test_filepath = (
            Path(TestUtils.get_local_test_data_dir("dstability"))
            / "Tutorial_v20_2_1.stix"
        )
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dstability"))
            / "Tutorial_serialized_directly.stix"
        )

        dsm.parse(test_filepath)
        assert (
            len(dsm.datastructure.stages) > 1
        ), "Didn't correctly parse multiple stages."
        assert dsm.datastructure.is_valid
        dsm.serialize(test_output_filepath)
        assert test_output_filepath.exists()
