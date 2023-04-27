from pathlib import Path

import pytest
from teamcity import is_running_under_teamcity

from geolib.models import DFoundationsModel
from tests.utils import TestUtils, only_teamcity

test_file_directory = "dfoundations/benchmarks"


class TestRegressionSuite:
    input_testdata = TestUtils.get_test_files_from_local_test_dir(
        test_file_directory, "*.fod"
    )
    input_testdata_ids = [str(input_file.stem) for input_file in input_testdata]

    @pytest.mark.systemtest
    @only_teamcity
    @pytest.mark.parametrize("test_file", input_testdata, ids=input_testdata_ids)
    def test_parse_output_benchmarks(self, test_file: Path):
        # 1. Set up test data
        filename = test_file.stem
        output_test_folder = Path(TestUtils.get_output_test_data_dir(test_file_directory))
        output_test_file = output_test_folder / (filename + ".json")
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))

    @pytest.mark.unittest
    def test_regression_issue8(self):
        test_folder = Path(TestUtils.get_local_test_data_dir(test_file_directory))
        test_file = test_folder / "bm1-1a.fod"
        ds = DFoundationsModel()
        ds.parse(test_file)
