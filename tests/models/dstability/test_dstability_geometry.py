import pytest

import os

from pydantic import ValidationError
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.soils import Soil
from geolib.geometry import Point
from pathlib import Path

from tests.utils import TestUtils

class TestDStabilityGeometry:
    @pytest.mark.unittest
    def test_dstability_add_layer_without_soil_raises(self):
        dstability_model = DStabilityModel(inputfn=None)
        points = [Point(x=-20., z=2.0), Point(x=50., z=2.0), Point(x=50.0, z=-5.), Point(x=-20., z=-5.)]
        
        with pytest.raises(ValueError):
            _ = dstability_model.add_layer(points=points, soil_code='Peat')

    @pytest.mark.unittest
    def test_dstability_add_layer_with_soil(self):
        dstability_model = DStabilityModel(inputfn=None)
        points = [Point(x=-20., z=2.0), Point(x=50., z=2.0), Point(x=50.0, z=-5.), Point(x=-20., z=-5.)]
        
        _ = dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=points, soil_code="Peat")
        assert len(dstability_model.datastructure.soillayers[0].SoilLayers) == 1

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_given_data_contains_num_soillayers(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(inputfn=None)
        
        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        assert len(dstability_model.datastructure.soillayers[0].SoilLayers) == 6

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_given_data_soillayer_polygon_points_equal(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(inputfn=None)
        
        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None
        
        # 3. Run test.
        dstability_model.parse(test_input_filepath)        
        expected_polygon_coords = [
            (150.0, -5.0),
            (150.0, -15.0),
            (-100, -15.0),
            (-100., -2.),
            (-9., -2.),
            (-1., -3.),
            (11., -3.),
            (20., -5.)]
        
        layer = dstability_model.datastructure.geometries[0].Layers[0]
        found_polygon_coords = [(p.X, p.Z) for p in layer.Points]
        assert expected_polygon_coords == found_polygon_coords
        
