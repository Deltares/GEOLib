"""
This module handles the four types of loads in DStability.
"""

import abc

from pydantic import Field, model_validator
from typing_extensions import Annotated

from geolib.models import BaseDataClass

from ...geometry.one import Point
from .internal import (
    PersistableConsolidation,
    PersistableLineLoad,
    PersistablePoint,
    PersistableTree,
    PersistableUniformLoad,
)


class DStabilityLoad(BaseDataClass):
    """Base Class for Loads."""

    label: str | None = None

    @abc.abstractmethod
    def to_internal_datastructure(self):
        raise NotImplementedError


class Consolidation(BaseDataClass):
    degree: Annotated[float, Field(ge=0, le=100)] = 100
    layer_id: int

    def to_internal_datastructure(self) -> PersistableConsolidation:
        return PersistableConsolidation(Degree=self.degree, LayerId=str(self.layer_id))


class UniformLoad(DStabilityLoad):
    """UniformLoad."""

    start: float
    end: float
    magnitude: Annotated[float, Field(ge=0)]
    angle_of_distribution: Annotated[float, Field(ge=0, le=90)]

    @model_validator(mode="after")
    def end_greater_than_start(self):
        if self.end <= self.start:
            raise ValueError(
                f"End {self.end} should be greater than start ({self.start})"
            )
        return self

    def to_internal_datastructure(self) -> PersistableUniformLoad:
        return PersistableUniformLoad(
            Label=self.label,
            Start=self.start,
            End=self.end,
            Magnitude=self.magnitude,
            Spread=self.angle_of_distribution,
        )


class LineLoad(DStabilityLoad):
    """DStability Lineload."""

    location: Point
    angle: Annotated[float, Field(ge=-360, le=360)]
    magnitude: Annotated[float, Field(ge=0)]
    angle_of_distribution: Annotated[float, Field(ge=0, le=90)]

    def to_internal_datastructure(self) -> PersistableLineLoad:
        return PersistableLineLoad(
            Label=self.label,
            Location=PersistablePoint(X=self.location.x, Z=self.location.z),
            Angle=self.angle,
            Magnitude=self.magnitude,
            Spread=self.angle_of_distribution,
        )


class TreeLoad(DStabilityLoad):
    """Inherits :class:`~geolib.models.dstability.loads.DStabilityLoad`."""

    tree_top_location: Point
    wind_force: float
    width_of_root_zone: float
    angle_of_distribution: float

    def to_internal_datastructure(self) -> PersistableTree:
        return PersistableTree(
            Label=self.label,
            Location=PersistablePoint(
                X=self.tree_top_location.x, Z=self.tree_top_location.z
            ),
            Force=self.wind_force,
            RootZoneWidth=self.width_of_root_zone,
            Spread=self.angle_of_distribution,
        )


class Earthquake(DStabilityLoad):
    """Inherits :class:`~geolib.models.dstability.loads.DStabilityLoad`."""

    horizontal_factor: float
    vertical_factor: float
    free_water_factor: float
