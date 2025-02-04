import pytest

from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.settings import (
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    PassiveSide,
)


class TestStage:
    @pytest.mark.unittest
    def test_add_initial_stage(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        assert model.current_stage is None

        stage_id = model.add_stage(
            name=name_1st_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        )

        assert model.current_stage == stage_id == 0
        assert len(model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            model.datastructure.input_data.construction_stages.stages[0].name
            == name_1st_stage
        )

    @pytest.mark.unittest
    def test_add_stage_with_pile_top_displacement(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        pile_top_displacement = 0.05

        model.add_stage(
            name=name_1st_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
            pile_top_displacement=pile_top_displacement,
        )

        assert (
            model.datastructure.input_data.construction_stages.stages[
                0
            ].displacement_top_sheet_piling
            == pile_top_displacement
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "passive_side,value_in_input_file",
        [
            pytest.param(
                PassiveSide.DSHEETPILING_DETERMINED, 0, id="DSheetPiling determined"
            ),
            pytest.param(PassiveSide.LEFT, 1, id="Left side"),
            pytest.param(PassiveSide.RIGHT, 2, id="Right side"),
        ],
    )
    def test_add_stage_with_valid_passive_sides(
        self, passive_side: PassiveSide, value_in_input_file: int
    ):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        model.add_stage(
            name=name_1st_stage,
            passive_side=passive_side,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        )

        assert (
            model.datastructure.input_data.construction_stages.stages[0].passive_side
            == value_in_input_file
        )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "stage_method,model_method",
        [
            pytest.param(
                LateralEarthPressureMethodStage.KA_KO_KP,
                LateralEarthPressureMethod.MIXED,
                id="Stage method with mixed 1",
            ),
            pytest.param(
                LateralEarthPressureMethodStage.C_PHI_DELTA,
                LateralEarthPressureMethod.MIXED,
                id="Stage method with mixed 2",
            ),
            pytest.param(
                LateralEarthPressureMethodStage.KA_KO_KP,
                LateralEarthPressureMethod.KA_KO_KP,
                id="Same methods",
            ),
            pytest.param(
                LateralEarthPressureMethodStage.C_PHI_DELTA,
                LateralEarthPressureMethod.C_PHI_DELTA,
                id="Same methods",
            ),
        ],
    )
    def test_add_stage_with_valid_methods(
        self,
        stage_method: LateralEarthPressureMethodStage,
        model_method: LateralEarthPressureMethod,
    ):
        model = DSheetPilingModel()
        kwargs = {
            "name": "Initial stage",
            "passive_side": PassiveSide.DSHEETPILING_DETERMINED,
            "method_left": stage_method,
            "method_right": stage_method,
        }
        model.datastructure.input_data.model.method = model_method

        model.add_stage(**kwargs)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "stage_method,model_method",
        [
            pytest.param(
                LateralEarthPressureMethodStage.KA_KO_KP,
                LateralEarthPressureMethod.C_PHI_DELTA,
                id="Incompatible 1",
            ),
            pytest.param(
                LateralEarthPressureMethodStage.C_PHI_DELTA,
                LateralEarthPressureMethod.KA_KO_KP,
                id="Incompatible 2",
            ),
        ],
    )
    def test_add_stage_with_invalid_methods_raises_value_error(
        self,
        stage_method: LateralEarthPressureMethodStage,
        model_method: LateralEarthPressureMethod,
    ):
        model = DSheetPilingModel()
        kwargs = {
            "name": "Initial stage",
            "passive_side": PassiveSide.DSHEETPILING_DETERMINED,
            "method_left": stage_method,
            "method_right": stage_method,
        }
        model.datastructure.input_data.model.method = model_method

        with pytest.raises(ValueError):
            model.add_stage(**kwargs)

    @pytest.mark.unittest
    def test_add_second_stage_with_different_name(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        name_2nd_stage = "Second stage"

        assert model.current_stage is None

        model.add_stage(
            name=name_1st_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        )
        assert model.current_stage == 0
        assert len(model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            model.datastructure.input_data.construction_stages.stages[0].passive_side
            == PassiveSide.DSHEETPILING_DETERMINED
        )

        model.add_stage(
            name=name_2nd_stage,
            passive_side=PassiveSide.LEFT,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        )
        assert model.current_stage == 1
        assert len(model.datastructure.input_data.construction_stages.stages) == 2
        assert (
            model.datastructure.input_data.construction_stages.stages[0].passive_side
            == PassiveSide.DSHEETPILING_DETERMINED
        )
        assert (
            model.datastructure.input_data.construction_stages.stages[1].passive_side
            == PassiveSide.LEFT
        )

    @pytest.mark.unittest
    def test_add_second_stage_with_similar_name_raises_value_error(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        model.add_stage(
            name=name_1st_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        )

        with pytest.raises(ValueError):
            model.add_stage(
                name=name_1st_stage,
                passive_side=PassiveSide.DSHEETPILING_DETERMINED,
                method_left=LateralEarthPressureMethodStage.KA_KO_KP,
                method_right=LateralEarthPressureMethodStage.KA_KO_KP,
            )

    @pytest.mark.unittest
    @pytest.mark.xfail(reason="Not yet implemented")
    def test_add_stage_copy_is_true_raises_valueError(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        with pytest.raises(ValueError):
            model.add_stage(
                name=name_1st_stage,
                passive_side=PassiveSide.DSHEETPILING_DETERMINED,
                method_left=LateralEarthPressureMethodStage.KA_KO_KP,
                method_right=LateralEarthPressureMethodStage.KA_KO_KP,
                copy=True,
            )
