import pytest
import os
import shutil
from pathlib import Path

from teamcity import is_running_under_teamcity

from geolib.models import BaseModel
from geolib.models import BaseModelStructure

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import DStabilityStructure


from tests.utils import TestUtils


class TestDStabilityModel:
    @pytest.mark.unittest
    def test_instantiate_DStabilityModel(self):
        assert isinstance(DStabilityModel(inputfn=None), BaseModel), (
            "" + "DStabilityModel does not instanciate BaseModel"
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filepath", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_given_datadir_when_parse_then_datastructure_of_expected_type(
        self, filepath: str
    ):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(filepath))
        dstability_model = DStabilityModel(inputfn=None)

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        # 4. Verify final expectations.
        assert dstability_model.is_valid
        assert isinstance(dstability_model.datastructure, DStabilityStructure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure"),],
    )
    def test_given_data_when_parseandserialize_then_doesnotraise(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(inputfn=None)
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dstability\\parseandserialize")
        )

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        if len(os.listdir(test_output_filepath)) > 0:
            shutil.rmtree(test_output_filepath)
            os.mkdir(test_output_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        dstability_model.serialize(test_output_filepath)

        # 4. Verify final expectations.
        assert dstability_model.is_valid
        assert len(os.listdir(test_output_filepath)) > 0, (
            "" + "No data was generated while serializing."
        )

    @pytest.mark.systemtest
    @pytest.mark.skipif(
        not is_running_under_teamcity(), reason="Console test only installed on TC."
    )
    def test_execute_model_succesfully(self):
        # 1. Set up test data.
        dm = DStabilityModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
        dm.parse(test_filepath)

        test_output_filepath = Path(TestUtils.get_output_test_data_dir("test"))
        dm.serialize(test_output_filepath)

        # 2. Verify initial expectations.
        assert os.path.exists(test_output_filepath)

        # 3. Run test.
        dm.input_fn = test_output_filepath
        status = dm.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0
