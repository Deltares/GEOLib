import pytest

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import MohrCoulombParameters, ShearStrengthModelTypePhreaticLevel, Soil


class TestDStabilitySoil:
    @pytest.mark.unittest
    def test_dstability_add_soil(self):
        dstability_model = DStabilityModel(filename=None)
        soil_1 = Soil(name="Test", code="Test")

        dstability_model.add_soil(soil_1)
        assert dstability_model.soils.has_soilcode("Test") is True

        with pytest.raises(ValueError) as _:
            soil_2 = Soil(name="AnotherTest", code="Test")
            dstability_model.add_soil(soil_2)

    def test_dstability_add_soil_with_shear_strength_model_type(self):
        dstability_model = DStabilityModel(filename=None)

        # Create soils
        soil_1 = Soil(name="Test1", code="Test1")

        soil_2 = Soil(name="Test2", code="Test2")
        soil_2.shear_strength_model_below_phreatic_level = (
            ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB
        )
        soil_2.shear_strength_model_above_phreatic_level = (
            ShearStrengthModelTypePhreaticLevel.SHANSEP
        )

        soil_3 = Soil(name="Test3", code="Test3")
        soil_3.shear_strength_model_below_phreatic_level = (
            ShearStrengthModelTypePhreaticLevel.NONE
        )
        soil_3.shear_strength_model_above_phreatic_level = (
            ShearStrengthModelTypePhreaticLevel.NONE
        )

        # Add soils
        dstability_model.add_soil(soil_1)
        dstability_model.add_soil(soil_2)
        dstability_model.add_soil(soil_3)

        # assert defaults
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test1"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB.value
        )
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test1"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.SHANSEP.value
        )

        # assert changed values
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test2"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB.value
        )
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test2"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.SHANSEP.value
        )

        # assert changed values
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test3"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.NONE.value
        )
        assert (
            dstability_model.datastructure.soils.get_soil(
                "Test3"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.NONE.value
        )

    def test_dstability_edit_soil(self):
        dstability_model = DStabilityModel(filename=None)
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=1.0)
        soil_1 = Soil(
            name="Test", code="Test", mohr_coulomb_parameters=mohr_coulomb_parameters
        )
        code = dstability_model.add_soil(soil_1)

        dstability_model.edit_soil(code=code, cohesion=2.0, friction_angle=35)
        assert pytest.approx(
            dstability_model.soils.get_soil("Test").mohr_coulomb_parameters.cohesion.mean,
            2.0,
        )

    def test_has_10_default_soils(self):
        dstability_model = DStabilityModel(filename=None)
        assert len(dstability_model.soils.Soils) == 10

    def test_has_default_soil_codes(self):
        dstability_model = DStabilityModel(filename=None)
        expected_soilcodes = {
            "H_Aa_ht_new",
            "H_Aa_ht_old",
            "H_Rk_k_shallow",
            "H_Rk_k_deep",
            "H_Rk_ko",
            "H_vhv_v",
            "H_vbv_v",
            "P_Rk_k&s",
            "Sand",
            "H_Ro_z&k",
        }
        default_soilcodes = {soil.Code for soil in dstability_model.soils.Soils}
        assert expected_soilcodes == default_soilcodes
