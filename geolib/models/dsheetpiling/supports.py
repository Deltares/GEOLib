from enum import IntEnum

from pydantic import Field, PositiveFloat, StringConstraints
from typing_extensions import Annotated

from geolib.models import BaseDataClass

from .internal import Anchor as InternalAnchor
from .internal import Strut as InternalStrut
from .internal import Support as InternalSupport
from .settings import Side


class Anchor(BaseDataClass):
    """Anchor. This option is not available for SinglePileModelType.

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
    """

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    level: float
    e_modulus: PositiveFloat | None = None
    cross_section: PositiveFloat | None = None
    wall_height_kranz: Annotated[float, Field(ge=0)] | None = None
    length: PositiveFloat | None = None
    angle: float | None = None
    side: Side = Side.RIGHT
    yield_force: Annotated[float, Field(ge=0)] | None = None

    def to_internal(self) -> InternalAnchor:
        return InternalAnchor(**self.model_dump(exclude_none=True))


class Strut(BaseDataClass):
    """Strut. This option is not available for SinglePileModelType.

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

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    level: float
    e_modulus: PositiveFloat | None = None
    cross_section: PositiveFloat | None = None
    length: PositiveFloat | None = None
    angle: float | None = None
    buckling_force: Annotated[float, Field(ge=0)] | None = None
    side: Side = Side.RIGHT
    pre_compression: PositiveFloat | None = None

    def to_internal(self) -> InternalStrut:
        return InternalStrut(
            **self.model_dump(exclude_none=True, exclude={"pre_compression"})
        )


class SupportType(IntEnum):
    TRANSLATION = 1
    ROTATION = 2
    TRANSLATION_AND_ROTATION = 3


class SpringSupport(BaseDataClass):
    """Spring support."""

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    level: float
    rotational_stiffness: Annotated[float, Field(ge=0)]
    translational_stiffness: Annotated[float, Field(ge=0)]

    def to_internal(self) -> InternalSupport:
        return InternalSupport(**self.model_dump())


class RigidSupport(BaseDataClass):
    """Rigid support."""

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    level: float
    support_type: SupportType

    def to_internal(self) -> InternalSupport:
        rotational_stiffness, translational_stiffness = {
            SupportType.TRANSLATION.value: (0, 1),
            SupportType.ROTATION.value: (1, 0),
            SupportType.TRANSLATION_AND_ROTATION.value: (1, 1),
        }[self.support_type.value]

        return InternalSupport(
            name=self.name,
            level=self.level,
            rotational_stiffness=rotational_stiffness,
            translational_stiffness=translational_stiffness,
        )
