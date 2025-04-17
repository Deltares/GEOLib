import os
from pathlib import Path

import pytest

from geolib.geometry import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    InternalStateTypeEnum,
    PersistablePoint,
    PersistableStateLine,
    PersistableStatePoint,
)
from geolib.models.dstability.states import (
    DStabilityStateLinePoint,
    DStabilityStatePoint,
    DStabilityStress,
)
from geolib.soils import Soil
from tests.utils import TestUtils


class TestDStabilityStates:
    def setup_class(self):
        self.points = [
            Point(x=-20.0, z=2.0),
            Point(x=50.0, z=2.0),
            Point(x=50.0, z=-5.0),
            Point(x=-20.0, z=-5.0),
        ]

    @pytest.mark.unittest
    def test_dstability_add_state_point_is_instance(self):
        dstability_model = DStabilityModel(filename=None)
        _ = dstability_model.add_soil(Soil(code="Peat"))
        layer_id = dstability_model.add_layer(points=self.points, soil_code="Peat")

        dstability_state_point = DStabilityStatePoint(
            id=1,
            layer_id=layer_id,
            point=Point(x=10.0, z=10.0),
            stress=DStabilityStress(state_type=InternalStateTypeEnum.OCR, ocr=10.0),
        )

        _ = dstability_model.add_state_point(dstability_state_point)
        assert isinstance(
            dstability_model.datastructure.states[0].StatePoints[0], PersistableStatePoint
        )

    @pytest.mark.unittest
    def test_dstability_add_state_point_wrong_layer_id(self):
        dstability_model = DStabilityModel(filename=None)

        _ = dstability_model.add_soil(Soil(code="Peat"))
        _ = dstability_model.add_layer(points=self.points, soil_code="Peat")

        with pytest.raises(ValueError):
            dstability_state_point = DStabilityStatePoint(
                id=1,
                layer_id=-1,
                point=Point(x=10.0, z=10.0),
                stress=DStabilityStress(state_type=InternalStateTypeEnum.OCR, ocr=10.0),
            )
            _ = dstability_model.add_state_point(dstability_state_point)

    @pytest.mark.unittest
    def test_dstability_add_state_line_is_instance(self):
        dstability_model = DStabilityModel(filename=None)

        _ = dstability_model.add_soil(Soil(code="Peat"))
        _ = dstability_model.add_layer(points=self.points, soil_code="Peat")

        state_line_points = [Point(x=-20.0, z=2.0), Point(x=50.0, z=2.0)]
        dstability_state_line_point = DStabilityStateLinePoint(
            id=1,
            above=DStabilityStress(state_type=InternalStateTypeEnum.OCR, ocr=10.0),
            below=DStabilityStress(state_type=InternalStateTypeEnum.POP, ocr=20.0),
            x=0,
        )

        _ = dstability_model.add_state_line(
            state_line_points, [dstability_state_line_point]
        )
        assert isinstance(
            dstability_model.datastructure.states[0].StateLines[0], PersistableStateLine
        )

    # todo > add test to read the example and see if the statepoint and lines are read
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "file_path", [pytest.param("dstability/example_1.stix", id="Input Structure")]
    )
    def test_given_data_statepoints_equal(self, file_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(file_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        expected_state_point = DStabilityStatePoint(
            id=55,
            layer_id=30,
            label="SP 1",
            point=Point(x=45.0, z=4.0),
            stress=DStabilityStress(pop=10.0),
        )
        expected_persistable_state_point = (
            expected_state_point._to_internal_datastructure()
        )
        assert (
            dstability_model._get_state(2, 0).StatePoints[0]
            == expected_persistable_state_point
        )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "file_path", [pytest.param("dstability/example_1.stix", id="Input Structure")]
    )
    def test_given_data_state_lines_equal(self, file_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(file_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        points = [Point(x=20.0, z=0.0), Point(x=70.0, z=0.0)]

        state_line_point = DStabilityStateLinePoint(
            id=56,
            label="SP 2",
            above=DStabilityStress(pop=20),
            below=DStabilityStress(pop=30),
            x=35.0,
        )

        expected_state_line = PersistableStateLine(
            Points=[PersistablePoint(X=p.x, Z=p.z) for p in points],
            Values=[state_line_point._to_internal_datastructure()],
        )
        assert dstability_model._get_state(2, 0).StateLines[0] == expected_state_line
