import os
import pathlib
import shutil
from pathlib import Path
from tkinter import Label

import pytest
from teamcity import is_running_under_teamcity

from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dgeoflow import DGeoFlowModel
from geolib.models.dgeoflow.internal import (
    CalculationTypeEnum,
    DGeoFlowStructure,
    ErosionDirectionEnum,
    PersistablePoint,
    PipeTrajectory,
)
from tests.utils import TestUtils, only_teamcity


class TestDGeoFlowModel:
    @pytest.mark.unittest
    def test_instantiate_dgeoflow_model(self):
        assert isinstance(DGeoFlowModel(filename=None), BaseModel), (
            "" + "DGeoFlowModel does not instantiate BaseModel"
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filepath",
        [
            pytest.param("dgeoflow/Berekening3", id="Input Structure"),
            pytest.param(
                "dgeoflow/Berekening3/Berekening3.flox", id="Input Structure for zip"
            ),
        ],
    )
    def test_given_data_dir_when_parse_then_datastructure_of_expected_type(
        self, filepath: str
    ):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(filepath))
        dgeoflow_model = DGeoFlowModel(filename=None)

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dgeoflow_model is not None

        # 3. Run test.
        dgeoflow_model.parse(test_input_filepath)

        # 4. Verify final expectations.
        assert dgeoflow_model.is_valid
        assert isinstance(dgeoflow_model.datastructure, DGeoFlowStructure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dgeoflow/Berekening3", id="Input Structure"),
        ],
    )
    def test_given_data_when_parse_and_serialize_then_does_not_raise(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dgeoflow_model = DGeoFlowModel(filename=None)
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dgeoflow/parseandserialize")
        )

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        if len(os.listdir(test_output_filepath)) > 0:
            shutil.rmtree(test_output_filepath)
            os.mkdir(test_output_filepath)
        assert dgeoflow_model is not None

        # 3. Run test.
        dgeoflow_model.parse(test_input_filepath)
        dgeoflow_model.serialize(test_output_filepath)

        # 4. Verify final expectations.
        assert dgeoflow_model.is_valid
        assert len(os.listdir(test_output_filepath)) > 0, (
            "" + "No data was generated while serializing."
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dgeoflow/Berekening3", id="Basic flow"),
            pytest.param("dgeoflow/Tutorial", id="Tutorial"),
        ],
    )
    def test_execute_model_successfully(self, dir_path: str):
        # 1. Set up test data.
        dm = DGeoFlowModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dm.parse(test_filepath)

        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dgeoflow"))
            / "Berekening3_serialized.flox"
        )
        dm.serialize(test_output_filepath)

        # 2. Verify initial expectations.
        assert os.path.exists(test_output_filepath)

        # 3. Run test.
        dm.filename = test_output_filepath
        model = dm.execute()

        # 3. Verify model output has been parsed
        assert model

    @pytest.mark.acceptance
    def test_generate_groundwater_flow_model(self):

        dm = DGeoFlowModel()

        layer_1 = [
            Point(x=-50, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=-50, z=-20),
        ]
        layer_2 = [
            Point(x=-50, z=-5),
            Point(x=50, z=-5),
            Point(x=50, z=-10),
            Point(x=-50, z=-10),
        ]
        layer_3 = [
            Point(x=-50, z=0),
            Point(x=-10, z=0),
            Point(x=30, z=0),
            Point(x=50, z=0),
            Point(x=50, z=-5),
            Point(x=-50, z=-5),
        ]
        embankment = [
            Point(x=-10, z=0),
            Point(x=0, z=2),
            Point(x=10, z=2),
            Point(x=30, z=0),
        ]

        layers_and_soils = [
            (layer_1, "Sand"),
            (layer_2, "H_Ro_z&k"),
            (layer_3, "H_Rk_k_shallow"),
            (embankment, "H_Aa_ht_old"),
        ]

        [dm.add_layer(points, soil) for points, soil in layers_and_soils]

        dm.add_boundary_condition([Point(x=-50, z=0), Point(x=-10, z=0)], 3, "River")
        dm.add_boundary_condition([Point(x=30, z=0), Point(x=50, z=0)], 0, "Polder")

        assert dm.is_valid

        # Serialize model to input file.
        path = Path(TestUtils.get_output_test_data_dir("dgeoflow"), "simple_model.flox")
        dm.serialize(path)

        # Check for successful execution
        dm.execute()
        assert dm.datastructure

        assert len(dm.datastructure.groundwater_flow_results) == 1
        assert len(dm.datastructure.groundwater_flow_results[0].Elements) == 386  # type: ignore
        assert dm.datastructure.groundwater_flow_results[0].Elements[10].NodeResults[0].TotalPorePressure == 143.661  # type: ignore

    @pytest.mark.acceptance
    def test_generate_pipe_length_model(self):
        dm = DGeoFlowModel()

        layer_1 = [
            Point(x=-50, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=-50, z=-20),
        ]
        layer_2 = [
            Point(x=-50, z=-5),
            Point(x=50, z=-5),
            Point(x=50, z=-10),
            Point(x=-50, z=-10),
        ]
        layer_3 = [
            Point(x=-50, z=0),
            Point(x=-10, z=0),
            Point(x=30, z=0),
            Point(x=50, z=0),
            Point(x=50, z=-5),
            Point(x=-50, z=-5),
        ]
        embankment = [
            Point(x=-10, z=0),
            Point(x=0, z=2),
            Point(x=10, z=2),
            Point(x=30, z=0),
        ]

        layers_and_soils = [
            (layer_1, "Sand"),
            (layer_2, "H_Ro_z&k"),
            (layer_3, "H_Rk_k_shallow"),
            (embankment, "H_Aa_ht_old"),
        ]

        [dm.add_layer(points, soil) for points, soil in layers_and_soils]

        dm.add_boundary_condition([Point(x=-50, z=0), Point(x=-10, z=0)], 17, "River")
        dm.add_boundary_condition([Point(x=30, z=0), Point(x=50, z=0)], 0, "Polder")

        dm.set_calculation_type(calculation_type=CalculationTypeEnum.PIPE_LENGTH)
        dm.set_pipe_trajectory(
            pipe_trajectory=PipeTrajectory(
                Label="Pipe",
                D70=0.1,
                ErosionDirection=ErosionDirectionEnum.RIGHT_TO_LEFT,
                ElementSize=1,
                Points=[PersistablePoint(X=30, Z=0), PersistablePoint(X=-10, Z=0)],
            )
        )
        
        assert dm.is_valid

        # Serialize model to input file.
        path = Path(
            TestUtils.get_output_test_data_dir("dgeoflow"),
            "simple_pipe_length_model.flox",
        )
        dm.serialize(path)

        # Check for successful execution
        dm.execute()
        assert dm.datastructure

        assert len(dm.datastructure.pipe_length_results) == 1
        assert len(dm.datastructure.pipe_length_results[0].Elements) == 640  # type: ignore
        assert dm.datastructure.pipe_length_results[0].Elements[10].NodeResults[0].TotalPorePressure == 208.255  # type: ignore
        assert dm.datastructure.pipe_length_results[0].PipeLength == 26.0

    @pytest.mark.acceptance
    def test_generate_critical_head_model(self):
        dm = DGeoFlowModel()

        layer_1 = [
            Point(x=-50, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=-50, z=-20),
        ]
        layer_2 = [
            Point(x=-50, z=-5),
            Point(x=50, z=-5),
            Point(x=50, z=-10),
            Point(x=-50, z=-10),
        ]
        layer_3 = [
            Point(x=-50, z=0),
            Point(x=-10, z=0),
            Point(x=30, z=0),
            Point(x=50, z=0),
            Point(x=50, z=-5),
            Point(x=-50, z=-5),
        ]
        embankment = [
            Point(x=-10, z=0),
            Point(x=0, z=2),
            Point(x=10, z=2),
            Point(x=30, z=0),
        ]

        layers_and_soils = [
            (layer_1, "Sand"),
            (layer_2, "H_Ro_z&k"),
            (layer_3, "H_Rk_k_shallow"),
            (embankment, "H_Aa_ht_old"),
        ]

        [dm.add_layer(points, soil) for points, soil in layers_and_soils]

        river_boundary_id = dm.add_boundary_condition(
            [Point(x=-50, z=0), Point(x=-10, z=0)], 17, "River"
        )
        dm.add_boundary_condition([Point(x=30, z=0), Point(x=50, z=0)], 0, "Polder")
        dm.set_calculation_type(calculation_type=CalculationTypeEnum.CRITICAL_HEAD)
        dm.set_pipe_trajectory(
            pipe_trajectory=PipeTrajectory(
                Label="Pipe",
                D70=0.1,
                ErosionDirection=ErosionDirectionEnum.RIGHT_TO_LEFT,
                ElementSize=1,
                Points=[PersistablePoint(X=30, Z=0), PersistablePoint(X=-10, Z=0)],
            )
        )
        dm.set_critical_head_boundary_condition(boundary_condition_id=river_boundary_id)
        dm.set_critical_head_search_parameters(
            minimum_head_level=17, maximum_head_level=18
        )

        assert dm.is_valid

        # Serialize model to input file.
        path = Path(
            TestUtils.get_output_test_data_dir("dgeoflow"),
            "simple_critical_head_model.flox",
        )
        dm.serialize(path)

        # Check for successful execution
        dm.execute()
        assert dm.datastructure

        assert len(dm.datastructure.critical_head_results) == 1
        assert len(dm.datastructure.critical_head_results[0].Elements) == 640  # type: ignore
        assert dm.datastructure.critical_head_results[0].Elements[10].NodeResults[0].TotalPorePressure == 208.968  # type: ignore
        assert dm.datastructure.critical_head_results[0].PipeLength == 29.0
        assert dm.datastructure.critical_head_results[0].CriticalHead == 17.5
