from typing import Callable
import pytest

from geolib.models.dsheetpiling.water_level import WaterLevel
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.internal import (
    _DEFAULT_WATER_LEVEL_NAME,
    WaterLevels,
    WaterLevel as InternalWaterLevel,
)
from geolib.models.dsheetpiling.settings import (
    Side,
    PassiveSide,
    LateralEarthPressureMethodStage,
)


@pytest.fixture
def _model() -> DSheetPilingModel:
    model = DSheetPilingModel()
    model.add_stage(
        name="Initial stage",
        passive_side=PassiveSide.DSHEETPILING_DETERMINED,
        method_left=LateralEarthPressureMethodStage.KA_KO_KP,
        method_right=LateralEarthPressureMethodStage.KA_KO_KP,
    )
    return model

@pytest.fixture
def make_water_level() -> WaterLevel:
    def _make_water_level(name: str):
        return WaterLevel(
            name=name,
            level = -1
        )
    return _make_water_level


class TestWaterLevels:

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_water_level_invalid_stage_id_raises_ValueError(
        self,
        _model: DSheetPilingModel,
        make_water_level: Callable
    ):
        water_level = make_water_level(name=_DEFAULT_WATER_LEVEL_NAME)
        invalid_stage_id = len(_model.datastructure.input_data.construction_stages.stages) + 1

        with pytest.raises(ValueError, match=r"Stage \d+ is not added to the internal datastructure"):
            _model.add_head_line(water_level=water_level, side=Side.BOTH, stage_id=invalid_stage_id)


    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side",
        [
            pytest.param(Side.LEFT, id="Left side"),
            pytest.param(Side.RIGHT, id="Right side"),
            pytest.param(Side.BOTH, id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_water_level_internal_water_levels_updated(self, _model: DSheetPilingModel, make_water_level: Callable, side: Side):
        """Validate if water_level is refered in [WATERLEVELS]"""

        water_level_name = "Ground water level -1m"
        current_stage = _model.current_stage
        assert water_level_name != _DEFAULT_WATER_LEVEL_NAME
        water_level = make_water_level(water_level_name)

        _model.add_head_line(water_level=water_level, side=side, stage_id=current_stage)

        assert isinstance(_model.datastructure.input_data.waterlevels, WaterLevels)
        assert len(_model.datastructure.input_data.waterlevels.levels) == 1
        internal = _model.datastructure.input_data.waterlevels.levels[current_stage]
        assert isinstance(internal, InternalWaterLevel)
        assert internal.name == water_level_name
        assert internal.level == water_level.level
        assert internal.distribution_type == water_level.distribution_type
        assert internal.standard_deviation == water_level.standard_deviation

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side, left_water_level_name, right_water_level_name",
        [
            pytest.param(Side.LEFT, "Left water_level", _DEFAULT_WATER_LEVEL_NAME, id="Left side"),
            pytest.param(Side.RIGHT, _DEFAULT_WATER_LEVEL_NAME, "Right water_level", id="Right side"),
            pytest.param(Side.BOTH, "Same water_level", "Same water_level", id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_water_level_internal_construction_stages(
        self,
        _model: DSheetPilingModel,
        make_water_level: Callable,
        side: Side,
        left_water_level_name: str,
        right_water_level_name: str,
    ):
        """Validate if water_level is refered in [CONSTRUCTION STAGES]"""
        current_stage_id = _model.current_stage
        if side == Side.LEFT:
            assert left_water_level_name != _DEFAULT_WATER_LEVEL_NAME
            water_level = make_water_level(left_water_level_name)
        elif side == Side.RIGHT:
            assert right_water_level_name != _DEFAULT_WATER_LEVEL_NAME
            water_level = make_water_level(right_water_level_name)
        else:
            assert left_water_level_name == right_water_level_name != _DEFAULT_WATER_LEVEL_NAME
            water_level = make_water_level(right_water_level_name)

        _model.add_head_line(water_level=water_level, side=side, stage_id=current_stage_id)

        current_stage = _model.datastructure.input_data.construction_stages.stages[current_stage_id]
        assert current_stage.water_level_left == left_water_level_name
        assert current_stage.water_level_right == right_water_level_name
