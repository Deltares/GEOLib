import pytest

from geolib.models import models


class TestPosition:

    @pytest.mark.unittest
    def test_verify_default_parameters(self):
        position = models.Position('dummy')
        assert position is not None
        assert position.lon == 0.0
        assert position.lat == 0.0


class TestModel:

    @pytest.mark.unittest
    def test_instantiate_model_without_inputfn_doesnot_raise(self):
        try:
            model = models.Model(inputfn=None)
        except Exception as e_info:
            pytest.fail('Exception thrown but not expected {}', str(e_info))
        assert model is not None

    @pytest.mark.unittest
    def test_Model_parse_creates_new_instance(self):
        model = None
        try:
            model = models.Model.parse(None)
        except Exception as e_info:
            pytest.fail('Exception thrown but not expected {}', str(e_info))
        assert model is not None

