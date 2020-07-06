import pytest
from teamcity import is_running_under_teamcity
from tests.utils import TestUtils
from geolib.models import DSettlementModel
from pathlib import Path


class TestDSettlementRegressionSuite:

    input_testdata = TestUtils.get_test_files_from_local_test_dir(
        "dsettlement/benchmarks", "*.sld"
    )
    input_testdata_ids = [str(input_file.stem) for input_file in input_testdata]

    @pytest.mark.systemtest
    @pytest.mark.skipif(
        not is_running_under_teamcity(), reason="Regression tests take a long time."
    )
    @pytest.mark.parametrize("test_file", input_testdata, ids=input_testdata_ids)
    def test_parse_output_benchmarks_dsettlement(self, test_file):
        # 1. Set up test data
        filename = test_file.stem
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir("dsettlement/benchmarks")
        )
        output_test_file = output_test_folder / (filename + ".json")
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert test_file.exists(), f"Input test file was not found at {test_file}."

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))
