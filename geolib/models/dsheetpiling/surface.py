from typing import List, Optional

from geolib._compat import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    from pydantic import Field, StringConstraints, field_validator
    from typing_extensions import Annotated
else:
    from pydantic import confloat, conlist, constr, validator

from geolib.geometry import Point
from geolib.models import BaseDataClass

from .internal import Surface as InternalSurface
from .settings import DistributionType


class Surface(BaseDataClass):
    """Surface.

    Args:
        name: Name of the surface.
        points: Surface points. Points (X, Z) must be defined from the sheet outwards regarding x-coordinate.
        distribution_type: Distribution type.
        std: Standard deviation of the distribution type.
    """

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        points: Annotated[List[Point], Field(min_length=1)]
        distribution_type: Optional[DistributionType] = None
        std: Optional[Annotated[float, Field(ge=0.0)]] = None
    else:
        name: constr(min_length=1, max_length=50)
        points: conlist(Point, min_items=1)
        distribution_type: Optional[DistributionType] = None
        std: Optional[confloat(ge=0.0)] = None

    @classmethod
    def points_must_be_increasing_and_greater_or_equal_to_zero(cls, v):
        x_coords = [p.x for p in v]
        if min(x_coords) < 0:
            raise ValueError(
                f"All x-coordinates must be greater than or equal to 0, found {min(x_coords)}"
            )
        if x_coords[0] != 0:
            raise ValueError(
                f"X-coordinate first point should be zero, received {x_coords[0]}"
            )
        if x_coords != sorted(x_coords):
            raise ValueError("x-coordinates must be strictly increasing")
        return v

    if IS_PYDANTIC_V2:
        points_validator = field_validator("points")(
            points_must_be_increasing_and_greater_or_equal_to_zero
        )
    else:
        points_validator = validator("points")(
            points_must_be_increasing_and_greater_or_equal_to_zero
        )

    def to_internal(self) -> InternalSurface:
        if IS_PYDANTIC_V2:
            kwargs = self.model_dump(exclude_none=True, exclude=["points"])
        else:
            kwargs = self.dict(exclude_none=True, exclude={"points"})
        kwargs["points"] = [
            {"Nr": i, "X-coord": p.x, "Value": p.z}
            for i, p in enumerate(self.points, start=1)
        ]
        return InternalSurface(**kwargs)
