import os
import pathlib
import shutil
from pathlib import Path

import pytest
from teamcity import is_running_under_teamcity
from tests.utils import TestUtils, only_teamcity

from geolib.geometry.one import Point
from geolib.models import BaseModel, BaseModelStructure
from geolib.models.dstability import DStabilityModel
from geolib.models.dstability.analysis import (
    DStabilityBishopAnalysisMethod,
    DStabilityBishopBruteForceAnalysisMethod,
    DStabilityCircle,
    DStabilitySearchArea,
    DStabilitySearchGrid,
    DStabilitySpencerAnalysisMethod,
    DStabilitySpencerGeneticAnalysisMethod,
    DStabilityUpliftVanAnalysisMethod,
    DStabilityUpliftVanParticleSwarmAnalysisMethod,
)
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    AnalysisTypeEnum,
    CalculationTypeEnum,
    DStabilityStructure,
)
from geolib.models.dstability.loads import Consolidation, LineLoad, UniformLoad
from geolib.models.dstability.reinforcements import ForbiddenLine, Geotextile, Nail
from geolib.models.dstability.states import (
    DStabilityStateLinePoint,
    DStabilityStatePoint,
    DStabilityStress,
)
from geolib.soils import Soil


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
            pytest.param(
                "dstability/example_1/Tutorial.stix", id="Input Structure for zip"
            ),
            pytest.param("dstability/Tutorial_v20_2_1", id="Tutorial DStability 20.2.1"),
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
        "dir_path",
        [
            pytest.param("dstability/example_1", id="Input Structure"),
            pytest.param("dstability/Tutorial_v20_2_1", id="Tutorial DStability 20.2.1"),
        ],
    )
    def test_given_data_when_parseandserialize_then_doesnotraise(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel(filename=None)
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dstability/parseandserialize")
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
    @pytest.mark.parametrize(
        "dir_path",
        [
            pytest.param("dstability/example_1", id="Input Structure"),
            pytest.param("dstability/Tutorial_v20_2_1", id="Tutorial DStability 20.2.1"),
        ],
    )
    def test_execute_model_succesfully(self, dir_path: str):
        # 1. Set up test data.
        dm = DStabilityModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
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
        max_id_after_initialization_of_dstability_structure = 21
        dm = DStabilityModel()

        assert dm.datastructure.waternets[0].Id == "14"
        new_id = dm.datastructure.get_unique_id()
        assert new_id == max_id_after_initialization_of_dstability_structure

    @pytest.mark.acceptance
    @only_teamcity
    def test_generate_simple_model(self):

        dm = DStabilityModel()

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
            dm.add_soil_layer_consolidations(soil_layer_id=layer_id)

        assert len(dm.datastructure.loads[0].LayerLoads) == 4
        assert dm.is_valid

        # Serialize model to input file.
        path = pathlib.Path.cwd() / "test.stix"
        dm.serialize(path)

        status = dm.execute()
        assert status.returncode == 0

    @pytest.mark.systemtest
    def test_get_stabfactor(self):
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/test_dstab_full.stix")
        )
        dm = DStabilityModel()
        dm.parse(test_filepath)
        assert pytest.approx(dm.output["FactorOfSafety"], 0.56)

    def test_get_slipeplane(self):
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/test_dstab_full.stix")
        )
        dm = DStabilityModel()
        dm.parse(test_filepath)
        assert len(dm.output["SlipPlane"]) == 5

    @pytest.mark.acceptance
    @only_teamcity
    def test_generate_model_from_scratch(self):

        dm = DStabilityModel()

        bishop_analysis_method = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=20, z=3), radius=15)
        )
        dm.set_model(bishop_analysis_method)

        assert (
            dm.datastructure.calculationsettings[0].CalculationType
            == CalculationTypeEnum.DETERMINISTIC
        )
        assert (
            dm.datastructure.calculationsettings[0].AnalysisType
            == AnalysisTypeEnum.BISHOP
        )

        # add soil
        soil_peat_id = dm.add_soil(
            Soil(
                name="Peat (weak)",
                code="HV",
                cohesion=0.5,
                friction_angle=15.0,
                volumetric_weight_above_phreatic_level=10.2,
                volumetric_weight_below_phreatic_level=10.2,
            )
        )

        # add layers
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
            (layer_3, "HV"),
            (embankment, "H_Aa_ht_old"),
        ]

        layer_ids = []

        for layer, soil in layers_and_soils:
            layer_id = dm.add_layer(layer, soil)
            layer_ids.append(layer_id)

        outputdir = Path(TestUtils.get_output_test_data_dir("dstability/acceptancetest/"))
        path = outputdir / "test_layers.stix"
        dm.serialize(path)

        # add phreatic line
        phreatic_line_id = dm.add_head_line(
            points=[
                Point(x=-50, z=1.0),
                Point(x=0, z=1),
                Point(x=30, z=-1),
                Point(x=50, z=-1),
            ],
            label="Phreatic Line",
            is_phreatic_line=True,
        )

        path = outputdir / "test_phreatic_line.stix"
        dm.serialize(path)

        # add headline for deep sand
        sand_head_line_id = dm.add_head_line(
            points=[Point(x=-50, z=5.0), Point(x=50, z=5.0)],
            label="Hydraulic head in sandlayer",
        )

        dm.add_reference_line(
            points=[Point(x=-50, z=-3), Point(x=50, z=-3)],
            bottom_headline_id=phreatic_line_id,
            top_head_line_id=phreatic_line_id,
        )

        dm.add_reference_line(
            points=[Point(x=-50, z=-10), Point(x=50, z=-10)],
            bottom_headline_id=sand_head_line_id,
            top_head_line_id=sand_head_line_id,
        )

        path = outputdir / "test_reference_line.stix"
        dm.serialize(path)

        # change some parameters
        dm.edit_soil("HV", cohesion=2.0, friction_angle=17.5)
        path = outputdir / "test_edited_soil.stix"
        dm.serialize(path)

        #  add uniform load
        dm.add_load(
            UniformLoad(
                label="trafficload",
                start=6.5,
                end=9.0,
                magnitude=13,
                angle_of_distribution=45,
            )
        )
        path = outputdir / "test_uniformload.stix"
        dm.serialize(path)

        # add line load
        dm.add_load(
            LineLoad(
                location=Point(x=2.0, z=2.0),
                angle=0.0,
                magnitude=10.0,
                angle_of_distribution=45.0,
            )
        )
        path = outputdir / "test_lineload.stix"
        dm.serialize(path)

        # create reinforcements NAIL
        dm.add_reinforcement(
            Nail(
                location=Point(x=20.0, z=1.0),
                direction=15.0,
                horizontal_spacing=1.0,
                length=3.0,
                grout_diameter=0.1,
                max_pull_force=10.0,
                plastic_moment=5.0,
                bending_stiffness=100.0,
            )
        )
        path = outputdir / "test_nail.stix"
        dm.serialize(path)

        # create reinforcements GEOTEXTILE
        dm.add_reinforcement(
            Geotextile(
                start=Point(x=20.0, z=0.0),
                end=Point(x=30.0, z=0.0),
                effective_tensile_strength=10.0,
                reduction_area=0.5,
            )
        )
        path = outputdir / "test_geotextile.stix"
        dm.serialize(path)

        # create reinforcements FORBIDDEN LINE
        dm.add_reinforcement(
            ForbiddenLine(start=Point(x=30.0, z=0.0), end=Point(x=30.0, z=-4.0))
        )
        path = outputdir / "test_forbidden_line.stix"
        dm.serialize(path)

        # add bishop brute force
        dm.set_model(
            DStabilityBishopBruteForceAnalysisMethod(
                search_grid=DStabilitySearchGrid(
                    bottom_left=Point(x=15, z=2),
                    number_of_points_in_x=10,
                    number_of_points_in_z=10,
                    space=0.5,
                ),
                bottom_tangent_line_z=-6.0,
                number_of_tangent_lines=5,
                space_tangent_lines=0.5,
            )
        )
        path = outputdir / "test_bishop_brute_force.stix"
        dm.serialize(path)

        # add spencer
        dm.set_model(
            DStabilitySpencerAnalysisMethod(
                slipplane=[
                    Point(x=7, z=2.0),
                    Point(x=15, z=-3),
                    Point(x=30, z=-4.5),
                    Point(x=40, z=0.0),
                ]
            )
        )
        path = outputdir / "test_spencer.stix"
        dm.serialize(path)

        # add spencer genetic
        dm.set_model(
            DStabilitySpencerGeneticAnalysisMethod(
                slip_plane_a=[
                    Point(x=10, z=2.0),
                    Point(x=15, z=0),
                    Point(x=30, z=-4),
                    Point(x=35, z=0.0),
                ],
                slip_plane_b=[
                    Point(x=5, z=2.0),
                    Point(x=15, z=-3),
                    Point(x=30, z=-6),
                    Point(x=40, z=0.0),
                ],
            )
        )
        path = outputdir / "test_spencer_genetic.stix"
        dm.serialize(path)

        # uplift
        dm.set_model(
            DStabilityUpliftVanAnalysisMethod(
                first_circle=DStabilityCircle(center=Point(x=5, z=5), radius=9.5),
                second_circle_center=Point(x=40, z=2),
            )
        )
        path = outputdir / "test_uplift.stix"
        dm.serialize(path)

        # uplift particle swarm
        dm.set_model(
            DStabilityUpliftVanParticleSwarmAnalysisMethod(
                search_area_a=DStabilitySearchArea(
                    height=5.0, top_left=Point(x=0.0, z=10.0), width=5.0
                ),
                search_area_b=DStabilitySearchArea(
                    height=5.0, top_left=Point(x=35.0, z=5.0), width=5.0
                ),
                tangent_area_height=2.0,
                tangent_area_top_z=-4.5,
            )
        )
        path = outputdir / "test_uplift_particle_swarm.stix"
        dm.serialize(path)

        # state point
        dm.add_state_point(
            DStabilityStatePoint(
                layer_id=layer_ids[2],  # HV layer
                point=Point(x=0, z=-2.5),
                stress=DStabilityStress(pop=10.0),
            )
        )
        path = outputdir / "test_state_point.stix"
        dm.serialize(path)

        # state line
        dm.add_state_line(
            points=[Point(x=-50, z=-2), Point(x=50, z=-2)],
            state_points=[
                DStabilityStateLinePoint(
                    above=DStabilityStress(pop=5), below=DStabilityStress(pop=10), x=20
                )
            ],
        )
        path = outputdir / "test_state_line.stix"
        dm.serialize(path)

        # Test run and verify return code of 0 (indicates succesfull run)
        status = dm.execute()
        assert status.returncode == 0
