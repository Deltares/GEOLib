from enum import IntEnum
from typing import Optional

from geolib._compat import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    from pydantic import Field, PositiveFloat, StringConstraints
    from typing_extensions import Annotated
else:
    from pydantic import PositiveFloat, confloat, constr

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

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
    level: float
    e_modulus: Optional[PositiveFloat] = None
    cross_section: Optional[PositiveFloat] = None
    if IS_PYDANTIC_V2:
        wall_height_kranz: Optional[Annotated[float, Field(ge=0)]] = None
    else:
        wall_height_kranz: Optional[confloat(ge=0)] = None
    length: Optional[PositiveFloat] = None
    angle: Optional[float] = None
    side: Side = Side.RIGHT
    if IS_PYDANTIC_V2:
        yield_force: Optional[Annotated[float, Field(ge=0)]] = None
    else:
        yield_force: Optional[confloat(ge=0)] = None

    def to_internal(self) -> InternalAnchor:
        if IS_PYDANTIC_V2:
            return InternalAnchor(**self.model_dump(exclude_none=True))
        else:
            return InternalAnchor(**self.dict(exclude_none=True))


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

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
    level: float
    e_modulus: Optional[PositiveFloat] = None
    cross_section: Optional[PositiveFloat] = None
    length: Optional[PositiveFloat] = None
    angle: Optional[float] = None
    if IS_PYDANTIC_V2:
        buckling_force: Optional[Annotated[float, Field(ge=0)]] = None
    else:
        buckling_force: Optional[confloat(ge=0)] = None
    side: Side = Side.RIGHT
    pre_compression: Optional[PositiveFloat] = None

    def to_internal(self) -> InternalStrut:
        if IS_PYDANTIC_V2:
            return InternalStrut(
                **self.model_dump(exclude_none=True, exclude={"pre_compression"})
            )
        else:
            return InternalStrut(
                **self.dict(exclude_none=True, exclude={"pre_compression"})
            )


class SupportType(IntEnum):
    TRANSLATION = 1
    ROTATION = 2
    TRANSLATION_AND_ROTATION = 3


class SpringSupport(BaseDataClass):
    """Spring support."""

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: float
        rotational_stiffness: Annotated[float, Field(ge=0)]
        translational_stiffness: Annotated[float, Field(ge=0)]
    else:
        name: constr(min_length=1, max_length=50)
        level: float
        rotational_stiffness: confloat(ge=0)
        translational_stiffness: confloat(ge=0)

    def to_internal(self) -> InternalSupport:
        if IS_PYDANTIC_V2:
            return InternalSupport(**self.model_dump())
        else:
            return InternalSupport(**self.dict())


class RigidSupport(BaseDataClass):
    """Rigid support."""

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
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
