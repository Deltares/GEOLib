from contextlib import nullcontext as does_not_raise
from typing import Callable

import pytest
from pydantic import ValidationError

from geolib.geometry.one import Point
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.internal import _DEFAULT_SURFACE_NAME
from geolib.models.dsheetpiling.internal import Surface as InternalSurface
from geolib.models.dsheetpiling.internal import Surfaces
from geolib.models.dsheetpiling.settings import (
    LateralEarthPressureMethodStage,
    PassiveSide,
    Side,
)
from geolib.models.dsheetpiling.surface import Surface


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
def make_surface() -> Surface:
    def _make_surface(name: str):
        return Surface(name=name, points=[Point(x=0, z=0), Point(x=1, z=0)])

    return _make_surface


class TestSurfaces:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "points,run_expectation",
        [
            pytest.param([Point(x=0, z=0)], does_not_raise(), id="Single point"),
            pytest.param(
                [Point(x=0, z=0), Point(x=1, z=0)], does_not_raise(), id="Multiple points"
            ),
            pytest.param(
                [],
                pytest.raises(
                    ValidationError, match=r" List should have at least 1 item"
                ),
                id="No points",
            ),
            pytest.param(
                [Point(x=-1, z=0)],
                pytest.raises(
                    ValidationError,
                    match=r"All x-coordinates must be greater than or equal to 0, found",
                ),
                id="Negative x-coordinates",
            ),
            pytest.param(
                [Point(x=1, z=0)],
                pytest.raises(
                    ValidationError,
                    match=r"X-coordinate first point should be zero, received",
                ),
                id="First x-coordinate not zero",
            ),
            pytest.param(
                [Point(x=0, z=0), Point(x=10, z=0), Point(x=5, z=0)],
                pytest.raises(
                    ValidationError, match=r"x-coordinates must be strictly increasing"
                ),
                id="Not strictly increasing",
            ),
        ],
    )
    def test_surface_initialization_with_different_points_arguments(
        self, points: list[Point], run_expectation
    ):
        surface_name = "Ground level -2m"
        with run_expectation:
            Surface(name=surface_name, points=points)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_surface_invalid_stage_id_raises_ValueError(
        self, _model: DSheetPilingModel, make_surface: Callable
    ):
        surface = make_surface(name=_DEFAULT_SURFACE_NAME)
        invalid_stage_id = (
            len(_model.datastructure.input_data.construction_stages.stages) + 1
        )

        with pytest.raises(
            ValueError, match=r"Stage \d+ is not added to the internal datastructure"
        ):
            _model.add_surface(surface=surface, side=Side.BOTH, stage_id=invalid_stage_id)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side",
        [
            pytest.param(Side.LEFT, id="Left side"),
            pytest.param(Side.RIGHT, id="Right side"),
            pytest.param(Side.BOTH, id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_surface_internal_surfaces_updated(
        self, _model: DSheetPilingModel, make_surface: Callable, side: Side
    ):
        """Validate if surface is refered in [SURFACES]"""

        surface_name = "Ground level -2m"
        current_stage = _model.current_stage
        assert surface_name != _DEFAULT_SURFACE_NAME
        surface = make_surface(surface_name)

        # _model.add_surface(surface=surface, side=Side.LEFT, stage_id=0)
        _model.add_surface(surface=surface, side=side, stage_id=current_stage)

        assert isinstance(_model.datastructure.input_data.surfaces, Surfaces)
        assert len(_model.datastructure.input_data.surfaces.surfaces) == 1
        internal = _model.datastructure.input_data.surfaces.surfaces[current_stage]
        assert isinstance(internal, InternalSurface)
        assert internal.name == surface_name
        assert len(internal.points) == len(surface.points)
        for i, (point, internal_point) in enumerate(
            zip(surface.points, internal.points), start=1
        ):
            assert i == internal_point["Nr"]
            assert point.x == internal_point["X-coord"]
            assert point.z == internal_point["Value"]

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "side, left_surface_name, right_surface_name",
        [
            pytest.param(
                Side.LEFT, "Left surface", _DEFAULT_SURFACE_NAME, id="Left side"
            ),
            pytest.param(
                Side.RIGHT, _DEFAULT_SURFACE_NAME, "Right surface", id="Right side"
            ),
            pytest.param(Side.BOTH, "Same surface", "Same surface", id="Both sides"),
        ],
    )
    def test_dsheetpilingmodel_add_surface_internal_construction_stages(
        self,
        _model: DSheetPilingModel,
        make_surface: Callable,
        side: Side,
        left_surface_name: str,
        right_surface_name: str,
    ):
        """Validate if surface is refered in [CONSTRUCTION STAGES]"""
        current_stage = _model.current_stage

        if side == Side.LEFT:
            assert left_surface_name != _DEFAULT_SURFACE_NAME
            surface = make_surface(left_surface_name)
        elif side == Side.RIGHT:
            assert right_surface_name != _DEFAULT_SURFACE_NAME
            surface = make_surface(right_surface_name)
        else:
            assert left_surface_name == right_surface_name != _DEFAULT_SURFACE_NAME
            surface = make_surface(right_surface_name)

        _model.add_surface(surface=surface, side=side, stage_id=current_stage)

        assert (
            _model.datastructure.input_data.construction_stages.stages[
                current_stage
            ].surface_left
            == left_surface_name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[
                current_stage
            ].surface_right
            == right_surface_name
        )
