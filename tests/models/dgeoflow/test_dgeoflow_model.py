import os
import pathlib
import shutil
from pathlib import Path

import pytest
from teamcity import is_running_under_teamcity

from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dgeoflow import DGeoFlowModel
from geolib.models.dgeoflow.internal import DGeoFlowStructure

from tests.utils import TestUtils, only_teamcity


class TestDGeoFlowModel:
    @pytest.mark.unittest
    def test_instantiate_DGeoFlowModel(self):
        assert isinstance(DGeoFlowModel(filename=None), BaseModel), (
            "" + "DGeoFlowModel does not instanciate BaseModel"
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
    def test_given_datadir_when_parse_then_datastructure_of_expected_type(
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
    def test_given_data_when_parseandserialize_then_doesnotraise(self, dir_path: str):
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
    @pytest.mark.skipif(
        not is_running_under_teamcity(), reason="Console test only installed on TC."
    )
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dgeoflow/Berekening3", id="Input Structure"),
        ],
    )
    def test_execute_model_succesfully(self, dir_path: str):
        # 1. Set up test data.
        dm = DGeoFlowModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dm.parse(test_filepath)

        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dgeoflow")) / "Berekening3_serialized.flox"
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
    def test_generate_simple_model(self):

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

        layer_ids = [dm.add_layer(points, soil) for points, soil in layers_and_soils]
        for layer_id in layer_ids:
            # Has to be done in separate loop since all layers first need to be definied.
            dm.add_layeractivation(layer_id=layer_id)

        dm.add_boundarycondition([Point(x=-50,z=0), Point(x=-10,z=0)], 3, "River")
        dm.add_boundarycondition([Point(x=30,z=0), Point(x=50,z=0)], 0, "Polder")

        assert dm.is_valid

        # Serialize model to input file.
        path = pathlib.Path.cwd() / "test.flox"
        dm.serialize(path)

        # Check for succesfull execution
        dm.execute()
        assert dm.datastructure
