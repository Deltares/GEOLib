import pytest

from geolib.models.model_dataclasses import Position


class TestPosition:
    @pytest.mark.unittest
    def test_verify_default_parameters(self):
        position = Position("dummy")
        assert position is not None
        assert position.lon == 0.0
        assert position.lat == 0.0
