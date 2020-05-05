import pytest
import os
import shutil
from pathlib import Path

from teamcity import is_running_under_teamcity

from geolib.models import BaseModel
from geolib.models import BaseModelStructure

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import DStabilityStructure

from tests.utils import TestUtils


class TestDStabilityModel:
    @pytest.mark.unittest
    def test_instantiate_DStabilityModel(self):
        assert isinstance(DStabilityModel(filename=None), BaseModel), (
            "" + "DStabilityModel does not instanciate BaseModel"
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filepath",
        [
            pytest.param("dstability/example_1", id="Input Structure"),
            pytest.param("dstability/example_1/Tutorial.stix", id="Input Structure"),
        ],
    )
    def test_given_datadir_when_parse_then_datastructure_of_expected_type(
        self, filepath: str
    ):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(filepath))
        dstability_model = DStabilityModel(filename=None)

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        # 4. Verify final expectations.
        assert dstability_model.is_valid
        assert isinstance(dstability_model.datastructure, DStabilityStructure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure"),],
    )
    def test_given_data_when_parseandserialize_then_doesnotraise(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(filename=None)
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dstability\\parseandserialize")
        )

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        if len(os.listdir(test_output_filepath)) > 0:
            shutil.rmtree(test_output_filepath)
            os.mkdir(test_output_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        dstability_model.serialize(test_output_filepath)

        # 4. Verify final expectations.
        assert dstability_model.is_valid
        assert len(os.listdir(test_output_filepath)) > 0, (
            "" + "No data was generated while serializing."
        )

    @pytest.mark.systemtest
    @pytest.mark.skipif(
        not is_running_under_teamcity(), reason="Console test only installed on TC."
    )
    def test_execute_model_succesfully(self):
        # 1. Set up test data.
        dm = DStabilityModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))
        dm.parse(test_filepath)

        test_output_filepath = Path(TestUtils.get_output_test_data_dir("test"))
        dm.serialize(test_output_filepath)

        # 2. Verify initial expectations.
        assert os.path.exists(test_output_filepath)

        # 3. Run test.
        dm.filename = test_output_filepath
        status = dm.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0

    @pytest.mark.unittest
    def test_gen_unique_id(self):
        """This test will fail when we've added new default
        ids to the internal datastructure. Please update accordingly."""
        max_id_after_initialization_of_dstability_structure = 32
        dm = DStabilityModel()

        assert dm.datastructure.waternets[0].Id == "21"
        new_id = dm.datastructure.get_unique_id()
        assert new_id == max_id_after_initialization_of_dstability_structure

    @pytest.mark.integrationtest
    def test_generate_simple_model(self):

        import pathlib

        from geolib.models.dstability import DStabilityModel

        from geolib.models.dstability.analysis import (
            DStabilityBishopAnalysisMethod,
            DStabilityCircle,
        )

        from geolib.geometry.one import Point

        dm = DStabilityModel()

        bishop_analysis_method = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=20, z=3), radius=15)
        )

        dm.set_model(bishop_analysis_method)

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

        layer_ids = []

        for layer, soil in layers_and_soils:

            layer_id = dm.add_layer(layer, soil)

            layer_ids.append(layer_id)

        for (
            layer_id
        ) in (
            layer_ids
        ):  # Has to be done in separate loop since all layers first need to be definied.

            dm.add_soil_layer_consolidations(soil_layer_id=layer_id)

        assert len(dm.datastructure.loads[0].LayerLoads) == 4

        # assert (
        # dm.is_valid
        # ), True  # TODO call this during serializing; also, consider raising error why it's not valid

        # Serialize model to input file.

        path = pathlib.Path.cwd() / "test.stix"

        dm.serialize(path)
