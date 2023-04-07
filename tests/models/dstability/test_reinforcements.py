from itertools import product

import pytest
from pydantic import ValidationError

from geolib.geometry.one import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    PersistableForbiddenLine,
    PersistableGeotextile,
    PersistableNail,
)
from geolib.models.dstability.reinforcements import (
    DStabilityReinforcement,
    ForbiddenLine,
    Geotextile,
    Nail,
)


@pytest.fixture
def _get_forbidden_line() -> ForbiddenLine:
    start = Point(x=0, z=0)
    end = Point(x=1, z=0)
    return ForbiddenLine(start=start, end=end)


@pytest.fixture
def _get_geotextile() -> Geotextile:
    start = Point(x=0, z=0)
    end = Point(x=1, z=0)
    return Geotextile(
        start=start, end=end, effective_tensile_strength=5, reduction_area=5
    )


@pytest.fixture
def _get_nail() -> Nail:
    location = Point(x=0, z=0)
    return Nail(location=location)


class TestDStabilityModel:  # TODO move to test_dsettlementmodel
    def test_no_reinforcement_provided(self):
        dstability_model = DStabilityModel(filename=None)

        class NotaDStabilityReinforcement:
            pass

        reinforcement = NotaDStabilityReinforcement()

        with pytest.raises(ValueError):
            dstability_model.add_reinforcement(
                reinforcement=reinforcement, scenario_index=0, stage_index=0
            )


class TestForbiddenLine:
    @pytest.mark.unittest
    def test_create_valid_forbiddenline(self, _get_forbidden_line):

        forbiddenline = _get_forbidden_line
        assert issubclass(type(forbiddenline), DStabilityReinforcement)

        dstability_datastructure = forbiddenline._to_internal_datastructure()

        assert isinstance(dstability_datastructure, PersistableForbiddenLine)

    @pytest.mark.unittest
    def test_create_forbiddenline_with_same_point_coordinates(self):
        start = end = Point(x=0, z=0)
        # TODO check if DStability allow sthis
        _ = ForbiddenLine(start=start, end=end)

    @pytest.mark.unittest
    def test_given_invalid_arguments_when_add_reinforcement_then_raises_value_error(
        self, _get_forbidden_line
    ):
        dstability_model = DStabilityModel(filename=None)
        forbiddenline = _get_forbidden_line

        with pytest.raises(ValueError):
            dstability_model.add_reinforcement(
                reinforcement=forbiddenline, scenario_index=0, stage_index=100
            )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "stage_index",
        [
            pytest.param(0, id="default stage id"),
            pytest.param(None, id="no stage_index argument"),
        ],
    )
    def test_add_reinforcement_forbiddenline(self, _get_forbidden_line, stage_index):
        dstability_model = DStabilityModel()
        stage_index = stage_index or 0

        forbiddenline = _get_forbidden_line

        dstability_model.add_reinforcement(
            reinforcement=forbiddenline, scenario_index=0, stage_index=stage_index
        )

        forbidden_lines_datastructure = dstability_model.datastructure.reinforcements[
            stage_index
        ].ForbiddenLines
        assert len(forbidden_lines_datastructure) == 1

        dstability_datastructure = forbidden_lines_datastructure[stage_index]

        assert isinstance(dstability_datastructure, PersistableForbiddenLine)

        assert dstability_datastructure.Start.X == forbiddenline.start.x
        assert dstability_datastructure.Start.Z == forbiddenline.start.z
        assert dstability_datastructure.End.X == forbiddenline.end.x
        assert dstability_datastructure.End.Z == forbiddenline.end.z


