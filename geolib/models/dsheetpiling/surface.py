from pydantic import Field, StringConstraints, field_validator
from typing_extensions import Annotated

from geolib.models import BaseDataClass

from .internal import Surface as InternalSurface, SurfacePoint
from .settings import DistributionType

class Surface(BaseDataClass):
    """Surface.

    Args:
        name: Name of the surface.
        points: Surface points. Points (X, Z) must be defined from the sheet outwards regarding x-coordinate.
        distribution_type: Distribution type.
        std: Standard deviation of the distribution type.
        construction_level_tolerance: (Only relevant for CROW calculation) Construction level tolerance.
        survey_uncertainty: (Only relevant for CROW calculation) Survey uncertainty.
    """

    name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    points: Annotated[list[SurfacePoint], Field(min_length=1)]
    distribution_type: DistributionType | None = None
    std: Annotated[float, Field(ge=0.0)] | None = None
    construction_level_tolerance: Annotated[float, Field(ge=0.0)] | None = None
    survey_uncertainty: Annotated[float, Field(ge=0.0)] | None = None

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

    points_validator = field_validator("points")(
        points_must_be_increasing_and_greater_or_equal_to_zero
    )

    def to_internal(self) -> InternalSurface:
        kwargs = self.model_dump(exclude_none=True, exclude=["points"])
        kwargs["points"] = [
            {"Nr": i, "X-coord": p.x, "Value": p.z,  "Rep. erosion height": p.rep_erosion_height}
            for i, p in enumerate(self.points, start=1)
        ]
        return InternalSurface(**kwargs)
