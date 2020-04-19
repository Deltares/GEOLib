import pytest

from geolib.models import BaseModel
from geolib.models.dfoundations.dfoundation_model import DFoundationsModel


class TestDfoundationsModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DFoundationsModel_instance(self):
        dfoundation_model = DFoundationsModel()
        assert dfoundation_model is not None
        assert isinstance(dfoundation_model, BaseModel), (
            "" + "DFoundationsModel does not instanciate BaseModel"
        )
