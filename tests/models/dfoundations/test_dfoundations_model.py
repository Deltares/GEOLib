import logging
import os
from pathlib import Path
from typing import Type

import pytest
from teamcity import is_running_under_teamcity

from geolib.models import BaseModel
from geolib.models.dfoundations.dfoundation_model import DFoundationsModel
from geolib.models.dfoundations.internal import (
    DFoundationsDumpStructure,
    DFoundationsStructure,
)
from tests.utils import TestUtils, only_teamcity


class TestDfoundationsModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DFoundationsModel_instance(self):
        dfoundation_model = DFoundationsModel()
        assert dfoundation_model is not None
        assert isinstance(dfoundation_model, BaseModel), (
            "" + "DFoundationsModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename,structure",
        [
            pytest.param(Path("bm1-1a.foi"), DFoundationsStructure, id="Input file"),
            pytest.param(Path("bm1-1a.fod"), DFoundationsDumpStructure, id="Output file"),
        ],
    )
    def test_given_filepath_when_parse_then_does_not_raise(
        self, filename: Path, structure: Type
    ):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / filename
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.is_file()

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert isinstance(ds.datastructure, structure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1a.foi"), id="Input file")],
    )
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / filename
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / filename
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.is_file()
        if output_test_file.is_file():
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DFoundationsStructure)
        input_datastructure = dict(ds.datastructure.input_data)

        # 4.2. Read the generated data.
        assert output_test_file.is_file()
        output_datastructure = dict(
            DFoundationsModel().parse(output_test_file).input_data
        )
        assert not (
            input_datastructure is output_datastructure
        ), "Both references are the same."

        # 4.3. Compare values
        output_keys = output_datastructure.keys()
        errors = []
        for ds_key, ds_value in input_datastructure.items():
            if not (ds_key in output_keys):
                errors.append(f"Key {ds_key} not serialized!")
                continue
            if not (ds_value == output_datastructure[ds_key]):
                logging.warning(f"UNEQUAL: {ds_value} != {output_datastructure[ds_key]}")
                errors.append(f"Values for key {ds_key} differ from parsed to serialized")
        if errors:
            print(errors)
            pytest.fail(f"Failed with the following {errors}")

    @pytest.mark.systemtest
    @only_teamcity
    def test_execute_console_successfully(self):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test.foi"

        df.parse(test_file)
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert output_test_file.is_file()

        # 3. Run test.
        df.filename = output_test_file
        status = df.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0

    @pytest.mark.unittest
    def test_execute_console_without_filename_raises_exception(self):
        # 1. Set up test data.
        df = DFoundationsModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.acceptance
    @pytest.mark.xfail(reason="Can't work yet.")
    @only_teamcity
    def test_run_model_from_scratch(self):
        # 1. Set up test data.
        df = DFoundationsModel()
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "acceptance_from_scratch.foi"

        # Setup from scratch data here
        # add soils
        # add geometry
        # etc

        # 2. Verify initial expectations.
        df.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        df.filename = output_test_file
        status = df.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0
