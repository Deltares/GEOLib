from pathlib import Path

import pytest
from geolib.models import DSheetPilingModel
from teamcity import is_running_under_teamcity
from tests.utils import TestUtils, only_teamcity

benchmark_directory = "dsheetpiling/benchmarks"
complex_projects_directory = "dsheetpiling/complex_projects"
tutorials_directory = "dsheetpiling/tutorials"


class TestDSheetPilingRegressionSuite:
    input_benchmark_testdata = TestUtils.get_test_files_from_local_test_dir(
        benchmark_directory, "*.shd"
    )
    input_benchmark_testdata_ids = [str(input_file.stem) for input_file in input_benchmark_testdata]

    input_complex_projects_testdata = TestUtils.get_test_files_from_local_test_dir(
        complex_projects_directory, "*.shd"
    )
    input_complex_projects_testdata_ids = [str(input_file.stem) for input_file in input_complex_projects_testdata]

    input_tutorials_testdata = TestUtils.get_test_files_from_local_test_dir(
        tutorials_directory, "*.shd"
    )
    input_tutorials_testdata_ids = [str(input_file.stem) for input_file in input_tutorials_testdata]

    # @pytest.mark.parametrize(
    #     "test_file",
    #     input_testdata,
    #     ids=input_testdata_ids,
    # )
    # def test_generate_output_benchmarks_dsheetpiling(self, test_file: Path):
    #     # 1. Set up test data.
    #     df = DSheetPilingModel()
    #     input_file = test_file.with_suffix(".shi")

    #     # 2. Verify initial expectations.
    #     assert input_file.is_file()

    #     # 3. Run test.
    #     df.parse(input_file)
    #     df.execute()

    #     # 3. Verify return code of 0 (indicates successful run)
    #     assert df.datastructure
    #     assert test_file.is_file()

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
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir(benchmark_directory)
        )
        output_test_file = output_test_folder / (filename + ".json")
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))

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
        output_test_file = output_test_folder / (filename + ".json")
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))

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
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir(tutorials_directory)
        )
        output_test_file = output_test_folder / (filename + ".json")
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))
