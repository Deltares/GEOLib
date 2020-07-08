import pytest
import os
from typing import List
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.states import DStabilityStress, DStabilityStatePoint, DStabilityStateLinePoint
from geolib.models.dstability.internal import StateType, PersistableStatePoint, PersistableStateLine, PersistablePoint
from geolib.geometry import Point
from geolib.soils import Soil
from pathlib import Path
from tests.utils import TestUtils


class TestDStabilityStates:
    def setup_class(self):
        self.points = [Point(x=-20., z=2.0), Point(x=50., z=2.0), Point(x=50.0, z=-5.), Point(x=-20., z=-5.)]

    @pytest.mark.unittest
    def test_dstability_add_state_point_is_instance(self):
        dstability_model = DStabilityModel(filename=None)
        _ = dstability_model.add_soil(Soil(code="Peat"))
        layer_id = dstability_model.add_layer(points=self.points, soil_code="Peat") 
        
        dstability_state_point = DStabilityStatePoint(
            id=1,
            layer_id=layer_id,
            point=Point(x=10.0, z=10.0),
            stress=DStabilityStress(state_type=StateType.OCR, ocr=10.0)
        )

        _ = dstability_model.add_state_point(dstability_state_point)
        assert isinstance(dstability_model.datastructure.states[0].StatePoints[0], PersistableStatePoint) 

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
                stress=DStabilityStress(state_type=StateType.OCR, ocr=10.0)
            )
            _ = dstability_model.add_state_point(dstability_state_point)

    @pytest.mark.unittest
    def test_dstability_add_state_line_is_instance(self):
        dstability_model = DStabilityModel(filename=None)

        _ = dstability_model.add_soil(Soil(code="Peat"))
        _ = dstability_model.add_layer(points=self.points, soil_code="Peat")

        state_line_points = [Point(x=-20., z=2.0), Point(x=50., z=2.0)]
        dstability_state_line_point = DStabilityStateLinePoint(
            id=1,
            above=DStabilityStress(state_type=StateType.OCR, ocr=10.0),
            below=DStabilityStress(state_type=StateType.POP, ocr=20.0),
            x=0
        )

        _ = dstability_model.add_state_line(state_line_points, [dstability_state_line_point])
        assert isinstance(dstability_model.datastructure.states[0].StateLines[0], PersistableStateLine) 


    # todo > add test to read the example and see if the statepoint and lines are read
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_given_data_statepoints_equal(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(inputfn=None)
        
        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None
        
        # 3. Run test.
        dstability_model.parse(test_input_filepath)      

        expected_state_point = DStabilityStatePoint(
            id=27,
            layer_id=14,
            label='SP 1',
            point=Point(x=4.26, z=7.67),
            stress=DStabilityStress()
        )
        expected_persistable_state_point = expected_state_point._to_internal_datastructure()
        assert dstability_model.datastructure.states[0].StatePoints[0] == expected_persistable_state_point

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_given_data_statelines_equal(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(inputfn=None)
        
        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None
        
        # 3. Run test.
        dstability_model.parse(test_input_filepath)   

        points = [
            Point(x=-8.8, z=3.5),
            Point(x=-1.4, z=1.0),
            Point(x=10.6, z=1.0),
            Point(x=20.0, z=4.0)
        ]   

        state_line_point = DStabilityStateLinePoint(
            id=28,
            label='SP 2',
            above=DStabilityStress(),
            below=DStabilityStress(),
            x=15.718
        )

        expected_state_line = PersistableStateLine(
            Points=[PersistablePoint(X=p.x, Z=p.z) for p in points],
            Values=[state_line_point._to_internal_datastructure()]
        )
        assert(dstability_model.datastructure.states[0].StateLines[0] == expected_state_line)
