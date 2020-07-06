import pytest

from geolib.models.dsheetpiling.water_level import WaterLevel
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.internal import (
    _DEFAULT_WATER_LEVEL_NAME,
    WaterLevels,
    WaterLevel as InternalWaterLevel,
)


@pytest.fixture
def _model() -> DSheetPilingModel:
    model = DSheetPilingModel()
    model.add_stage(name="Initial stage")
    return model


class TestWaterLevels:
    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_phreatic_level_no_levels_provided_raises_value_error(
        self, _model: DSheetPilingModel
    ):
        with pytest.raises(ValueError) as e:
            _model.add_head_line()
        assert str(e.value) == "Provide either left or right water level"

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_phreatic_level_left(self, _model: DSheetPilingModel):
        water_level_name = "Ground water level -2m"
        level = -1
        water_level = WaterLevel(name=water_level_name, level=level)

        _model.add_head_line(left=water_level)

        # Validate [WATERLEVELS]
        assert isinstance(_model.datastructure.input_data.waterlevels, WaterLevels)
        assert len(_model.datastructure.input_data.waterlevels.levels) == 1
        internal = _model.datastructure.input_data.waterlevels.levels[0]
        assert isinstance(internal, InternalWaterLevel)
        assert internal.name == water_level_name
        assert internal.level == level

        # Validate [CONSTRUCTION STAGES]
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].water_level_left
            == water_level_name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                0
            ].water_level_right
            == _DEFAULT_WATER_LEVEL_NAME
        )

        # Validate validator (only one side has been set)
        with pytest.raises(ValueError):
            _model.is_valid

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_phreatic_level_right(self, _model: DSheetPilingModel):
        water_level_name = "Ground water level -2m"
        level = -1
        water_level = WaterLevel(name=water_level_name, level=level)

        _model.add_head_line(right=water_level)

        # Validate [WATERLEVELS]
        assert isinstance(_model.datastructure.input_data.waterlevels, WaterLevels)
        assert len(_model.datastructure.input_data.waterlevels.levels) == 1
        internal = _model.datastructure.input_data.waterlevels.levels[0]
        assert isinstance(internal, InternalWaterLevel)
        assert internal.name == water_level_name
        assert internal.level == level

        # Validate [CONSTRUCTION STAGES]
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].water_level_left
            == _DEFAULT_WATER_LEVEL_NAME
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                0
            ].water_level_right
            == water_level_name
        )

        # Validate validator (only one side has been set)
        with pytest.raises(ValueError):
            _model.is_valid

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_phreatic_level_left_and_right_different(
        self, _model: DSheetPilingModel
    ):
        water_level_name = "Ground water level -2m"
        name_left = water_level_name + " left"
        name_right = water_level_name + " right"
        level_left = 0
        level_right = -1
        water_level_left = WaterLevel(name=name_left, level=level_left)
        water_level_right = WaterLevel(name=name_right, level=level_right)

        _model.add_head_line(left=water_level_left, right=water_level_right)

        # Validate [WATERLEVELS]
        assert isinstance(_model.datastructure.input_data.waterlevels, WaterLevels)
        assert len(_model.datastructure.input_data.waterlevels.levels) == 2
        assert _model.datastructure.input_data.waterlevels.water_level_names == {
            name_left,
            name_right,
        }

        # Validate [CONSTRUCTION STAGES]
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].water_level_left
            == name_left
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                0
            ].water_level_right
            == name_right
        )

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_phreatic_level_left_and_right_same(
        self, _model: DSheetPilingModel
    ):
        water_level_name = "Ground water level -2m"
        level = -1
        water_level = WaterLevel(name=water_level_name, level=level)

        _model.add_head_line(left=water_level, right=water_level)

        # Validate [WATERLEVELS]
        assert isinstance(_model.datastructure.input_data.waterlevels, WaterLevels)
        assert len(_model.datastructure.input_data.waterlevels.levels) == 1
        internal = _model.datastructure.input_data.waterlevels.levels[0]
        assert _model.datastructure.input_data.waterlevels.water_level_names == {
            water_level_name
        }
        assert isinstance(internal, InternalWaterLevel)
        assert internal.name == water_level_name
        assert internal.level == level

        # Validate [CONSTRUCTION STAGES]
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].water_level_left
            == water_level_name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                0
            ].water_level_right
            == water_level_name
        )
