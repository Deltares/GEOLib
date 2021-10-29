"""
This module handles the four types of loads in DStability.
"""
import abc
from typing import List, Optional

from pydantic import NoneStr, confloat, validator

from geolib.models import BaseDataClass

from ...geometry.one import Point
from .internal import (
    PersistableConsolidation,
    PersistableLineLoad,
    PersistablePoint,
    PersistableUniformLoad,
)


class DStabilityLoad(BaseDataClass):
    """Base Class for Loads."""

    label: NoneStr

    @abc.abstractmethod
    def to_internal_datastructure(self):
        raise NotImplementedError


class Consolidation(BaseDataClass):
    degree: confloat(ge=0, le=100) = 100
    layer_id: int

    def to_internal_datastructure(self) -> PersistableConsolidation:
        return PersistableConsolidation(Degree=self.degree, LayerId=str(self.layer_id))


class UniformLoad(DStabilityLoad):
    """UniformLoad."""

    start: float
    end: float
    magnitude: confloat(ge=0)
    angle_of_distribution: confloat(ge=0, le=90)

    @validator("end")
    def end_greater_than_start(cls, v, values):
        if v <= values["start"]:
            raise ValueError(f"End {v} should be greater than start ({values['start']})")
        return v

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
    angle: confloat(ge=-360, le=360)
    magnitude: confloat(ge=0)
    angle_of_distribution: confloat(ge=0, le=90)

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

    height: float
    wind_force: float
    width_of_root_zone: float
    angle_of_distribution: float


class Earthquake(DStabilityLoad):
    """Inherits :class:`~geolib.models.dstability.loads.DStabilityLoad`."""

    horizontal_factor: float
    vertical_factor: float
    free_water_factor: float
