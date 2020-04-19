from datetime import timedelta
from enum import Enum

from pydantic import BaseModel


class DrainType(Enum):
    pass


class DrainGridType(Enum):
    pass


class DrainSchedule(BaseModel):
    pass


class VerticalDrain(BaseModel):
    """Vertical Drain Class to inherit from."""

    drain_type: DrainType
    range_from: float
    range_to: float
    bottom_position: float
    center_to_center: float
    width_diameter: float
    thickness: float
    grid: DrainGridType
    start_of_drainage: timedelta
    phreatic_level_in_drain: float
    schedule: DrainSchedule
