import pytest
from pathlib import Path
from geolib.models import BaseModel
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import DStabilityOutputStructure


from tests.utils import TestUtils


class TestDstabilityModel:
    @pytest.mark.unittest
    def test_DStabilityModel_instance(self):
        dstability_model = DStabilityModel(inputfn=None)
        assert dstability_model is not None
        assert isinstance(dstability_model, BaseModel), (
            "" + "DStabilityModel does not instanciate BaseModel"
        )

        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
        dstability_model.parse(test_filepath)
        assert dstability_model.is_valid
        dstability_model.serialize(Path("test"))

        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/example_1/results")
        )
        dstability_model.parse(test_filepath)
        assert isinstance(dstability_model.datastructure, DStabilityOutputStructure)
