"""Pile Library for D-Foundations.

"""
from enum import Enum
from typing import Optional

from pydantic.types import PositiveInt, confloat, constr

from geolib.geometry import Point
from geolib.models import BaseDataClass

from .internal import (
    BearingPileSlipLayer,
    LoadSettlementCurve,
    PileMaterial,
    PileShape,
    PileType,
    PileTypeForClayLoamPeat,
    PositionBearingPile,
    PositionTensionPile,
    TypesBearingPiles,
    TypesTensionPiles,
)


class PileLocation(BaseDataClass):
    """Base Class for Pile location."""

    pile_name: constr(min_length=0, max_length=10) = ""
    point: Point
    pile_head_level: confloat(ge=-1000, le=1000)
    limit_state_str: confloat(ge=0, le=100000)
    limit_state_service: confloat(ge=0, le=100000)

    def _to_internal(self, index: PositiveInt):
        return {
            "index": index,
            "pile_name": "'" + self.pile_name + "'",
            "x_coordinate": self.point.x,
            "y_coordinate": self.point.y,
            "pile_head_level": self.pile_head_level,
            "limit_state_str": self.limit_state_str,
            "limit_state_service": self.limit_state_service,
        }


class BearingPileLocation(PileLocation):
    """Inherits :class:`~geolib.models.dfoundations.piles.PileLocation`."""

    surcharge: confloat(ge=0, le=100000)

    def _to_internal(self, index: PositiveInt):
        pile_location = super()._to_internal(index)
        return PositionBearingPile(**pile_location, surcharge=self.surcharge)


class TensionPileLocation(PileLocation):
    """Inherits :class:`~geolib.models.dfoundations.piles.PileLocation`."""

    use_alternating_loads: bool
    max_force: confloat(ge=-100000, le=100000)
    min_force: confloat(ge=-100000, le=100000)

    def _to_internal(self, index: PositiveInt):
        pile_location = super()._to_internal(index)
        return PositionTensionPile(
            **pile_location,
            use_alternating_loads=self.use_alternating_loads,
            max_force=self.max_force,
            min_force=self.min_force,
        )


class BasePileType(Enum):
    """Supported pile types enum"""

    USER_DEFINED_VIBRATING = PileType.USER_DEFINED_VIBRATING.value
    USER_DEFINED_LOW_VIBRATING = PileType.USER_DEFINED_LOW_VIBRATING.value


class BasePileTypeForClayLoamPeat(Enum):
    """Pile types for clay loam and peat enum"""

    STANDARD = PileTypeForClayLoamPeat.STANDARD.value
    USER_DEFINED = PileTypeForClayLoamPeat.USER_DEFINED.value


class Pile(BaseDataClass):
    """Base Class for Piles."""

    pile_name: str
    pile_type: BasePileType
    pile_class_factor_shaft_sand_gravel: confloat(ge=0, le=9)
    pile_class_factor_shaft_clay_loam_peat: Optional[confloat(ge=0, le=9)]
    preset_pile_class_factor_shaft_clay_loam_peat: BasePileTypeForClayLoamPeat
    elasticity_modulus: confloat(ge=0, le=1e25)


class BearingPile(Pile):
    """Inherits :class:`~geolib.models.dfoundations.piles.Pile`."""

    pile_class_factor_tip: confloat(ge=0, le=9)
    load_settlement_curve: LoadSettlementCurve
    user_defined_pile_type_as_prefab: bool
    use_manual_reduction_for_qc: bool
    reduction_percentage_qc: confloat(ge=25, le=100) = 25
    characteristic_adhesion: confloat(ge=0, le=1000)

    overrule_pile_tip_shape_factor: bool
    pile_tip_shape_factor: Optional[confloat(ge=0, le=10)]
    overrule_pile_tip_cross_section_factors: bool
    pile_tip_cross_section_factor: Optional[confloat(ge=0, le=10)]

    def _to_internal(self):
        return TypesBearingPiles(
            pile_name=self.pile_name,
            pile_type=self.pile_type.value,
            pile_type_for_execution_factor_sand_gravel=PileType.USER_DEFINED,
            execution_factor_sand_gravel=self.pile_class_factor_shaft_sand_gravel,
            pile_type_for_execution_factor_clay_loam_peat=(
                self.preset_pile_class_factor_shaft_clay_loam_peat.value
            ),
            execution_factor_clay_loam_peat=self.pile_class_factor_shaft_clay_loam_peat,
            pile_type_for_pile_class_factor=PileType.USER_DEFINED,
            pile_class_factor=self.pile_class_factor_tip,
            pile_type_for_load_settlement_curve=self.load_settlement_curve,
            user_defined_pile_type_as_prefab=self.user_defined_pile_type_as_prefab,
            use_manual_reduction_for_qc=self.use_manual_reduction_for_qc,
            reduction_percentage_qc=self.reduction_percentage_qc,
            material=PileMaterial.USER_DEFINED,
            elasticity_modulus=self.elasticity_modulus,
            slip_layer=BearingPileSlipLayer.USER_DEFINED,
            characteristic_adhesion=self.characteristic_adhesion,
            overrule_pile_tip_shape_factor=self.overrule_pile_tip_shape_factor,
            pile_tip_shape_factor=self.pile_tip_shape_factor,
            overrule_pile_tip_cross_section_factors=(
                self.overrule_pile_tip_cross_section_factors
            ),
            pile_tip_cross_section_factor=self.pile_tip_cross_section_factor,
            is_user_defined=True,
            use_pre_2016=False,
        )


