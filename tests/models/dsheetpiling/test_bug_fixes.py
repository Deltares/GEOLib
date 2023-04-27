from pathlib import Path

import geolib as gl
import pytest
from geolib.models.dsheetpiling.calculation_options import *
from geolib.models.dsheetpiling.constructions import *
from geolib.models.dsheetpiling.dsheetpiling_model import *
from geolib.models.dsheetpiling.loads import *
from geolib.models.dsheetpiling.profiles import *
from geolib.models.dsheetpiling.settings import *
from geolib.soils import *
from tests.utils import TestUtils

test_file_directory = "dsheetpiling/bugfixes"
benchmarks_directory = 'dsheetpiling/benchmarks'


@pytest.mark.usefixtures("cleandir_dsh")
class TestDsheetPilingBugFixes:
    @pytest.mark.acceptance
    def test_consistent_model_setting(self):
        # In this case the method set in the set_model function
        # should be consistent with what is written in the input file

        # 1. Build model.
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_output_test_data_dir(test_file_directory))
        output_test_file = test_folder / Path("test_consistent_model_setting.shi")

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
        )
        model.set_model(modeltype)

        # Add stage 1.
        stage_id = model.add_stage(
            name="Stage 1",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()
        # 3. test final expectations
        assert model.input.input_data.model.method.value == 2

    @pytest.mark.acceptance
    def test_geolib191(self):
        # In this case the same load is added in multiple stages.
        # The load should not be duplicated if applied to multiple stages
        # The expectation is that the load is defined once but added to all the stages.

        # 1. Build model.
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_output_test_data_dir(test_file_directory))
        output_test_file = test_folder / Path("GEOLIB191.shi")

        # Add stage 1.
        stage_id = model.add_stage(
            name="Stage 1",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # Add stage 2.
        stage_id = model.add_stage(
            name="Stage 2",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        # same load should be applied in both stages
        model.add_load(load=uniform_load, stage_id=stage_id - 1)
        model.add_load(load=uniform_load, stage_id=stage_id)

        # add moment load
        moment_load = Moment(
            name="New Moment",
            level=-4,
            load=10,
        )
        model.add_load(load=moment_load, stage_id=stage_id - 1)
        model.add_load(load=moment_load, stage_id=stage_id)

        # add surcharge load
        surcharge_load = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
        )
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id - 1)
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=stage_id - 1)
        model.add_load(load=normal_force, stage_id=stage_id)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. check that only one load is written in the input
        assert len(model.input.input_data.uniform_loads.loads) == 1
        assert len(model.input.input_data.normal_forces.loads) == 1
        assert len(model.input.input_data.surcharge_loads.loads) == 1
        assert len(model.input.input_data.moments.loads) == 1
        # test that loads are applied in both stages
        stage_1 = model.input.input_data.construction_stages.stages[0]
        assert stage_1.moment_loads[0] == "New Moment"
        assert stage_1.normal_forces[0] == "New normal force"
        assert stage_1.surcharge_loads_left[0] == "New SurchargeLoad"
        assert stage_1.uniform_loads[0] == "New UniformLoad"
        stage_2 = model.input.input_data.construction_stages.stages[0]
        assert stage_2.moment_loads[0] == "New Moment"
        assert stage_2.normal_forces[0] == "New normal force"
        assert stage_2.surcharge_loads_left[0] == "New SurchargeLoad"
        assert stage_2.uniform_loads[0] == "New UniformLoad"

    @pytest.mark.integrationtest
    def test_parse_field_verify_sheet_piling_calculation_type_standard(self):
        # Former test of test_geolib_173
        # 1. Define test data
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir(benchmarks_directory))
        test_file = test_folder / Path("bm4-5a.shd")

        # 2. Verify initial conditions
        assert test_file.is_file()

        # 3. Run test
        model.parse(filename=test_file)

        # 4. Verify final expectations
        assert model.output.calculation_type == "Standard"
        assert len(model.output.construction_stage) == 3

    @pytest.mark.integrationtest
    def test_parse_field_verify_sheet_piling_calculation_type_allowable_anchor_force(
        self,
    ):
        # Former test of test_geolib_173
        # 1. Define test data
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir(benchmarks_directory))
        test_file = test_folder / Path("bm3-1b.shd")

        # 2. Verify initial conditions
        assert test_file.is_file()

        # 3. Run test
        model.parse(filename=test_file)

        # 4. Verify final expectations
        assert model.output.calculation_type == "Allowable Anchor Force"
        assert len(model.output.construction_stage) == 1

    @pytest.mark.integrationtest
    def test_parse_field_verify_sheet_piling_according_to_cur_method_a(self):
        # Former test of test_geolib_173
        # 1. Define test data
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir(benchmarks_directory))
        test_file = test_folder / Path("bm3-1d.shd")

        # 2. Verify initial conditions
        assert test_file.is_file()

        # 3. Run test
        model.parse(filename=test_file)

        # 4. Verify final expectations.
        assert (
            model.output.calculation_type
            == "Verify Sheet Piling according to CUR Method A"
        )
        assert model.output.verify_step_6____5_serviceability_limit_state
        assert model.output.verify_step_6____5_multiplied_by_factor
        assert (
            model.output.verify_step_6____3_low_modulus_of_subgrade_reaction_and_low_passive_water_level
        )

    @pytest.mark.integrationtest
    def test_parse_field_verify_sheet_piling_according_to_cur_method_b(self):
        # Former test of test_geolib_173
        # 1. Define test data
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir(benchmarks_directory))
        test_file = test_folder / Path("bm4-17a.shd")

        # 2. Verify initial conditions
        assert test_file.is_file()

        # 3. Run test
        model.parse(filename=test_file)

        assert (
            model.output.calculation_type
            == "Verify Sheet Piling according to CUR Method B"
        )
        assert model.output.verify_step_6____5_serviceability_limit_state
        assert model.output.verify_step_6____5_multiplied_by_factor
        assert (
            model.output.verify_step_6____3_low_modulus_of_subgrade_reaction_and_low_passive_water_level
        )
        assert (
            model.output.verify_step_6____4_high_modulus_of_subgrade_reaction_and_low_passive_water_level
        )
        assert (
            model.output.verify_step_6____1_low_modulus_of_subgrade_reaction_and_high_passive_water_level
        )
        assert (
            model.output.verify_step_6____2_high_modulus_of_subgrade_reaction_and_high_passive_water_level
        )
