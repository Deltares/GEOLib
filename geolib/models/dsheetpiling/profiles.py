"""
Profile and Layer classes which are used by both D-Foundations and DSheetPiling.
D-Foundations often requires more parameters, which are unused for DSheetPiling.

"""

from typing import List

from geolib._compat import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    from pydantic import Field, field_validator
    from typing_extensions import Annotated
else:
    from pydantic import conlist, validator

from geolib.geometry.one import Point
from geolib.models import BaseDataClass
from geolib.soils import Soil

from .internal import SoilProfile as InternalSoilProfile


class CPT(BaseDataClass):
    """Internal Placeholder CPT measurements as used in D-Foundations/D-Sheetpiling.

    It is here because input files can contain CPTs coupled to a Profile.

    .. todo::
        * Add Friction and other parameters?
        * Unify with DFoundations
    """

    z: List[float]
    qc: List[float]


class CPTRule(BaseDataClass):
    """Placeholder class for CPT interpretation options."""


class SoilLayer(BaseDataClass):
    """Layer in a D-Sheetpiling Profile."""

    top_of_layer: float
    soil: str
    water_pressure_top: float = 0.0
    water_pressure_bottom: float = 0.0


class SoilProfile(BaseDataClass):
    """D-Sheetpiling Profile."""

    name: str
    if IS_PYDANTIC_V2:
        layers: Annotated[List[SoilLayer], Field(min_length=1)]
    else:
        layers: conlist(SoilLayer, min_items=1)
    coordinate: Point = Point(x=0, y=0)

    @classmethod
    def top_of_layers_must_be_decreasing(cls, v):
        top_of_layers = [l.top_of_layer for l in v]
        if top_of_layers != sorted(top_of_layers, reverse=True):
            raise ValueError(
                f"Top of layer must decrease with each layer along depth. Top of layers: {top_of_layers}"
            )
        return v

    if IS_PYDANTIC_V2:
        top_of_layer_validator = field_validator(
            "layers",
        )(top_of_layers_must_be_decreasing)
    else:
        top_of_layer_validator = validator("layers")(top_of_layers_must_be_decreasing)

    def to_internal(self) -> InternalSoilProfile:
        if IS_PYDANTIC_V2:
            return InternalSoilProfile(**self.model_dump(exclude_none=True))
        else:
            return InternalSoilProfile(**self.dict(exclude_none=True))