class TensionPile(Pile):
    """Inherits :class:`~geolib.models.dfoundations.piles.Pile`."""

    unit_weight_pile: confloat(ge=0, le=1000)

    def _to_internal(self):
        return TypesTensionPiles(
            pile_name=self.pile_name,
            pile_type_for_execution_factor_sand_gravel=self.pile_type.value,
            execution_factor_sand_gravel=self.pile_class_factor_shaft_sand_gravel,
            pile_type_for_execution_factor_clay_loam_peat=(
                self.preset_pile_class_factor_shaft_clay_loam_peat.value
            ),
            execution_factor_clay_loam_peat=self.pile_class_factor_shaft_clay_loam_peat,
            material=PileMaterial.USER_DEFINED,
            unit_weight_pile=self.unit_weight_pile,
            elasticity_modulus=self.elasticity_modulus,
        )


class BearingRoundPile(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.diameter = self.diameter
        types_bearing_pile.shape = PileShape.ROUND_PILE
        return types_bearing_pile


class TensionRoundPile(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.diameter = self.diameter
        types_tension_pile.shape = PileShape.ROUND_PILE
        return types_tension_pile


class BearingRectangularPile(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_width: confloat(ge=0, le=100)
    base_length: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_width = self.base_width
        types_bearing_pile.base_length = self.base_length
        types_bearing_pile.shape = PileShape.RECTANGULAR_PILE
        return types_bearing_pile


class TensionRectangularPile(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    base_width: confloat(ge=0, le=100)
    base_length: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.base_width = self.base_width
        types_tension_pile.base_length = self.base_length
        types_tension_pile.shape = PileShape.RECTANGULAR_PILE
        return types_tension_pile


class BearingRoundPileWithEnlargedBase(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_diameter = self.base_diameter
        types_bearing_pile.pile_diameter = self.pile_diameter
        types_bearing_pile.base_height = self.base_height
        types_bearing_pile.shape = PileShape.ROUND_PILE_WITH_ENLARGED_BASE
        return types_bearing_pile


class TensionRoundPileWithEnlargedBase(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.base_diameter = self.base_diameter
        types_tension_pile.pile_diameter = self.pile_diameter
        types_tension_pile.base_height = self.base_height
        types_tension_pile.shape = PileShape.ROUND_PILE_WITH_ENLARGED_BASE
        return types_tension_pile


class BearingRectangularPileWithEnlargedBase(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_width_v: confloat(ge=0, le=100)
    base_length_v: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)
    shaft_width: confloat(ge=0, le=100)
    shaft_length: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_width_v = self.base_width_v
        types_bearing_pile.base_length_v = self.base_length_v
        types_bearing_pile.base_height = self.base_height
        types_bearing_pile.shaft_width = self.shaft_width
        types_bearing_pile.shaft_length = self.shaft_length
        types_bearing_pile.shape = PileShape.RECTANGULAR_PILE_WITH_ENLARGED_BASE
        return types_bearing_pile


class TensionRectangularPileWithEnlargedBase(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    base_width_v: confloat(ge=0, le=100)
    base_length_v: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)
    shaft_width: confloat(ge=0, le=100)
    shaft_length: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.base_width_v = self.base_width_v
        types_tension_pile.base_length_v = self.base_length_v
        types_tension_pile.base_height = self.base_height
        types_tension_pile.shaft_width = self.shaft_width
        types_tension_pile.shaft_length = self.shaft_length
        types_tension_pile.shape = PileShape.RECTANGULAR_PILE_WITH_ENLARGED_BASE
        return types_tension_pile


class BearingRoundTaperedPile(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    diameter_at_pile_tip: confloat(ge=0, le=100)
    increase_in_diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.diameter = self.diameter_at_pile_tip
        types_bearing_pile.increase_in_diameter = self.increase_in_diameter
        types_bearing_pile.shape = PileShape.ROUND_TAPERED_PILE
        return types_bearing_pile


class TensionRoundTaperedPile(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    diameter_at_pile_tip: confloat(ge=0, le=100)
    increase_in_diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.diameter = self.diameter_at_pile_tip
        types_tension_pile.increase_in_diameter = self.increase_in_diameter
        types_tension_pile.shape = PileShape.ROUND_TAPERED_PILE
        return types_tension_pile


class BearingRoundHollowPileWithClosedBase(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    external_diameter: confloat(ge=0, le=100)
    wall_thickness: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.external_diameter = self.external_diameter
        types_bearing_pile.internal_diameter = (
            self.external_diameter - 2 * self.wall_thickness
        )
        types_bearing_pile.shape = PileShape.ROUND_HOLLOW_PILE_WITH_CLOSED_BASE
        return types_bearing_pile


class TensionRoundHollowPileWithClosedBase(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    external_diameter: confloat(ge=0, le=100)
    wall_thickness: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.external_diameter = self.external_diameter
        types_tension_pile.internal_diameter = (
            self.external_diameter - 2 * self.wall_thickness
        )
        types_tension_pile.shape = PileShape.ROUND_HOLLOW_PILE_WITH_CLOSED_BASE
        return types_tension_pile


class BearingRoundPileWithLostTip(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_diameter = self.base_diameter
        types_bearing_pile.pile_diameter = self.pile_diameter
        types_bearing_pile.shape = PileShape.ROUND_PILE_WITH_LOST_TIP
        return types_bearing_pile


class TensionRoundPileWithLostTip(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.base_diameter = self.base_diameter
        types_tension_pile.pile_diameter = self.pile_diameter
        types_tension_pile.shape = PileShape.ROUND_PILE_WITH_LOST_TIP
        return types_tension_pile


class BearingRoundPileWithInSituFormedBase(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_diameter = self.base_diameter
        types_bearing_pile.pile_diameter = self.pile_diameter
        types_bearing_pile.base_height = self.base_height
        types_bearing_pile.shape = PileShape.ROUND_PILE_WITH_IN_SITU_FORMED_BASE
        return types_bearing_pile


class TensionRoundPileWithInSituFormedBase(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    base_diameter: confloat(ge=0, le=100)
    pile_diameter: confloat(ge=0, le=100)
    base_height: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.base_diameter = self.base_diameter
        types_tension_pile.pile_diameter = self.pile_diameter
        types_tension_pile.base_height = self.base_height
        types_tension_pile.shape = PileShape.ROUND_PILE_WITH_IN_SITU_FORMED_BASE
        return types_tension_pile


class BearingSection(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    base_width: confloat(ge=0, le=100)
    base_length: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.base_width = self.base_width
        types_bearing_pile.base_length = self.base_length
        types_bearing_pile.shape = PileShape.SECTION
        return types_bearing_pile


class TensionSection(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    circumference: confloat(ge=0, le=100)
    cross_section: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.circumference = self.circumference
        types_tension_pile.cross_section = self.cross_section
        types_tension_pile.shape = PileShape.USER_DEFINED
        return types_tension_pile


class BearingRoundOpenEndedHollowPile(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    external_diameter: confloat(ge=0, le=100)
    wall_thickness: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.external_diameter = self.external_diameter
        types_bearing_pile.internal_diameter = (
            self.external_diameter - 2 * self.wall_thickness
        )
        types_bearing_pile.shape = PileShape.ROUND_OPEN_ENDED_HOLLOW_PILE
        return types_bearing_pile


class TensionRoundOpenEndedHollowPile(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    external_diameter: confloat(ge=0, le=100)
    wall_thickness: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.external_diameter = self.external_diameter
        types_tension_pile.internal_diameter = (
            self.external_diameter - 2 * self.wall_thickness
        )
        types_tension_pile.shape = PileShape.ROUND_OPEN_ENDED_HOLLOW_PILE
        return types_tension_pile


class BearingHShapedPile(BearingPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.BearingPile`."""

    height_h_shape: confloat(ge=0, le=100)
    width_h_shape: confloat(ge=0, le=100)
    thickness_web: confloat(ge=0, le=100)
    thickness_flange: confloat(ge=0, le=100)

    def _to_internal(self):
        types_bearing_pile = super()._to_internal()
        types_bearing_pile.height_h_shape = self.height_h_shape
        types_bearing_pile.width_h_shape = self.width_h_shape
        types_bearing_pile.thickness_web = self.thickness_web
        types_bearing_pile.thickness_flange = self.thickness_flange
        types_bearing_pile.shape = PileShape.H_SHAPED_PROFILE
        return types_bearing_pile


class TensionHShapedPile(TensionPile):
    """Inherits :class:`~geolib.models.dfoundations.piles.TensionPile`."""

    height_h_shape: confloat(ge=0, le=100)
    width_h_shape: confloat(ge=0, le=100)
    thickness_web: confloat(ge=0, le=100)
    thickness_flange: confloat(ge=0, le=100)

    def _to_internal(self):
        types_tension_pile = super()._to_internal()
        types_tension_pile.height_h_shape = self.height_h_shape
        types_tension_pile.width_h_shape = self.width_h_shape
        types_tension_pile.thickness_web = self.thickness_web
        types_tension_pile.thickness_flange = self.thickness_flange
        types_tension_pile.shape = PileShape.H_SHAPED_PROFILE
        return types_tension_pile
