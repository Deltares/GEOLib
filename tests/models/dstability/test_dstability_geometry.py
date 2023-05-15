import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from geolib.geometry import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import Soil
from tests.utils import TestUtils


class TestDStabilityGeometry:
    @pytest.mark.unittest
    def test_dstability_add_layer_without_soil_raises(self):
        dstability_model = DStabilityModel()
        points = [
            Point(x=-20.0, z=2.0),
            Point(x=50.0, z=2.0),
            Point(x=50.0, z=-5.0),
            Point(x=-20.0, z=-5.0),
        ]

        with pytest.raises(ValueError):
            _ = dstability_model.add_layer(points=points, soil_code="Peat")

    @pytest.mark.unittest
    def test_dstability_add_layer_with_soil(self):
        dstability_model = DStabilityModel()
        points = [
            Point(x=-20.0, z=2.0),
            Point(x=50.0, z=2.0),
            Point(x=50.0, z=-5.0),
            Point(x=-20.0, z=-5.0),
        ]

        _ = dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=points, soil_code="Peat")
        assert len(dstability_model.datastructure.soillayers[0].SoilLayers) == 1

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "file_path", [pytest.param("dstability/example_1.stix", id="Input Structure")]
    )
    def test_given_data_contains_num_soillayers(self, file_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(file_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        assert len(dstability_model.datastructure.soillayers[0].SoilLayers) == 2

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "file_path", [pytest.param("dstability/example_1.stix", id="Input Structure")]
    )
    def test_given_data_soillayer_polygon_points_equal(self, file_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(file_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        expected_polygon_coords = [
            (70.0, 0.0),
            (20.0, 0.0),
            (20.0, 10.0),
            (30.0, 10.0),
            (50.0, 10.0),
            (70.0, 10.0),
        ]

        layer = dstability_model.datastructure.geometries[3].Layers[0]
        found_polygon_coords = [(p.X, p.Z) for p in layer.Points]
        assert expected_polygon_coords == found_polygon_coords
