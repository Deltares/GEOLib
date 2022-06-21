from contextlib import nullcontext as does_not_raise
from typing import Callable, List

import pytest
from pydantic import ValidationError

from geolib.geometry.one import Point
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.internal import _DEFAULT_SOIL_PROFILE_NAME
from geolib.models.dsheetpiling.internal import SoilProfile as InternalProfile
from geolib.models.dsheetpiling.internal import SoilProfiles
from geolib.models.dsheetpiling.profiles import SoilLayer, SoilProfile
from geolib.models.dsheetpiling.settings import (
    CurveSettings,
    LateralEarthPressureMethodStage,
    ModulusReactionType,
    PassiveSide,
    Side,
)
from geolib.soils import Soil

_SOIL_TEST_NAME_1: str = "Clay"
_SOIL_TEST_NAME_2: str = "Sand"
_PROFILE_TEST_NAME: str = "test profiel"
_PROFILE_TEST_COORDINATES: Point = Point(x=100, y=250)
_TEST_LAYERS: List[SoilLayer] = [
    SoilLayer(top_of_layer=0, soil=_SOIL_TEST_NAME_1),
    SoilLayer(top_of_layer=-2, soil=_SOIL_TEST_NAME_2),
]


@pytest.fixture
def _model() -> DSheetPilingModel:
    model = DSheetPilingModel()
    model.add_stage(
        name="Initial stage",
        passive_side=PassiveSide.DSHEETPILING_DETERMINED,
        method_left=LateralEarthPressureMethodStage.KA_KO_KP,
        method_right=LateralEarthPressureMethodStage.KA_KO_KP,
    )
    model.add_soil(Soil(name=_SOIL_TEST_NAME_1))
    model.add_soil(Soil(name=_SOIL_TEST_NAME_2))
    return model


@pytest.fixture
def make_profile() -> SoilProfile:
    def _make_profile(name: str):
        return SoilProfile(
            name=name, layers=_TEST_LAYERS, coordinate=_PROFILE_TEST_COORDINATES
        )

    return _make_profile


class TestCurveSettings:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "modulus_reaction_type",
        [
            pytest.param(ModulusReactionType.TANGENT),
            pytest.param(ModulusReactionType.SECANT),
        ],
    )
    @pytest.mark.parametrize(
        "use_unloading_reloading_curve",
        [
            pytest.param(True),
            pytest.param(False),
        ],
    )
    @pytest.mark.parametrize(
        "curve_number,raising_context",
        [
            pytest.param(
                0,
                pytest.raises(
                    ValidationError,
                    match=r"ensure this value is greater than or equal to 1",
                ),
                id="Lower than allowed",
            ),
            pytest.param(1, does_not_raise()),
            pytest.param(2, does_not_raise()),
            pytest.param(3, does_not_raise()),
            pytest.param(4, does_not_raise()),
            pytest.param(
                5,
                pytest.raises(
                    ValidationError, match=r"ensure this value is less than or equal to 4"
                ),
                id="Higher than allowed",
            ),
        ],
    )
    def test_curve_settings(
        self,
        modulus_reaction_type: ModulusReactionType,
        use_unloading_reloading_curve: bool,
        curve_number: int,
        raising_context,
    ):
        with raising_context:
            CurveSettings(
                modulus_reaction_type=modulus_reaction_type,
                use_unloading_reloading_curve=use_unloading_reloading_curve,
                curve_number=curve_number,
            )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "modulus_reaction_type",
        [
            pytest.param(ModulusReactionType.TANGENT),
            pytest.param(ModulusReactionType.SECANT),
        ],
    )
    @pytest.mark.parametrize(
        "use_unloading_reloading_curve",
        [
            pytest.param(True),
            pytest.param(False),
        ],
    )
    @pytest.mark.parametrize(
        "curve_number",
        [pytest.param(1), pytest.param(2), pytest.param(3), pytest.param(4)],
    )
    def test_dsheetpilingmodel_add_curve_settings_internal_soil_profiles_updated(
        self,
        _model: DSheetPilingModel,
        modulus_reaction_type: ModulusReactionType,
        use_unloading_reloading_curve: bool,
        curve_number: int,
    ):
        """Validate if curve settings are refered in [SOIL PROFILES]"""

        curve_settings = CurveSettings(
            modulus_reaction_type=modulus_reaction_type,
            use_unloading_reloading_curve=use_unloading_reloading_curve,
            curve_number=curve_number,
        )
        _model.set_curve_settings(curve_settings=curve_settings)

        assert isinstance(_model.datastructure.input_data.soil_profiles, SoilProfiles)
        assert (
            _model.datastructure.input_data.soil_profiles.modulus_reaction_type
            == modulus_reaction_type.value
        )
        assert (
            _model.datastructure.input_data.soil_profiles.use_unloading_reloading_curve
            == use_unloading_reloading_curve
        )
        assert _model.datastructure.input_data.soil_profiles.curve_number == curve_number


