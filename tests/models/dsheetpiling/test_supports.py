from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest
from pydantic import ValidationError

from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dsheetpiling.internal import _DEFAULT_PRE_STRESS
from geolib.models.dsheetpiling.internal import Anchor as InternalAnchor
from geolib.models.dsheetpiling.internal import Anchors
from geolib.models.dsheetpiling.internal import Strut as InternalStrut
from geolib.models.dsheetpiling.internal import Struts
from geolib.models.dsheetpiling.internal import Support as InternalSupport
from geolib.models.dsheetpiling.internal import SupportContainer
from geolib.models.dsheetpiling.settings import (
    LateralEarthPressureMethodStage,
    PassiveSide,
)
from geolib.models.dsheetpiling.supports import (
    Anchor,
    RigidSupport,
    SpringSupport,
    Strut,
    SupportType,
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
def _anchor() -> Anchor:
    return Anchor(name="Anchor 1", level=0)


@pytest.fixture
def _strut() -> Strut:
    return Strut(name="Strut 1", level=0)


class TestAnchor:
    @pytest.mark.parametrize(
        "argument,value",
        [
            pytest.param("name", "", id="Name too short"),
            pytest.param("name", "i" * 51, id="Name too long"),
            pytest.param("e_modulus", -1, id="Negative E-modulus"),
            pytest.param("cross_section", -1, id="Negative cross section area"),
            pytest.param("wall_height_kranz", -1, id="Negative wall height"),
            pytest.param("length", -1, id="Negative length"),
            pytest.param("yield_force", -1, id="Negative yield force"),
            pytest.param("side", "Not a side", id="None Side"),
        ],
    )
    def test_anchor_invalid_parameter_range_value_error(
        self, _model: DSheetPilingModel, argument: str, value: Any
    ):
        anchor_name = "Anchor 1"
        level = 0
        kwargs = {"name": anchor_name, "level": level, argument: value, "stage_id": 0}
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
    def test_dsheetpilingmodel_add_anchor_or_strut_no_invalid_support_provided_raises_value_error(
        self, _model: DSheetPilingModel
    ):
        with pytest.raises(ValueError):
            _model.add_anchor_or_strut(support=None, stage_id=0)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_anchor(
        self, _model: DSheetPilingModel, _anchor: Anchor
    ):
        _model.add_anchor_or_strut(
            support=_anchor, pre_stress=_DEFAULT_PRE_STRESS, stage_id=0
        )

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
        _model.add_anchor_or_strut(
            support=_anchor, pre_stress=pre_stress, stage_id=_model.current_stage
        )

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
            _model.add_anchor_or_strut(support=_anchor, pre_stress=pre_stress, stage_id=0)


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
            _model.add_anchor_or_strut(support=None, stage_id=0)

    @pytest.mark.integrationtest
    def test_dsheetpilingmodel_add_strut(self, _model: DSheetPilingModel, _strut: Strut):
        _model.add_anchor_or_strut(
            support=_strut, pre_stress=_DEFAULT_PRE_STRESS, stage_id=0
        )

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
        _model.add_anchor_or_strut(support=_strut, pre_stress=pre_stress, stage_id=0)

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
            _model.add_anchor_or_strut(support=_strut, pre_stress=pre_stress, stage_id=0)


class TestSpringSupport:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("Correct name"),
        ],
    )
    @pytest.mark.parametrize(
        "level",
        [
            pytest.param(10, id="Valid level as int"),
            pytest.param(10.0, id="Valid level as float"),
        ],
    )
    @pytest.mark.parametrize(
        "rotational_stiffness",
        [
            pytest.param(0.0, id="Valid zero rotational stiffness"),
            pytest.param(10, id="Valid rotational stiffness as int"),
            pytest.param(10.0, id="Valid rotational stiffness as float"),
        ],
    )
    @pytest.mark.parametrize(
        "translational_stiffness",
        [
            pytest.param(0.0, id="Valid zero translational stiffness"),
            pytest.param(10, id="Valid translational stiffness as int"),
            pytest.param(10.0, id="Valid translational stiffness as float"),
        ],
    )
    def test_intialization_spring_support(
        self,
        name: str,
        level: float,
        rotational_stiffness: float,
        translational_stiffness: float,
    ):
        support = SpringSupport(
            name=name,
            level=level,
            rotational_stiffness=rotational_stiffness,
            translational_stiffness=translational_stiffness,
        )

        internal = support.to_internal()

        assert isinstance(internal, InternalSupport)
        assert support.name == internal.name
        assert support.level == internal.level
        assert support.rotational_stiffness == internal.rotational_stiffness
        assert support.translational_stiffness == internal.translational_stiffness

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "argument,value,raising_context",
        [
            pytest.param(
                "name",
                "i" * 51,
                pytest.raises(
                    ValidationError, match=r"ensure this value has at most 50 characters"
                ),
                id="Name too long",
            ),
            pytest.param(
                "rotational_stiffness",
                -1,
                pytest.raises(
                    ValidationError,
                    match=r"ensure this value is greater than or equal to 0",
                ),
                id="Name too long",
            ),
            pytest.param(
                "translational_stiffness",
                -1,
                pytest.raises(
                    ValidationError,
                    match=r"ensure this value is greater than or equal to 0",
                ),
                id="Negative translational stiffness",
            ),
        ],
    )
    def test_intialization_spring_support_invalid_input_raises(
        self,
        argument: str,
        value: Any,
        raising_context,
    ):
        valid_kwargs = {
            "name": "Valid name",
            "level": -5,
            "rotational_stiffness": 10,
            "translational_stiffness": 10,
        }
        valid_kwargs[argument] = value

        with raising_context:
            SpringSupport(**valid_kwargs)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("Correct name"),
        ],
    )
    @pytest.mark.parametrize(
        "level",
        [
            pytest.param(10, id="Valid level as int"),
            pytest.param(10.0, id="Valid level as float"),
        ],
    )
    @pytest.mark.parametrize(
        "rotational_stiffness",
        [
            pytest.param(0.0, id="Valid zero rotational stiffness"),
            pytest.param(10, id="Valid rotational stiffness as int"),
            pytest.param(10.0, id="Valid rotational stiffness as float"),
        ],
    )
    @pytest.mark.parametrize(
        "translational_stiffness",
        [
            pytest.param(0.0, id="Valid zero translational stiffness"),
            pytest.param(10, id="Valid translational stiffness as int"),
            pytest.param(10.0, id="Valid translational stiffness as float"),
        ],
    )
    def test_dsheetpilingmodel_add_support(
        self,
        _model: DSheetPilingModel,
        name: str,
        level: float,
        rotational_stiffness: float,
        translational_stiffness: float,
    ):
        support = SpringSupport(
            name=name,
            level=level,
            rotational_stiffness=rotational_stiffness,
            translational_stiffness=translational_stiffness,
        )
        current_stage = _model.current_stage
        _model.add_support(support=support, stage_id=current_stage)

        # Validate [RIGID SUPPORTS]
        assert isinstance(
            _model.datastructure.input_data.spring_supports, SupportContainer
        )
        assert len(_model.datastructure.input_data.spring_supports.supports) == 1
        internal = _model.datastructure.input_data.spring_supports.supports[0]
        assert isinstance(internal, InternalSupport)
        assert internal.name == support.name
        assert internal.level == support.level
        assert rotational_stiffness == internal.rotational_stiffness
        assert translational_stiffness == internal.translational_stiffness

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(
                _model.datastructure.input_data.construction_stages.stages[
                    0
                ].spring_supports
            )
            == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].spring_supports[
                0
            ]
            == support.name
        )


