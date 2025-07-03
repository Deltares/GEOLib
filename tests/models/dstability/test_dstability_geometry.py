import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from geolib.geometry import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import PersistablePoint
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

    @pytest.mark.unittest
    def test_layer_with_incorrectly_ordered_points_are_fixed(self):
        layer = [
            Point(x=-50, z=-10),
            Point(x=20, z=-10),
            Point(x=40, z=-10),
            Point(x=30, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=20, z=-20),
            Point(x=40, z=-20),
            Point(x=30, z=-20),
            Point(x=-50, z=-20),
        ]

        dstability_model = DStabilityModel()
        dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=layer, soil_code="Peat")

        expected_layer = [
            PersistablePoint(X=30, Z=-10),
            PersistablePoint(X=40, Z=-10),
            PersistablePoint(X=50, Z=-10),
            PersistablePoint(X=50, Z=-20),
            PersistablePoint(X=40, Z=-20),
            PersistablePoint(X=30, Z=-20),
            PersistablePoint(X=20, Z=-20),
            PersistablePoint(X=-50, Z=-20),
            PersistablePoint(X=-50, Z=-10),
            PersistablePoint(X=20, Z=-10),
        ]

        assert (
            dstability_model.datastructure.geometries[0].Layers[0].Points
            == expected_layer
        )

    @pytest.mark.unittest
    def test_layer_with_missing_points_on_edge_are_fixed(self):
        layer1 = [
            Point(x=-50, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=-50, z=-20),
        ]

        layer2 = [
            Point(x=-50, z=-10),
            Point(x=-25, z=-10),
            Point(x=25, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=20),
            Point(x=-50, z=20),
        ]

        dstability_model = DStabilityModel()
        dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=layer1, soil_code="Peat")
        dstability_model.add_layer(points=layer2, soil_code="Peat")

        expected_layer = [
            PersistablePoint(X=50, Z=-20),
            PersistablePoint(X=-50, Z=-20),
            PersistablePoint(X=-50, Z=-10),
            PersistablePoint(X=-25, Z=-10),
            PersistablePoint(X=25, Z=-10),
            PersistablePoint(X=50, Z=-10),
        ]

        assert (
            dstability_model.datastructure.geometries[0].Layers[0].Points
            == expected_layer
        )

    @pytest.mark.unittest
    def test_multiple_layers_with_missing_points_on_edge_are_fixed(self):
        layer1 = [
            Point(x=0, z=0),
            Point(x=100, z=0),
            Point(x=100, z=10),
            Point(x=0, z=10),
        ]

        layer2 = [
            Point(x=10, z=10),
            Point(x=20, z=10),
            Point(x=20, z=20),
            Point(x=10, z=20),
        ]

        layer3 = [
            Point(x=25, z=10),
            Point(x=20, z=15),
            Point(x=25, z=20),
            Point(x=30, z=15),
            Point(x=30, z=10),
        ]

        dstability_model = DStabilityModel()
        dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=layer1, soil_code="Peat", label="L1")
        dstability_model.add_layer(points=layer2, soil_code="Peat", label="L2")
        dstability_model.add_layer(points=layer3, soil_code="Peat", label="L3")

        expected_layer = [
            PersistablePoint(X=30.0, Z=10.0),
            PersistablePoint(X=25.0, Z=10.0),
            PersistablePoint(X=20.0, Z=10.0),
            PersistablePoint(X=10.0, Z=10.0),
            PersistablePoint(X=0.0, Z=10.0),
            PersistablePoint(X=0.0, Z=0.0),
            PersistablePoint(X=100.0, Z=0.0),
            PersistablePoint(X=100.0, Z=10.0)
        ]

        assert (
            dstability_model.datastructure.geometries[0].Layers[0].Points
            == expected_layer
        )

    @pytest.mark.unittest
    def test_enclosed_layer_with_missing_points_on_edge_is_fixed(self):
        layer1 = [
            Point(x=0, z=0),
            Point(x=0, z=10),
            Point(x=10, z=10),
            Point(x=10, z=0),
            Point(x=9, z=0),
            Point(x=9, z=9),
            Point(x=5, z=9), # Point to add
            Point(x=1, z=9),
            Point(x=1, z=0),
        ]

        layer2 = [
            Point(x=1, z=0),
            Point(x=1, z=5),
            Point(x=5, z=5), # Point to add
            Point(x=9, z=5),
            Point(x=9, z=0),
        ]

        # Enclosed layer
        layer3 = [
            Point(x=1, z=5),
            Point(x=1, z=9),
            Point(x=9, z=9),
            Point(x=9, z=5),
        ]

        dstability_model = DStabilityModel()
        dstability_model.add_soil(Soil(code="Peat"))
        dstability_model.add_layer(points=layer1, soil_code="Peat", label="L1")
        dstability_model.add_layer(points=layer2, soil_code="Peat", label="L2")
        dstability_model.add_layer(points=layer3, soil_code="Peat", label="L3")

        expected_layer = [
            PersistablePoint(X=9.0, Z=9.0),
            PersistablePoint(X=9.0, Z=5.0),
            PersistablePoint(X=5.0, Z=5.0),
            PersistablePoint(X=1.0, Z=5.0),
            PersistablePoint(X=1.0, Z=9.0),
            PersistablePoint(X=5.0, Z=9.0),
        ]

        assert (
            dstability_model.datastructure.geometries[0].Layers[2].Points
            == expected_layer
        )
