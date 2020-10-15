import pytest
from teamcity import is_running_under_teamcity
from geolib.soils import (
    Soil,
    MohrCoulombParameters,
)
from pydantic import ValidationError


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
