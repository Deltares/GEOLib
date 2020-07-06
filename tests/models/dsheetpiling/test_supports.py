import pytest
from typing import Any

from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.supports import Anchor, RigidSupport, SpringSupport, Strut
from geolib.models.dsheetpiling.internal import (
    _DEFAULT_PRE_STRESS,
    Anchors,
    Anchor as InternalAnchor,
    Struts,
    Strut as InternalStrut,
)
from pydantic import ValidationError


@pytest.fixture
def _model() -> DSheetPilingModel:
    model = DSheetPilingModel()
    model.add_stage(name="Initial stage")
    return model


@pytest.fixture
def _anchor() -> Anchor:
    return Anchor(name="Anchor 1", level=0)


@pytest.fixture
def _strut() -> Strut:
    return Strut(name="Strut 1", level=0)


class TestAnchor:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "argument,value",
        [
            pytest.param("name", "", id="Name too short"),
            pytest.param("name", "i" * 51, id="Name too long"),
            pytest.param("e_modulus", -1, id="Negative E-modulus"),
            pytest.param("cross_section", -1, id="Negative cross section area"),
            pytest.param("wall_height_kranz", -1, id="Negative wall height"),
            pytest.param("length", -1, id="Negative length"),
            pytest.param("angle", -1, id="Negative angle"),
            pytest.param("yield_force", -1, id="Negative yield force"),
            pytest.param("side", "Not a side", id="None Side"),
        ],
    )
    def test_anchor_invalid_parameter_range_value_error(
        self, _model: DSheetPilingModel, argument: str, value: Any
    ):
        anchor_name = "Anchor 1"
        level = 0
        kwargs = {"name": anchor_name, "level": level, argument: value}
        with pytest.raises(ValidationError):
            Anchor(**kwargs)

    @pytest.mark.unittest
    def test_anchor_with_valid_input(self, _model: DSheetPilingModel):
        anchor_name = "Anchor 1"
        level = 0

        anchor = Anchor(name=anchor_name, level=level)
        internal = anchor.to_internal()
        assert isinstance(internal, InternalAnchor)

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_anchor_no_support_provided_raises_value_error(
        self, _model: DSheetPilingModel
    ):
        with pytest.raises(ValueError):
            _model.add_support(support=None)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_anchor(
        self, _model: DSheetPilingModel, _anchor: Anchor
    ):
        _model.add_support(support=_anchor)

        # Validate [ANCHORS]
        assert isinstance(_model.datastructure.input_data.anchors, Anchors)
        assert len(_model.datastructure.input_data.anchors.anchors) == 1
        internal = _model.datastructure.input_data.anchors.anchors[0]
        assert isinstance(internal, InternalAnchor)
        assert internal.name == _anchor.name
        assert internal.level == _anchor.level

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(_model.datastructure.input_data.construction_stages.stages[0].anchors)
            == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].anchors[0].name
            == _anchor.name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0]
            .anchors[0]
            .pre_stress
            == _DEFAULT_PRE_STRESS
        )

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_anchor_with_valid_pre_stress(
        self, _model: DSheetPilingModel, _anchor: Anchor
    ):
        pre_stress = 10
        _model.add_support(support=_anchor, pre_stress=pre_stress)

        # Validate [ANCHORS]
        assert isinstance(_model.datastructure.input_data.anchors, Anchors)
        assert len(_model.datastructure.input_data.anchors.anchors) == 1
        internal = _model.datastructure.input_data.anchors.anchors[0]
        assert isinstance(internal, InternalAnchor)
        assert internal.name == _anchor.name
        assert internal.level == _anchor.level

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(_model.datastructure.input_data.construction_stages.stages[0].anchors)
            == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].anchors[0].name
            == _anchor.name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0]
            .anchors[0]
            .pre_stress
            == pre_stress
        )

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_anchor_with_invalid_pre_stress_raises_validation_error(
        self, _model: DSheetPilingModel, _anchor: Anchor
    ):
        pre_stress = -10

        with pytest.raises(ValidationError):
            _model.add_support(support=_anchor, pre_stress=pre_stress)


class TestStrut:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "argument,value",
        [
            pytest.param("name", "", id="Name too short"),
            pytest.param("name", "i" * 51, id="Name too long"),
            pytest.param("e_modulus", -1, id="Negative E-modulus"),
            pytest.param("cross_section", -1, id="Negative cross section area"),
            pytest.param("length", -1, id="Negative length"),
            pytest.param("angle", -1, id="Negative angle"),
            pytest.param("buckling_force", -1, id="Negative buckling force"),
            pytest.param("side", "Not a side", id="None Side"),
            pytest.param("pre_compression", -1, id="Negative pre compression"),
        ],
    )
    def test_strut_invalid_parameter_range_value_error(
        self, _model: DSheetPilingModel, argument: str, value: Any
    ):
        strut_name = "Strut 1"
        level = 0
        kwargs = {"name": strut_name, "level": level, argument: value}
        with pytest.raises(ValidationError):
            Strut(**kwargs)

    @pytest.mark.unittest
    def test_strut_with_valid_input(self, _model: DSheetPilingModel):
        strut_name = "Strut 1"
        level = 0

        strut = Strut(name=strut_name, level=level)
        internal = strut.to_internal()
        assert isinstance(internal, InternalStrut)

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_strut_no_support_provided_raises_value_error(
        self, _model: DSheetPilingModel
    ):
        with pytest.raises(ValueError):
            _model.add_support(support=None)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_strut(self, _model: DSheetPilingModel, _strut: Strut):
        _model.add_support(support=_strut)

        # Validate [ANCHORS]
        assert isinstance(_model.datastructure.input_data.struts, Struts)
        assert len(_model.datastructure.input_data.struts.struts) == 1
        internal = _model.datastructure.input_data.struts.struts[0]
        assert isinstance(internal, InternalStrut)
        assert internal.name == _strut.name
        assert internal.level == _strut.level

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(_model.datastructure.input_data.construction_stages.stages[0].struts) == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].struts[0].name
            == _strut.name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0]
            .struts[0]
            .pre_stress
            == _DEFAULT_PRE_STRESS
        )

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_strut_with_valid_pre_stress(
        self, _model: DSheetPilingModel, _strut: Strut
    ):
        pre_stress = 10
        _model.add_support(support=_strut, pre_stress=pre_stress)

        # Validate [ANCHORS]
        assert isinstance(_model.datastructure.input_data.struts, Struts)
        assert len(_model.datastructure.input_data.struts.struts) == 1
        internal = _model.datastructure.input_data.struts.struts[0]
        assert isinstance(internal, InternalStrut)
        assert internal.name == _strut.name
        assert internal.level == _strut.level

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(_model.datastructure.input_data.construction_stages.stages[0].struts) == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].struts[0].name
            == _strut.name
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0]
            .struts[0]
            .pre_stress
            == pre_stress
        )

    @pytest.mark.unittest
    def test_dsheetpilingmodel_add_strut_with_invalid_pre_stress_raises_validation_error(
        self, _model: DSheetPilingModel, _strut: Strut
    ):
        pre_stress = -10

        with pytest.raises(ValidationError):
            _model.add_support(support=_strut, pre_stress=pre_stress)
