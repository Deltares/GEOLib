import pytest
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import Soil


class TestDStabilitySoil:
    @pytest.mark.unittest
    def test_dstability_add_soil(self):
        dstability_model = DStabilityModel(inputfn=None)
        soil_1 = Soil(name="Test", code="Test")

        dstability_model.add_soil(soil_1)
        assert dstability_model.soils.has_soilcode("Test") is True

        with pytest.raises(ValueError) as _:
            soil_2 = Soil(name="AnotherTest", code="Test")
            dstability_model.add_soil(soil_2)

    @pytest.mark.unittest
    def test_dstability_remove_soil(self):
        dstability_model = DStabilityModel(inputfn=None)
        soil_1 = Soil(name="Test", code="Test")
        soil_1_id = dstability_model.add_soil(soil_1)
        dstability_model.remove_soil(soil_1_id)
        assert dstability_model.soils.has_soilcode("Test") is False

    def test_dstability_edit_soil(self):
        dstability_model = DStabilityModel(inputfn=None)
        soil_1 = Soil(name="Test", code="Test", cohesion=1.0)
        soil_1_id = dstability_model.add_soil(soil_1)
        dstability_model.edit_soil(soil_1_id, cohesion=2.0, friction_angle=35)
        assert pytest.approx(dstability_model.soils.get_soil(soil_1_id).cohesion, 2.0)
