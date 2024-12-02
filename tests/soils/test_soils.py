import pytest
from pydantic_core._pydantic_core import ValidationError

from geolib.soils import (
    MohrCoulombParameters,
    Soil,
    SoilClassificationParameters,
    StochasticParameter,
)


class TestSoils:
    @pytest.mark.unittest
    def test_set_stochastic_parameters_from_float(self):
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=2)
        soil = Soil(mohr_coulomb_parameters=mohr_coulomb_parameters)
        soil.set_stochastic_parameters(soil.mohr_coulomb_parameters)

        assert isinstance(soil.mohr_coulomb_parameters.cohesion, StochasticParameter)
        assert soil.mohr_coulomb_parameters.cohesion.mean == 2
        assert soil.mohr_coulomb_parameters.cohesion.standard_deviation == 0

    @pytest.mark.unittest
    def test_set_stochastic_parameters_from_stochastic_parameter(self):
        mohr_coulomb_parameters = MohrCoulombParameters()

        mohr_coulomb_parameters.cohesion.mean = 2
        mohr_coulomb_parameters.cohesion.standard_deviation = 1
        soil = Soil(mohr_coulomb_parameters=mohr_coulomb_parameters)

        soil.set_stochastic_parameters(mohr_coulomb_parameters)

        assert isinstance(soil.mohr_coulomb_parameters.cohesion, StochasticParameter)
        assert soil.mohr_coulomb_parameters.cohesion.mean == 2
        assert soil.mohr_coulomb_parameters.cohesion.standard_deviation == 1

    @pytest.mark.unittest
    def test_set_all_stochastic_parameters(self):
        mohr_coulomb_parameters = MohrCoulombParameters(cohesion=2, friction_angle=30)
        soil_classification_parameters = SoilClassificationParameters(min_void_ratio=0.3)
        soil = Soil(
            mohr_coulomb_parameters=mohr_coulomb_parameters,
            soil_classification_parameters=soil_classification_parameters,
        )

        soil.set_all_stochastic_parameters()
        assert isinstance(soil.mohr_coulomb_parameters.cohesion, StochasticParameter)
        assert isinstance(
            soil.mohr_coulomb_parameters.friction_angle, StochasticParameter
        )
        assert isinstance(soil.soil_classification_parameters.min_void_ratio, float)

    @pytest.mark.unittest
    def test_error_raised_when_value_not_part_of_soil(self):
        with pytest.raises(ValidationError):
            Soil(wrong_name="Peat")
