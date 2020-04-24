import os

import pytest

from geolib.models.base_model import BaseModel
from geolib.models.base_model import MetaData

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
