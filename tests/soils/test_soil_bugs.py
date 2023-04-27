import pytest
from pydantic import ValidationError
from teamcity import is_running_under_teamcity

from geolib.models.dfoundations.dfoundations_model import DFoundationsModel
from geolib.soils import MohrCoulombParameters, Soil, SoilType


class TestNaNSoils:
    @pytest.mark.unittest
    def test_set_infinite_yields_error(self):
        soil = Soil()

        with pytest.raises(ValidationError):
            MohrCoulombParameters(cohesion=float("nan"))

        with pytest.raises(ValidationError):
            soil.mohr_coulomb_parameters.cohesion = "-inf"

        with pytest.raises(ValidationError):
            soil.mohr_coulomb_parameters.friction_angle = "nan"

        with pytest.raises(ValidationError):
            kwargs = {"cohesion": 5, "friction_angle": "inf"}
            soil = Soil(mohr_coulomb_parameters=kwargs)

    @pytest.mark.unittest
    def test_set_cu_is_optional(self):
        SOIL_PARAMETERS = [
            {
                "materiaal": "Onbekend materiaal",
                "unsat": 0.0,
                "sat": 0.0,
                "phi": 0.0,
                "soiltype": SoilType.GRAVEL,
            },
            {
                "materiaal": "Grond, fijn korrelig",
                "unsat": 18.0,
                "sat": 20.0,
                "phi": 25.0,
                "soiltype": SoilType.SAND,
            },
            {
                "materiaal": "Veen",
                "unsat": 12.0,
                "sat": 12.0,
                "phi": 15.0,
                "soiltype": SoilType.PEAT,
            },
            {
                "materiaal": "Klei, zwk siltig-siltig",
                "unsat": 15.0,
                "sat": 15.0,
                "phi": 20.0,
                "soiltype": SoilType.CLAY,
            },
            {
                "materiaal": "Klei, siltig/leem",
                "unsat": 16.5,
                "sat": 16.5,
                "phi": 25.0,
                "soiltype": SoilType.CLAY,
            },
            {
                "materiaal": "Zand, siltig tot leem",
                "unsat": 17.0,
                "sat": 19.0,
                "phi": 27.5,
                "soiltype": SoilType.SAND,
            },
            {
                "materiaal": "Zand, zwk siltig-siltig",
                "unsat": 18.0,
                "sat": 20.0,
                "phi": 30,
                "soiltype": SoilType.SAND,
            },
            {
                "materiaal": "Zand, zand tot grindig",
                "unsat": 18.0,
                "sat": 20.0,
                "phi": 32.5,
                "soiltype": SoilType.GRAVEL,
            },
            {
                "materiaal": "Zand, vastzand, kleiig",
                "unsat": 18.0,
                "sat": 20.0,
                "phi": 30.0,
                "soiltype": SoilType.SAND,
            },
            {
                "materiaal": "Grond, zeer stijf",
                "unsat": 18.0,
                "sat": 20.0,
                "phi": 30.0,
                "soiltype": SoilType.SAND,
            },
        ]

        model = DFoundationsModel()

        for soil in SOIL_PARAMETERS:
            soil_type = Soil()
            soil_type.name = soil["materiaal"]
            soil_type.soil_type_nl = soil["soiltype"]
            soil_type.mohr_coulomb_parameters.friction_angle = soil["phi"]
            soil_type.soil_weight_parameters.saturated_weight = soil["sat"]
            soil_type.soil_weight_parameters.unsaturated_weight = soil["unsat"]
            model.add_soil(soil_type)
            assert (
                model.soils[soil_type.name].soilcu == 0.00
            ), "Should have default Cu with 0"
