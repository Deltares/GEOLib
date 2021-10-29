"""
This module handles the three types of reinforcements in DStability.
"""

import abc
from typing import List, Tuple

from pydantic import NoneStr, confloat

from geolib.models import BaseDataClass

from ...geometry.one import Point
from ...utils import snake_to_camel
from .internal import (
    PersistableForbiddenLine,
    PersistableGeotextile,
    PersistableNail,
    PersistablePoint,
    PersistableStressAtDistance,
)


class DStabilityReinforcement(BaseDataClass, metaclass=abc.ABCMeta):
    """Base Class for Reinforcements."""

    label: NoneStr = None

    @abc.abstractmethod
    def _to_internal_datastructure(self):
        raise NotImplementedError


class Nail(DStabilityReinforcement):
    """DStability Nail, used for soil nailing."""

    location: Point  # TODO x, z must be below ground level
    direction: float = 0.0
    horizontal_spacing: float = 0.0
    length: confloat(gt=0) = 3.0
    diameter: confloat(gt=0) = 0.1
    grout_diameter: confloat(gt=0) = 0.1
    critical_angle: float = 0.0
    max_pull_force: float = 0.0
    plastic_moment: float = 0.0
    bending_stiffness: confloat(gt=0) = 0.1
    use_facing: bool = False
    use_lateral_stress: bool = (
        False  # TODO set on wether or not lateralstresses are provided?
    )
    use_shear_stress: bool = (
        False  # TODO set on wether or not shearstresses are provided?
    )
    lateral_stresses: List[Tuple[float, float]] = []
    shear_stresses: List[Tuple[float, float]] = []

    def _to_internal_datastructure(self) -> PersistableNail:
        data = {
            **{
                snake_to_camel(name): value
                for name, value in self.dict().items()
                if name not in {"x", "z", "lateral_stresses", "shear_stresses"}
            },
            "Location": PersistablePoint(X=self.location.x, Z=self.location.z),
            "LateralStresses": [
                PersistableStressAtDistance(Distance=distance, Stress=stress)
                for distance, stress in self.lateral_stresses
            ],
            "ShearStresses": [
                PersistableStressAtDistance(Distance=distance, Stress=stress)
                for distance, stress in self.shear_stresses
            ],
        }
        return PersistableNail(**data)


class ForbiddenLine(DStabilityReinforcement):
    """Inherits :class:`~geolib.models.dstability.reinforcements.DStabilityReinforcement`. Needs to be further defined."""

    start: Point
    end: Point

    def _to_internal_datastructure(self) -> PersistableForbiddenLine:
        return PersistableForbiddenLine(
            Label=self.label,
            Start=PersistablePoint(X=self.start.x, Z=self.start.z),
            End=PersistablePoint(X=self.end.x, Z=self.end.z),
        )


class Geotextile(DStabilityReinforcement):
    """Geotextile"""

    start: Point
    end: Point
    effective_tensile_strength: confloat(gt=0)
    reduction_area: confloat(gt=0)

    def _to_internal_datastructure(self) -> PersistableForbiddenLine:
        return PersistableGeotextile(
            Label=self.label,
            Start=PersistablePoint(X=self.start.x, Z=self.start.z),
            End=PersistablePoint(X=self.end.x, Z=self.end.z),
            TensileStrength=self.effective_tensile_strength,
            ReductionArea=self.reduction_area,
        )