class TestGeotextile:
    @pytest.mark.unittest
    def test_create_valid_geotextile(self, _get_geotextile):
        geotextile = _get_geotextile
        assert issubclass(type(geotextile), DStabilityReinforcement)

    @pytest.mark.unittest
    def test_initialized_with_negative_tensile_strength(self, _get_geotextile):
        start = Point(x=0, z=0)
        end = Point(x=1, z=0)
        with pytest.raises(ValidationError):
            Geotextile(
                start=start, end=end, effective_tensile_strength=-5, reduction_area=5
            )

    @pytest.mark.unittest
    def test_initialized_with_negative_reduction_area(self):
        start = Point(x=0, z=0)
        end = Point(x=1, z=0)
        with pytest.raises(ValidationError):
            Geotextile(
                start=start, end=end, effective_tensile_strength=5, reduction_area=-5
            )

    @pytest.mark.unittest
    def test_given_invalid_arguments_when_add_reinforcement_then_raises_value_error(
        self, _get_geotextile
    ):
        dstability_model = DStabilityModel(filename=None)
        geotextile = _get_geotextile

        with pytest.raises(ValueError):
            dstability_model.add_reinforcement(reinforcement=geotextile, stage_index=100)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "stage_index",
        [
            pytest.param(0, id="default stage id"),
            pytest.param(None, id="no stage_index argument"),
        ],
    )
    def test_add_reinforcement_geotextile(self, _get_geotextile, stage_index):
        dstability_model = DStabilityModel()
        stage_index = stage_index or 0

        geotextile = _get_geotextile
        geotextile.label = "geotextile1"

        dstability_model.add_reinforcement(
            reinforcement=geotextile, stage_index=stage_index
        )

        geotextiles_datastructure = dstability_model.datastructure.reinforcements[
            stage_index
        ].Geotextiles
        assert len(geotextiles_datastructure) == 1

        dstability_datastructure = geotextiles_datastructure[stage_index]

        assert isinstance(dstability_datastructure, PersistableGeotextile)

        assert dstability_datastructure.Start.X == geotextile.start.x
        assert dstability_datastructure.Start.Z == geotextile.start.z
        assert dstability_datastructure.End.X == geotextile.end.x
        assert dstability_datastructure.End.Z == geotextile.end.z
        assert (
            dstability_datastructure.TensileStrength
            == geotextile.effective_tensile_strength
        )
        assert dstability_datastructure.ReductionArea == geotextile.reduction_area


class TestNail:
    @pytest.mark.unittest
    def test_create_valid_nail(self, _get_nail):
        nail = _get_nail

        assert issubclass(type(nail), DStabilityReinforcement)

        dstability_datastructure = nail._to_internal_datastructure()

        assert isinstance(dstability_datastructure, PersistableNail)
        assert dstability_datastructure.Label == nail.label
        assert dstability_datastructure.Location.X == nail.location.x
        assert dstability_datastructure.Location.Z == nail.location.z

    @pytest.mark.unittest
    def test_invalid_values_for_nail(self):
        greater_then_keys = {
            "length",
            "diameter",
            "grout_diameter",
            "bending_stiffness",
        }
        invalid_values = {0, -1}
        location = Point(x=0, z=0)

        for key, value in product(greater_then_keys, invalid_values):
            with pytest.raises(ValidationError):
                Nail(location=location, **{key: value})

    @pytest.mark.unittest
    def test_given_invalid_arguments_when_add_reinforcement_then_raises_value_error(
        self, _get_nail
    ):
        dstability_model = DStabilityModel(filename=None)
        nail = _get_nail

        with pytest.raises(ValueError):
            dstability_model.add_reinforcement(reinforcement=nail, stage_index=100)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "stage_index",
        [
            pytest.param(0, id="default stage id"),
            pytest.param(None, id="no stage_index argument"),
        ],
    )
    def test_add_reinforcement_nail(self, _get_nail, stage_index):
        dstability_model = DStabilityModel()
        stage_index = stage_index or 0
        nail = _get_nail

        dstability_model.add_reinforcement(
            reinforcement=nail, scenario_index=0, stage_index=stage_index
        )

        nails_datastructure = dstability_model.datastructure.reinforcements[
            stage_index
        ].Nails
        assert len(nails_datastructure) == 1

        dstability_datastructure = nails_datastructure[stage_index]

        assert isinstance(dstability_datastructure, PersistableNail)

        assert dstability_datastructure.Label == nail.label
        assert dstability_datastructure.Location.X == nail.location.x
        assert dstability_datastructure.Location.Z == nail.location.z
