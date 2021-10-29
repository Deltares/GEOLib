from pathlib import Path

import pytest

import geolib as gl
from geolib.models.dsheetpiling.calculation_options import *
from geolib.models.dsheetpiling.constructions import *
from geolib.models.dsheetpiling.dsheetpiling_model import *
from geolib.models.dsheetpiling.loads import *
from geolib.models.dsheetpiling.profiles import *
from geolib.models.dsheetpiling.settings import *
from geolib.soils import *
from tests.utils import TestUtils


class TestDsheetPilingBugFixes:
    @pytest.mark.acceptance
    def test_consistent_model_setting(self):
        # In this case the method set in the set_model function
        # should be consistent with what is written in the input file

        # 1. Build model.
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
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
        test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
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
        moment_load = Moment(name="New Moment", level=-4, load=10,)
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
    @pytest.mark.parametrize(
        "file",
        [
            pytest.param("bm4-5a.shd"),
            pytest.param("bm4-17a.shd"),
            pytest.param("bm3-1b.shd"),
            pytest.param("bm3-1d.shd"),
        ],
    )
    def test_geolib_173(self, file: str):
        # In this case the following structure can be seen in the dumpfile.
        #
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling/benchmarks"))
        test_file = test_folder / Path(file)

        model.parse(filename=test_file)
        outputdict = dict(model.output)

        if outputdict["calculation_type"] == "Standard":
            assert len(outputdict["construction_stage"]) == 3
        elif (
            outputdict["calculation_type"]
            == "Verify Sheet Piling according to CUR Method B"
        ):
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_deformation.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_moment_high_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_moment_low_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_high_mod_with_alt_passive_waterlevel.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_low_mod_with_alt_passive_waterlevel.construction_stage
                )
                == 1
            )
        elif outputdict["calculation_type"] == "Allowable Anchor Force":
            assert len(outputdict["construction_stage"]) == 1
        elif (
            outputdict["calculation_type"]
            == "Verify Sheet Piling according to CUR Method A"
        ):
            assert len(model.output.verify_deformation.construction_stage) == 1
            assert (
                len(
                    model.output.verify_moment_high_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(model.output.verify_moment_low_angle_of_subgr_reac.construction_stage)
                == 1
            )
