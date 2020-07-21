import os

import pytest

from geolib.models.base_model import BaseModel, BaseModelList
from geolib.models.base_model import MetaData
from geolib.models import DSettlementModel

from tests.utils import TestUtils, only_teamcity
from pathlib import Path
from teamcity import is_running_under_teamcity


class TestBaseModel:
    @pytest.fixture
    def default_base_model(self):
        return BaseModel()

    @pytest.mark.unittest
    def test_meta_init(self):
        # test loading from geolib.env
        m = MetaData()
        assert m.company == "Deltares"

    @pytest.mark.unittest
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_Model_initialize_createsfile_when_no_config_file_given(
        self, default_base_model
    ):
        # 1. Set initial test data.
        config_filename = None

        # 2. Define test action.
        try:
            inputfile_filename = default_base_model.initialize(
                config_file=config_filename
            )
        # 3. Verify final expectations.
        except Exception as e_info:
            pytest.fail("Exception thrown but not expected {}".format(e_info))
        assert inputfile_filename, "No filename was generated"
        assert os.path.exists(
            inputfile_filename
        ), "" + "No file was created at {}".format(inputfile_filename)

    @pytest.mark.unittest
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_Model_execute_timeout_after_giventime(self, default_base_model):
        # 1. Set initial test data.
        timeout = 2
        expected_error = "The execution timed out, a log can be seen in ..."

        # 2. Define test action.
        with pytest.raises(TimeoutError) as e_info:
            default_base_model.execute(timeout)

        # 3. Verify final expectations.
        error_message = str(e_info.value)
        assert error_message == expected_error, (
            ""
            + "Expected exception message {},".format(expected_error)
            + "retrieved {}".format(error_message)
        )

    @pytest.mark.acceptance
    @only_teamcity
    def test_basemodellist_execute(self):
        # Setup models
        a = DSettlementModel()
        b = DSettlementModel()
        input_folder = Path(TestUtils.get_local_test_data_dir("dsettlement"))
        benchmark_fn = input_folder / "bm1-1.sli"

        output_folder = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "multiple"
        )

        ml = BaseModelList(models=[a, b])
        for i, model in enumerate(ml.models):
            model.parse(benchmark_fn)

        # Execute
        output = ml.execute(output_folder, nprocesses=1)
        assert len(output.models) == 2
        for model in output.models:
            assert model.datastructure