class TestRigidSupport:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("Correct name"),
        ],
    )
    @pytest.mark.parametrize(
        "level",
        [
            pytest.param(10, id="Valid level as int"),
            pytest.param(10.0, id="Valid level as float"),
        ],
    )
    @pytest.mark.parametrize(
        "support_type, translational_stiffness, rotational_stiffness",
        [
            pytest.param(SupportType.TRANSLATION, 1, 0, id="Translation support type"),
            pytest.param(SupportType.ROTATION, 0, 1, id="Rotation support type"),
            pytest.param(
                SupportType.TRANSLATION_AND_ROTATION,
                1,
                1,
                id="Translation and rotation support type",
            ),
        ],
    )
    def test_intialization_rigid_support(
        self,
        name: str,
        level: float,
        support_type: SupportType,
        rotational_stiffness: int,
        translational_stiffness: int,
    ):
        support = RigidSupport(
            name=name,
            level=level,
            support_type=support_type,
        )

        internal = support.to_internal()

        assert isinstance(internal, InternalSupport)
        assert support.name == internal.name
        assert support.level == internal.level
        assert rotational_stiffness == internal.rotational_stiffness
        assert translational_stiffness == internal.translational_stiffness

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "argument,value,raising_context",
        [
            pytest.param(
                "name",
                "i" * 51,
                pytest.raises(
                    ValidationError, match=r"ensure this value has at most 50 characters"
                ),
                id="Name too long",
            ),
            pytest.param(
                "support_type",
                5,
                pytest.raises(
                    ValidationError,
                    match=r"value is not a valid enumeration member; permitted: 1, 2, 3",
                ),
                id="Name too long",
            ),
        ],
    )
    def test_intialization_rigid_support_invalid_input_raises(
        self,
        argument: str,
        value: Any,
        raising_context,
    ):
        valid_kwargs = {
            "name": "Valid name",
            "level": -5,
            "support_type": SupportType.TRANSLATION,
        }
        valid_kwargs[argument] = value

        with raising_context:
            RigidSupport(**valid_kwargs)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("Correct name"),
        ],
    )
    @pytest.mark.parametrize(
        "level",
        [
            pytest.param(10, id="Valid level as int"),
            pytest.param(10.0, id="Valid level as float"),
        ],
    )
    @pytest.mark.parametrize(
        "support_type, translational_stiffness, rotational_stiffness",
        [
            pytest.param(SupportType.TRANSLATION, 1, 0, id="Translation support type"),
            pytest.param(SupportType.ROTATION, 0, 1, id="Rotation support type"),
            pytest.param(
                SupportType.TRANSLATION_AND_ROTATION,
                1,
                1,
                id="Translation and rotation support type",
            ),
        ],
    )
    def test_dsheetpilingmodel_add_support(
        self,
        _model: DSheetPilingModel,
        name: str,
        level: float,
        support_type: SupportType,
        rotational_stiffness: int,
        translational_stiffness: int,
    ):
        support = RigidSupport(
            name=name,
            level=level,
            support_type=support_type,
        )
        current_stage = _model.current_stage
        _model.add_support(support=support, stage_id=current_stage)

        # Validate [RIGID SUPPORTS]
        assert isinstance(
            _model.datastructure.input_data.rigid_supports, SupportContainer
        )
        assert len(_model.datastructure.input_data.rigid_supports.supports) == 1
        internal = _model.datastructure.input_data.rigid_supports.supports[0]
        assert isinstance(internal, InternalSupport)
        assert internal.name == support.name
        assert internal.level == support.level
        assert rotational_stiffness == internal.rotational_stiffness
        assert translational_stiffness == internal.translational_stiffness

        # Validate [CONSTRUCTION STAGES]
        assert len(_model.datastructure.input_data.construction_stages.stages) == 1
        assert (
            len(
                _model.datastructure.input_data.construction_stages.stages[
                    0
                ].rigid_supports
            )
            == 1
        )
        assert (
            _model.datastructure.input_data.construction_stages.stages[0].rigid_supports[
                0
            ]
            == support.name
        )
