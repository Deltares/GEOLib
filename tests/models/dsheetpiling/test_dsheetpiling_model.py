import pytest

from geolib.models import BaseModel
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetpilingModel


class TestDsheetpilingModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSheetpilingModel_instance(self):
        dsheetpiling_model = DSheetpilingModel()
        assert dsheetpiling_model is not None
        assert isinstance(dsheetpiling_model, BaseModel), (
            "" + "DSheetpilingModel does not instanciate BaseModel"
        )
