import pytest
from typing import Dict, Optional

from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.settings import PassiveSide, LateralEarthPressureMethod


class TestStage:
    @pytest.mark.unittest
    def test_add_initial_stage(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        assert model.current_stage is None

        model.add_stage(name=name_1st_stage)

        assert model.current_stage == 0
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

        model.add_stage(name=name_1st_stage, pile_top_displacement=pile_top_displacement)

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

        model.add_stage(name=name_1st_stage, passive_side=passive_side)

        assert (
            model.datastructure.input_data.construction_stages.stages[0].passive_side
            == value_in_input_file
        )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "stage_method,model_method",
        [
            pytest.param(
                LateralEarthPressureMethod.KA_KO_KP,
                LateralEarthPressureMethod.MIXED,
                id="Stage method with mixed 1",
            ),
            pytest.param(
                LateralEarthPressureMethod.C_PHI_DELTA,
                LateralEarthPressureMethod.MIXED,
                id="Stage method with mixed 2",
            ),
            pytest.param(
                LateralEarthPressureMethod.KA_KO_KP,
                LateralEarthPressureMethod.KA_KO_KP,
                id="Same methods",
            ),
            pytest.param(
                LateralEarthPressureMethod.C_PHI_DELTA,
                LateralEarthPressureMethod.C_PHI_DELTA,
                id="Same methods",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "use_method_left,use_method_right",
        [
            pytest.param(True, False, id="Left, not right"),
            pytest.param(False, True, id="Not left, right"),
            pytest.param(True, True, id="Both"),
            pytest.param(False, False, id="None"),
        ],
    )
    def test_add_stage_with_valid_methods(
        self,
        stage_method: LateralEarthPressureMethod,
        model_method: LateralEarthPressureMethod,
        use_method_left: bool,
        use_method_right: bool,
    ):
        model = DSheetPilingModel()
        kwargs = {
            "name": "Initial stage",
            "method_left": stage_method if use_method_left else None,
            "method_right": stage_method if use_method_right else None,
        }
        model.datastructure.input_data.model.method = model_method

        model.add_stage(**kwargs)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "stage_method,model_method",
        [
            pytest.param(
                LateralEarthPressureMethod.MIXED,
                LateralEarthPressureMethod.MIXED,
                id="No mixed stage method possible",
            ),
            pytest.param(
                LateralEarthPressureMethod.KA_KO_KP,
                LateralEarthPressureMethod.C_PHI_DELTA,
                id="Incompatible 1",
            ),
            pytest.param(
                LateralEarthPressureMethod.C_PHI_DELTA,
                LateralEarthPressureMethod.KA_KO_KP,
                id="Incompatible 2",
            ),
        ],
    )
    @pytest.mark.parametrize(
        "use_method_left,use_method_right",
        [
            pytest.param(True, False, id="Left, not right"),
            pytest.param(False, True, id="Not left, right"),
            pytest.param(True, True, id="Both"),
        ],
    )
    def test_add_stage_with_invalid_methods_raises_value_error(
        self,
        stage_method: LateralEarthPressureMethod,
        model_method: LateralEarthPressureMethod,
        use_method_left: bool,
        use_method_right: bool,
    ):
        model = DSheetPilingModel()
        kwargs = {
            "name": "Initial stage",
            "method_left": stage_method if use_method_left else None,
            "method_right": stage_method if use_method_right else None,
        }
        model.datastructure.input_data.model.method = model_method

        with pytest.raises(ValueError):
            model.add_stage(**kwargs)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "kwargs",
        [
            pytest.param({"copy": True}, id="Copy not (yet) possible"),
            pytest.param(
                {"pile_top_displacement": "not a number"}, id="Pile tip must be a number"
            ),
        ],
    )
    def test_add_stage_with_invalid_argument_raises_value_error(self, kwargs: Dict):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        with pytest.raises(ValueError):
            model.add_stage(name=name_1st_stage, **kwargs)

    @pytest.mark.unittest
    def test_add_second_stage_with_different_name(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        name_2nd_stage = "Second stage"

        assert model.current_stage is None

        model.add_stage(name=name_1st_stage)
        assert model.current_stage == 0

        model.add_stage(name=name_2nd_stage)
        assert model.current_stage == 1

    @pytest.mark.unittest
    def test_add_second_stage_with_similar_name_raises_value_error(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        model.add_stage(name=name_1st_stage)

        with pytest.raises(ValueError):
            model.add_stage(name=name_1st_stage)

    @pytest.mark.unittest
    def test_add_stage_copy_is_true_raises_valueError(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"

        with pytest.raises(ValueError):
            model.add_stage(name=name_1st_stage, copy=True)

    @pytest.mark.integrationtest
    def test_is_valid_initial_stage_with_none_values_raises_value_error(self):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        model.add_stage(name=name_1st_stage)

        with pytest.raises(ValueError):
            model.is_valid
