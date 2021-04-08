import os
from pathlib import Path
from typing import List

import pytest
from pydantic import ValidationError

from geolib.geometry.one import Point
from geolib.models.dstability.analysis import (
    DStabilityBishopAnalysisMethod,
    DStabilityBishopBruteForceAnalysisMethod,
    DStabilityCircle,
    DStabilitySearchArea,
    DStabilitySearchGrid,
    DStabilitySlipPlaneConstraints,
    DStabilitySpencerAnalysisMethod,
    DStabilitySpencerGeneticAnalysisMethod,
    DStabilityUpliftVanAnalysisMethod,
    DStabilityUpliftVanParticleSwarmAnalysisMethod,
)
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    PersistableLayerLoad,
    PersistableLineLoad,
    PersistableSoilLayer,
    PersistableUniformLoad,
)
from geolib.models.dstability.loads import Consolidation, LineLoad, UniformLoad
from tests.utils import TestUtils


class TestDStabilityAnalysis:
    @pytest.mark.unittest
    def test_create_bishop_analysis(self):
        dstability_model = DStabilityModel()
        bishop_analysis = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=10.0, z=10.0), radius=15)
        )
        dstability_model.set_model(bishop_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].Bishop
            == bishop_analysis._to_internal_datastructure()
        )

    @pytest.mark.unittest
    def test_create_bishop_brute_force_analysis(self):
        dstability_model = DStabilityModel()
        bishop_brute_force_analysis = DStabilityBishopBruteForceAnalysisMethod(
            search_grid=DStabilitySearchGrid(
                bottom_left=Point(x=0, z=-10.0),
                number_of_points_in_x=10,
                number_of_points_in_z=10,
                space=0.5,
            ),
            bottom_tangent_line_z=-10,
            number_of_tangent_lines=5,
            space_tangent_lines=0.5,
        )
        dstability_model.set_model(bishop_brute_force_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].BishopBruteForce
            == bishop_brute_force_analysis._to_internal_datastructure()
        )

    @pytest.mark.unittest
    def test_create_spencer_analysis(self):
        dstability_model = DStabilityModel()
        spencer_analysis = DStabilitySpencerAnalysisMethod(
            slipplane=[Point(x=-10, z=-5), Point(x=-5, z=-6), Point(x=-3, z=-4)]
        )
        dstability_model.set_model(spencer_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].Spencer
            == spencer_analysis._to_internal_datastructure()
        )

    @pytest.mark.unittest
    def test_create_spencer_genetic_algorithm_analysis(self):
        dstability_model = DStabilityModel()
        spencer_genetic_algorithm_analysis = DStabilitySpencerGeneticAnalysisMethod(
            slip_plane_a=[Point(x=-10, z=-5), Point(x=-5, z=-6), Point(x=-3, z=-4)],
            slip_plane_b=[Point(x=-10, z=-8), Point(x=-5, z=-7), Point(x=-3, z=-6)],
        )
        dstability_model.set_model(spencer_genetic_algorithm_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].SpencerGenetic
            == spencer_genetic_algorithm_analysis._to_internal_datastructure()
        )

    @pytest.mark.unittest
    def test_create_uplift_van_algorithm_analysis(self):
        dstability_model = DStabilityModel()
        uplift_van_analysis = DStabilityUpliftVanAnalysisMethod(
            first_circle=DStabilityCircle(center=Point(x=10.0, z=10.0), radius=15),
            second_circle_center=Point(x=30, z=5.0),
        )
        dstability_model.set_model(uplift_van_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].UpliftVan
            == uplift_van_analysis._to_internal_datastructure()
        )

    @pytest.mark.unittest
    def test_create_uplift_van_particle_swarm_algorithm_analysis(self):
        dstability_model = DStabilityModel()
        uplift_van_particle_swarm_analysis = DStabilityUpliftVanParticleSwarmAnalysisMethod(
            search_area_a=DStabilitySearchArea(
                height=5.0, top_left=Point(x=-10.0, z=10.0), width=5.0
            ),
            search_area_b=DStabilitySearchArea(
                height=5.0, top_left=Point(x=10.0, z=10.0), width=5.0
            ),
            tangent_area_height=2.0,
            tangent_area_top_z=-5.0,
        )
        dstability_model.set_model(uplift_van_particle_swarm_analysis)
        assert (
            dstability_model.datastructure.calculationsettings[0].UpliftVanParticleSwarm
            == uplift_van_particle_swarm_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_bishop_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        bishop_analysis = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=23.7, z=24.6), radius=28)
        )

        assert (
            dstability_model.datastructure.calculationsettings[0].Bishop
            == bishop_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_bishop_brute_force_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)
        bishop_brute_force_analysis = DStabilityBishopBruteForceAnalysisMethod(
            search_grid=DStabilitySearchGrid(
                bottom_left=Point(x=20.43, z=18.150000000000002),
                number_of_points_in_x=17,
                number_of_points_in_z=10,
                space=1.0,
            ),
            bottom_tangent_line_z=2.8900000000000006,
            number_of_tangent_lines=16,
            space_tangent_lines=0.5,
        )
        assert (
            dstability_model.datastructure.calculationsettings[0].BishopBruteForce
            == bishop_brute_force_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_spencer_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        spencer_analysis = DStabilitySpencerAnalysisMethod(
            slipplane=[
                Point(x=-9.5, z=10.94),
                Point(x=-6.71, z=8.79),
                Point(x=4.15, z=6.56),
                Point(x=12.61, z=6.24),
                Point(x=21.23, z=5.44),
                Point(x=25.0, z=7.54),
            ]
        )
        assert (
            dstability_model.datastructure.calculationsettings[0].Spencer
            == spencer_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_spencer_genetic_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        spencer_genetic_analysis = DStabilitySpencerGeneticAnalysisMethod(
            slip_plane_a=[
                Point(x=-1.997, z=12.075),
                Point(x=3.83, z=9.27),
                Point(x=10.05, z=9.11),
                Point(x=16.5, z=8.93),
            ],
            slip_plane_b=[
                Point(x=-9.5, z=10.94),
                Point(x=0.64, z=5.76),
                Point(x=15.96, z=4.48),
                Point(x=25.0, z=7.54),
            ],
        )
        assert (
            dstability_model.datastructure.calculationsettings[0].SpencerGenetic
            == spencer_genetic_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_upliftvan_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        uplift_van_analysis = DStabilityUpliftVanAnalysisMethod(
            first_circle=DStabilityCircle(
                center=Point(x=6.73, z=17.54), radius=13.599830881301427
            ),
            second_circle_center=Point(x=21.23, z=9.98),
        )
        #        # debug(dstability_model.datastructure.calculationsettings[0].UpliftVan)

        assert (
            dstability_model.datastructure.calculationsettings[0].UpliftVan
            == uplift_van_analysis._to_internal_datastructure()
        )

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "dir_path", [pytest.param("dstability/example_1", id="Input Structure")]
    )
    def test_parse_upliftvan_particle_swarm_settings(self, dir_path: str):
        # 1. Set up test data.
        test_input_filepath = Path(TestUtils.get_local_test_data_dir(dir_path))
        dstability_model = DStabilityModel()

        # 2. Verify initial expectations.
        assert os.path.exists(test_input_filepath)
        assert dstability_model is not None

        # 3. Run test.
        dstability_model.parse(test_input_filepath)

        uplift_van_particle_swarm_analysis = DStabilityUpliftVanParticleSwarmAnalysisMethod(
            search_area_a=DStabilitySearchArea(
                height=5.109999999999999,
                top_left=Point(x=4.3100000000000005, z=19.97),
                width=4.949999999999999,
            ),
            search_area_b=DStabilitySearchArea(
                height=2.08, top_left=Point(x=19.31, z=11.35), width=4.790000000000003
            ),
            slip_plane_constraints=DStabilitySlipPlaneConstraints(
                width_zone_a=-5.0, x_left_zone_a=-5.0
            ),
            tangent_area_height=6.539999999999999,
            tangent_area_top_z=9.43,
        )
        assert (
            dstability_model.datastructure.calculationsettings[0].UpliftVanParticleSwarm
            == uplift_van_particle_swarm_analysis._to_internal_datastructure()
        )
