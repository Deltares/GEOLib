"""
This module handles the four types of loads in DStability.

.. todo::
    Unify these loads with the older models
"""

from pydantic import BaseModel


class DStabilityLoad(BaseModel):
    """Base Class for Loads."""

    label: str


class UniformLoad(DStabilityLoad):
    """Inherits :class:`~geolib.models.dstability.loads.DStabilityLoad`."""

    width: float
    magnitude: float
    angle_of_distribution: float


class LineLoad(DStabilityLoad):
    """Inherits :class:`~geolib.models.dstability.loads.DStabilityLoad`."""

    angle: float
    magnitude: float
    angle_of_distribution: float


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