class TestSoilProfile:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "layers,raise_context",
        [
            pytest.param(
                [SoilLayer(top_of_layer=0, soil=_SOIL_TEST_NAME_1)],
                does_not_raise(),
                id="Single layer",
            ),
            pytest.param(
                [
                    SoilLayer(top_of_layer=0, soil=_SOIL_TEST_NAME_1),
                    SoilLayer(top_of_layer=-2, soil=_SOIL_TEST_NAME_2),
                ],
                does_not_raise(),
                id="Multiple layers",
            ),
            pytest.param(
                [],
                pytest.raises(
                    ValidationError, match=r"ensure this value has at least 1 items"
                ),
                id="No layers",
            ),
            pytest.param(
                [
                    SoilLayer(top_of_layer=0, soil=_SOIL_TEST_NAME_1),
                    SoilLayer(top_of_layer=2, soil=_SOIL_TEST_NAME_2),
                ],
                pytest.raises(
                    ValidationError,
                    match=r"Top of layer must decrease with each layer along depth. Top of layers: ",
                ),
                id="Multiple layers, top of layer not decreasing",
            ),
        ],
    )
    def test_profile_initialization_with_different_points_arguments(
        self, layers: List[SoilLayer], raise_context
    ):
        with raise_context:
            profile = SoilProfile(name=_PROFILE_TEST_NAME, layers=layers)
        try:
            internal = profile.to_internal()
        except UnboundLocalError:
            return

        assert profile.name == internal.name
        assert profile.coordinate.x == internal.coordinate.x
        assert profile.coordinate.y == internal.coordinate.y
        assert profile.coordinate.z == internal.coordinate.z

        assert len(profile.layers) == len(internal.layers)
        for layer, internal_layer in zip(profile.layers, internal.layers):
            assert layer.top_of_layer == internal_layer.top_of_layer
            assert layer.soil == internal_layer.soil
            assert layer.water_pressure_top == internal_layer.water_pressure_top
            assert layer.water_pressure_bottom == internal_layer.water_pressure_bottom

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_profile_soil_unknown_raises_ValueError(
        self, _model: DSheetPilingModel
    ):
        current_stage = _model.current_stage
        name_not_in_soil_collection = "not in soil collection"
        layers = [SoilLayer(top_of_layer=0, soil=name_not_in_soil_collection)]
        profile = SoilProfile(name=_PROFILE_TEST_NAME, layers=layers)

        assert (
            name_not_in_soil_collection
            not in _model.datastructure.input_data.soil_collection.soil_names
        )

        with pytest.raises(ValueError):
            _model.add_profile(profile=profile, side=Side.BOTH, stage_id=current_stage)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_profile_invalid_stage_id_raises_ValueError(
        self, _model: DSheetPilingModel, make_profile: Callable
    ):
        profile = make_profile(name=_PROFILE_TEST_NAME)
        invalid_stage_id = (
            len(_model.datastructure.input_data.construction_stages.stages) + 1
        )

        with pytest.raises(
            ValueError, match=r"Stage \d+ is not added to the internal datastructure"
        ):
            _model.add_profile(profile=profile, side=Side.BOTH, stage_id=invalid_stage_id)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side",
        [
            pytest.param(Side.LEFT, id="Left side"),
            pytest.param(Side.RIGHT, id="Right side"),
            pytest.param(Side.BOTH, id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_profile_internal_soil_profiles_updated(
        self, _model: DSheetPilingModel, make_profile: Callable, side: Side
    ):
        """Validate if profile is refered in [SOIL PROFILES]"""

        profile_name = _PROFILE_TEST_NAME
        current_stage = _model.current_stage
        assert profile_name != _DEFAULT_SOIL_PROFILE_NAME
        profile = make_profile(profile_name)

        _model.add_profile(profile=profile, side=side, stage_id=current_stage)

        assert isinstance(_model.datastructure.input_data.soil_profiles, SoilProfiles)
        assert len(_model.datastructure.input_data.soil_profiles.soil_profiles) == 1
        internal = _model.datastructure.input_data.soil_profiles.soil_profiles[
            current_stage
        ]
        assert isinstance(internal, InternalProfile)
        assert internal.name == _PROFILE_TEST_NAME
        assert len(profile.layers) == len(internal.layers)
        for layer, internal_layer in zip(profile.layers, internal.layers):
            assert layer.dict() == internal_layer.dict()
        assert profile.coordinate.x == internal.coordinate.x
        assert profile.coordinate.y == internal.coordinate.y

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side, left_profile_name, right_profile_name",
        [
            pytest.param(
                Side.LEFT, "Left profile", _DEFAULT_SOIL_PROFILE_NAME, id="Left side"
            ),
            pytest.param(
                Side.RIGHT, _DEFAULT_SOIL_PROFILE_NAME, "Right profile", id="Right side"
            ),
            pytest.param(Side.BOTH, "Same profile", "Same profile", id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_profile_internal_construction_stages(
        self,
        _model: DSheetPilingModel,
        make_profile: Callable,
        side: Side,
        left_profile_name: str,
        right_profile_name: str,
    ):
        """Validate if profile is refered in [CONSTRUCTION STAGES]"""
        current_stage = _model.current_stage
        if side == Side.LEFT:
            assert left_profile_name != _DEFAULT_SOIL_PROFILE_NAME
            profile = make_profile(left_profile_name)
        elif side == Side.RIGHT:
            assert right_profile_name != _DEFAULT_SOIL_PROFILE_NAME
            profile = make_profile(right_profile_name)
        else:
            assert left_profile_name == right_profile_name != _DEFAULT_SOIL_PROFILE_NAME
            profile = make_profile(right_profile_name)

        _model.add_profile(profile=profile, side=side, stage_id=current_stage)

        assert (
            _model.datastructure.input_data.construction_stages.stages[
                current_stage
            ].soil_profile_left
            == left_profile_name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                current_stage
            ].soil_profile_right
            == right_profile_name
        )
