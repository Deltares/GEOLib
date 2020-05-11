import logging
import os
from pathlib import Path
from typing import Type

import pytest
from teamcity import is_running_under_teamcity

from geolib.models import BaseModel
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetpilingModel
from geolib.models.dsheetpiling.internal import (
    DSheetPilingInputStructure,
    DSheetPilingOutputStructure,
)
from tests.utils import TestUtils, only_teamcity


class TestDsheetpilingModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSheetpilingModel_instance(self):
        dsheetpiling_model = DSheetpilingModel()
        assert dsheetpiling_model is not None
        assert isinstance(dsheetpiling_model, BaseModel), (
            "" + "DSheetpilingModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename,structure",
        [
            pytest.param(Path("bm1-1.shi"), DSheetPilingInputStructure, id="Input file"),
            pytest.param(
                Path("bm1-1.shd"), DSheetPilingOutputStructure, id="Output file"
            ),
        ],
    )
    def test_given_filepath_when_parse_then_does_not_raise(
        self, filename: Path, structure: Type
    ):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / filename
        ds = DSheetpilingModel()

        # 2. Verify initial expectations
        assert test_file.is_file()

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert isinstance(ds.datastructure, structure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1.shi"), id="Input file")],
    )
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / filename
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / filename
        ds = DSheetpilingModel()

        # 2. Verify initial expectations
        assert test_file.is_file()
        if output_test_file.is_file():
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DSheetPilingInputStructure)
        input_datastructure = dict(ds.datastructure)

        # 4.2. Read the generated data.
        assert output_test_file.is_file()
        output_datastructure = dict(DSheetpilingModel().parse(output_test_file))
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
        df = DSheetpilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / "bm1-1.shi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / "test.shi"

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
        df = DSheetpilingModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.xfail(reason="Can't work yet.")
    def test_run_model_from_scratch(self):
        # 1. Set up test data.
        df = DSheetpilingModel()
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / "acceptance_from_scratch.shi"

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
