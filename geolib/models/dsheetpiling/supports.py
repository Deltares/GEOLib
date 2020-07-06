from pydantic import BaseModel as DataModel
from pydantic import PositiveFloat, constr
from typing import Optional
from .settings import Side
from .internal import (
    Anchor as InternalAnchor,
    Strut as InternalStrut
)


class Anchor(DataModel):
    """Anchor.

    Args:
        name: Name of the anchor
        level: Level of the anchor, or z-coordinate [m]
        e_modulus: E-modulus [kN/m^2]
        cross_section: Cross section [m^2/m']
        wall_height_kranz: Height of the wall [Kranz] [m]
        length: Length [m]
        angle: Angle [deg]
        yield_force: Yield force [kN/m']
        side: Side of the anchor [Side]
        pre_tension: Pre-tensioning forces [kN/m']
    """
    name: constr(min_length=1, max_length=50)
    level: float
    e_modulus: Optional[PositiveFloat] = None
    cross_section: Optional[PositiveFloat] = None
    wall_height_kranz: Optional[PositiveFloat] = None
    length: Optional[PositiveFloat] = None
    angle: Optional[PositiveFloat] = None
    side: Side = Side.RIGHT
    yield_force: Optional[PositiveFloat] = None

    def to_internal(self) -> InternalAnchor:
        return InternalAnchor(**self.dict(exclude_none=True))


class Strut(DataModel):
    """Strut.

    Args:
        name: Name of the strut
        level: Level of the strut, or z-coordinate [m]
        e_modulus: E-modulus [kN/m^2]
        cross_section: Cross section [m^2/m']
        length: Length [m]
        angle: Angle [deg]
        buckling_force: Buckling force of the strut [kN/m']
        side: Side of the strut [Side]
        pre_compression: Pre-compressions [kN/m']
    """
    name: constr(min_length=1, max_length=50)
    level: float
    e_modulus: Optional[PositiveFloat] = None
    cross_section: Optional[PositiveFloat] = None
    length: Optional[PositiveFloat] = None
    angle: Optional[PositiveFloat] = None
    buckling_force: Optional[PositiveFloat] = None
    side: Side = Side.RIGHT
    pre_compression: Optional[PositiveFloat] = None

    def to_internal(self) -> InternalStrut:
        return InternalStrut(**self.dict(exclude_none=True))


class SpringSupport(DataModel):
    """Spring support."""


class RigidSupport(DataModel):
    """Rigid support."""
