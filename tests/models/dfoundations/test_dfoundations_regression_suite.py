import pytest
from teamcity import is_running_under_teamcity
from tests.utils import TestUtils
from geolib.models import DFoundationsModel
from pathlib import Path


class TestRegressionSuite:
    @pytest.mark.systemtest
    # @pytest.mark.skipif(
    # not is_running_under_teamcity(), reason="Regression tests take a long time."
    # )
    @pytest.mark.parametrize(
        "filename",
        [
            pytest.param("bm1-10", id="bm1-10 shd file."),
            pytest.param("bm1-11a", id="bm1-11a shd file."),
            pytest.param("bm1-11b", id="bm1-11b shd file."),
            pytest.param("bm1-11c", id="bm1-11c shd file."),
            pytest.param("bm1-11d", id="bm1-11d shd file."),
            pytest.param("bm1-11e", id="bm1-11e shd file."),
            pytest.param("bm1-11f", id="bm1-11f shd file."),
            pytest.param("bm1-11g", id="bm1-11g shd file."),
            pytest.param("bm1-12a", id="bm1-12a shd file."),
            pytest.param("bm1-12b", id="bm1-12b shd file."),
            pytest.param("bm1-12c", id="bm1-12c shd file."),
            pytest.param("bm1-12d", id="bm1-12d shd file."),
            pytest.param("bm1-12e", id="bm1-12e shd file."),
            pytest.param("bm1-12f", id="bm1-12f shd file."),
            pytest.param("bm1-12g", id="bm1-12g shd file."),
            pytest.param("bm1-13", id="bm1-13 shd file."),
            pytest.param("bm1-14a", id="bm1-14a shd file."),
            pytest.param("bm1-14b", id="bm1-14b shd file."),
            pytest.param("bm1-15a", id="bm1-15a shd file."),
            pytest.param("bm1-15b", id="bm1-15b shd file."),
            pytest.param("bm1-15c", id="bm1-15c shd file."),
            pytest.param("bm1-15d", id="bm1-15d shd file."),
            pytest.param("bm1-15e", id="bm1-15e shd file."),
            pytest.param("bm1-15f", id="bm1-15f shd file."),
            pytest.param("bm1-15g", id="bm1-15g shd file."),
            pytest.param("bm1-16", id="bm1-16 shd file."),
            pytest.param("bm1-17a", id="bm1-17a shd file."),
            pytest.param("bm1-17b", id="bm1-17b shd file."),
            pytest.param("bm1-18a", id="bm1-18a shd file."),
            pytest.param("bm1-18b", id="bm1-18b shd file."),
            pytest.param("bm1-18c", id="bm1-18c shd file."),
            pytest.param("bm1-18d", id="bm1-18d shd file."),
            pytest.param("bm1-18e", id="bm1-18e shd file."),
            pytest.param("bm1-18f", id="bm1-18f shd file."),
            pytest.param("bm1-18g", id="bm1-18g shd file."),
            pytest.param("bm1-18h", id="bm1-18h shd file."),
            pytest.param("bm1-19a", id="bm1-19a shd file."),
            pytest.param("bm1-19b", id="bm1-19b shd file."),
            pytest.param("bm1-1b", id="bm1-1b shd file."),
            pytest.param("bm1-20a", id="bm1-20a shd file."),
            pytest.param("bm1-20b", id="bm1-20b shd file."),
            pytest.param("bm1-20c", id="bm1-20c shd file."),
            pytest.param("bm1-20d", id="bm1-20d shd file."),
            pytest.param("bm1-20e", id="bm1-20e shd file."),
            pytest.param("bm1-20f", id="bm1-20f shd file."),
            pytest.param("bm1-20g", id="bm1-20g shd file."),
            pytest.param("bm1-20h", id="bm1-20h shd file."),
            pytest.param("bm1-20i", id="bm1-20i shd file."),
            pytest.param("bm1-20j", id="bm1-20j shd file."),
            pytest.param("bm1-21", id="bm1-21 shd file."),
            pytest.param("bm1-2a", id="bm1-2a shd file."),
            pytest.param("bm1-2b", id="bm1-2b shd file."),
            pytest.param("bm1-3a", id="bm1-3a shd file."),
            pytest.param("bm1-3b", id="bm1-3b shd file."),
            pytest.param("bm1-4a", id="bm1-4a shd file."),
            pytest.param("bm1-4b", id="bm1-4b shd file."),
            pytest.param("bm1-5a", id="bm1-5a shd file."),
            pytest.param("bm1-5b", id="bm1-5b shd file."),
            pytest.param("bm1-6a", id="bm1-6a shd file."),
            pytest.param("bm1-6b", id="bm1-6b shd file."),
            pytest.param("bm1-7", id="bm1-7 shd file."),
            pytest.param("bm1-8", id="bm1-8 shd file."),
            pytest.param("bm1-9", id="bm1-9 shd file."),
            pytest.param("bm2-1", id="bm2-1 shd file."),
            pytest.param("bm2-2", id="bm2-2 shd file."),
            pytest.param("bm2-3", id="bm2-3 shd file."),
            pytest.param("bm2-4", id="bm2-4 shd file."),
            pytest.param("bm2-5", id="bm2-5 shd file."),
            pytest.param("bm2-6", id="bm2-6 shd file."),
            pytest.param("bm2-7a", id="bm2-7a shd file."),
            pytest.param("bm2-7b", id="bm2-7b shd file."),
            pytest.param("bm2-7c", id="bm2-7c shd file."),
            pytest.param("bm3-1", id="bm3-1 shd file."),
            pytest.param("bm3-2", id="bm3-2 shd file."),
            pytest.param("bm3-3a", id="bm3-3a shd file."),
            pytest.param("bm3-3b", id="bm3-3b shd file."),
            pytest.param("bm3-3c", id="bm3-3c shd file."),
            pytest.param("bm3-4", id="bm3-4 shd file."),
            pytest.param("bm3-5", id="bm3-5 shd file."),
            pytest.param("bm3-6", id="bm3-6 shd file."),
            pytest.param("bm3-7a", id="bm3-7a shd file."),
            pytest.param("bm3-7b", id="bm3-7b shd file."),
            pytest.param("bm3-8a", id="bm3-8a shd file."),
            pytest.param("bm3-8b", id="bm3-8b shd file."),
            pytest.param("bm4-1", id="bm4-1 shd file."),
            pytest.param("bm4-10", id="bm4-10 shd file."),
            pytest.param("bm4-11a", id="bm4-11a shd file."),
            pytest.param("bm4-11b", id="bm4-11b shd file."),
            pytest.param("bm4-12", id="bm4-12 shd file."),
            pytest.param("bm4-2", id="bm4-2 shd file."),
            pytest.param("bm4-3", id="bm4-3 shd file."),
            pytest.param("bm4-4", id="bm4-4 shd file."),
            pytest.param("bm4-5", id="bm4-5 shd file."),
            pytest.param("bm4-6", id="bm4-6 shd file."),
            pytest.param("bm4-7", id="bm4-7 shd file."),
            pytest.param("bm4-8", id="bm4-8 shd file."),
            pytest.param("bm4-9", id="bm4-9 shd file."),
        ],
    )
    def test_parse_output_benchmarks(self, filename):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations/benchmarks"))
        test_file = test_folder / (filename + ".fod")
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir("dfoundations/benchmarks")
        )
        output_test_file = output_test_folder / (filename + ".json")
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))
