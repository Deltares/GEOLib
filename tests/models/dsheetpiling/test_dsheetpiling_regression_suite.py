from pathlib import Path

import pytest
from geolib.models import DSheetPilingModel

from tests.utils import TestUtils, only_teamcity

benchmark_directory = "dsheetpiling/benchmarks"
complex_projects_directory = "dsheetpiling/complex_projects"
tutorials_directory = "dsheetpiling/tutorials"
dump_file_extension_filter = "*.shd"
output_test_file_extension = ".json"


class TestDSheetPilingRegressionSuite:
    input_benchmark_testdata = TestUtils.get_test_files_from_local_test_dir(
        benchmark_directory, dump_file_extension_filter
    )
    input_benchmark_testdata_ids = [
        str(input_file.stem) for input_file in input_benchmark_testdata
    ]

    input_complex_projects_testdata = TestUtils.get_test_files_from_local_test_dir(
        complex_projects_directory, dump_file_extension_filter
    )
    input_complex_projects_testdata_ids = [
        str(input_file.stem) for input_file in input_complex_projects_testdata
    ]

    input_tutorials_testdata = TestUtils.get_test_files_from_local_test_dir(
        tutorials_directory, dump_file_extension_filter
    )
    input_tutorials_testdata_ids = [
        str(input_file.stem) for input_file in input_tutorials_testdata
    ]

    @pytest.mark.systemtest
    @only_teamcity
    @pytest.mark.parametrize(
        "test_file",
        input_benchmark_testdata,
        ids=input_benchmark_testdata_ids,
    )
    def test_parse_output_benchmarks_dsheetpiling(self, test_file: Path):
        # 1. Set up test data
        filename = test_file.stem
        output_test_folder = Path(TestUtils.get_output_test_data_dir(benchmark_directory))
        output_test_file = output_test_folder / (filename + output_test_file_extension)
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.model_dump_json(indent=4))

    @pytest.mark.systemtest
    @only_teamcity
    @pytest.mark.parametrize(
        "test_file",
        input_complex_projects_testdata,
        ids=input_complex_projects_testdata_ids,
    )
    def test_parse_output_complex_projects_dsheetpiling(self, test_file: Path):
        # 1. Set up test data
        filename = test_file.stem
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir(complex_projects_directory)
        )
        output_test_file = output_test_folder / (filename + output_test_file_extension)
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.model_dump_json(indent=4))

    @pytest.mark.systemtest
    @only_teamcity
    @pytest.mark.parametrize(
        "test_file",
        input_tutorials_testdata,
        ids=input_tutorials_testdata_ids,
    )
    def test_parse_output_tutorials_dsheetpiling(self, test_file: Path):
        # 1. Set up test data
        filename = test_file.stem
        output_test_folder = Path(TestUtils.get_output_test_data_dir(tutorials_directory))
        output_test_file = output_test_folder / (filename + output_test_file_extension)
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.model_dump_json(indent=4))
