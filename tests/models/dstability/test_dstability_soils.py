import pytest

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import MohrCoulombParameters, ShearStrengthModelTypePhreaticLevel, Soil


class TestDStabilitySoil:
    @pytest.mark.unittest
    def test_dstability_add_soil(self):
        dstability_model = DStabilityModel(filename=None)
        soil_1 = Soil(name="Test", code="Test")

        dstability_model.add_soil(soil_1)
        assert dstability_model.soils.has_soil_code("Test") is True

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
            dstability_model.datastructure.soils.get_global_soil(
                "Test1"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB.value
        )
        assert (
            dstability_model.datastructure.soils.get_global_soil(
                "Test1"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.SHANSEP.value
        )

        # assert changed values
        assert (
            dstability_model.datastructure.soils.get_global_soil(
                "Test2"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.MOHR_COULOMB.value
        )
        assert (
            dstability_model.datastructure.soils.get_global_soil(
                "Test2"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.SHANSEP.value
        )

        # assert changed values
        assert (
            dstability_model.datastructure.soils.get_global_soil(
                "Test3"
            ).shear_strength_model_below_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.NONE.value
        )
        assert (
            dstability_model.datastructure.soils.get_global_soil(
                "Test3"
            ).shear_strength_model_above_phreatic_level.value
            == ShearStrengthModelTypePhreaticLevel.NONE.value
        )

    def test_dstability_get_soil(self):
        dstability_model = DStabilityModel(filename=None)
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=1.0, friction_angle=20)
        soil_1 = Soil(
            name="TestName", code="Test", mohr_coulomb_parameters=mohr_coulomb_parameters
        )

        dstability_model.add_soil(soil_1)

        soil = dstability_model.soils.get_soil("Test")

        assert soil.Id == soil_1.id
        assert soil.Name == soil_1.name
        assert soil.Code == soil_1.code
        assert (
            soil.MohrCoulombAdvancedShearStrengthModel.Cohesion
            == soil_1.mohr_coulomb_parameters.cohesion.mean
        )
        assert (
            soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle
            == soil_1.mohr_coulomb_parameters.friction_angle.mean
        )

    def test_dstability_get_soil_and_edit(self):
        dstability_model = DStabilityModel(filename=None)
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=1.0, friction_angle=20)
        soil_1 = Soil(
            name="TestName", code="Test", mohr_coulomb_parameters=mohr_coulomb_parameters
        )

        dstability_model.add_soil(soil_1)

        soil = dstability_model.soils.get_soil("Test")

        assert soil.Id == soil_1.id
        assert soil.Name == soil_1.name
        assert soil.Code == soil_1.code
        assert (
            soil.MohrCoulombAdvancedShearStrengthModel.Cohesion
            == soil_1.mohr_coulomb_parameters.cohesion.mean
        )
        assert (
            soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngle
            == soil_1.mohr_coulomb_parameters.friction_angle.mean
        )

        soil.MohrCoulombAdvancedShearStrengthModel.Cohesion = 99.0
        soil.SuShearStrengthModel.ShearStrengthRatio = 13.0

        soil = dstability_model.soils.get_soil("Test")
        assert soil.MohrCoulombAdvancedShearStrengthModel.Cohesion == 99.0
        assert soil.SuShearStrengthModel.ShearStrengthRatio == 13.0

    def test_dstability_get_global_soil(self):
        dstability_model = DStabilityModel(filename=None)
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=1.0, friction_angle=20)
        soil_1 = Soil(
            name="TestName", code="Test", mohr_coulomb_parameters=mohr_coulomb_parameters
        )
        dstability_model.add_soil(soil_1)

        global_soil = dstability_model.soils.get_global_soil("Test")

        assert global_soil.id == soil_1.id
        assert global_soil.name == soil_1.name
        assert global_soil.code == soil_1.code
        assert (
            global_soil.mohr_coulomb_parameters.cohesion
            == soil_1.mohr_coulomb_parameters.cohesion
        )
        assert (
            global_soil.mohr_coulomb_parameters.friction_angle
            == soil_1.mohr_coulomb_parameters.friction_angle
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
