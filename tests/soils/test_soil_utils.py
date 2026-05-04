import pytest

from geolib.soils.soil_utils import Color


class TestSoilsUtils:
    @pytest.mark.parametrize("color", [Color("green"), Color("red")])
    def test_conversion(self, color):
        internal_color = color.to_internal()
        newcolor = Color.from_internal(internal_color)
        assert newcolor.as_rgb_tuple() == color.as_rgb_tuple()
