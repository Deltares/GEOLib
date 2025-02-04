"""
Profile and Layer classes which are used by both D-Foundations and DSheetPiling.
D-Foundations often requires more parameters, which are unused for DSheetPiling.

"""

from pydantic import Field, field_validator
from typing_extensions import Annotated

from geolib.geometry.one import Point
from geolib.models import BaseDataClass

from .internal import SoilProfile as InternalSoilProfile


class CPT(BaseDataClass):
    """Internal Placeholder CPT measurements as used in D-Foundations/D-Sheetpiling.

    It is here because input files can contain CPTs coupled to a Profile.

    .. todo::
        * Add Friction and other parameters?
        * Unify with DFoundations
    """

    z: list[float]
    qc: list[float]


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
    layers: Annotated[list[SoilLayer], Field(min_length=1)]
    coordinate: Point = Point(x=0, y=0)

    @classmethod
    def top_of_layers_must_be_decreasing(cls, v):
        top_of_layers = [l.top_of_layer for l in v]
        if top_of_layers != sorted(top_of_layers, reverse=True):
            raise ValueError(
                f"Top of layer must decrease with each layer along depth. Top of layers: {top_of_layers}"
            )
        return v

    top_of_layer_validator = field_validator(
        "layers",
    )(top_of_layers_must_be_decreasing)

    def to_internal(self) -> InternalSoilProfile:
        return InternalSoilProfile(**self.model_dump(exclude_none=True))
