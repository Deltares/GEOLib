from typing import Optional

from pydantic import BaseModel as DataModel
from operator import attrgetter

from .one import Point
from typing import List


class Circle(DataModel):
    """A Circle.

    Used for DStability Calculation Options
    """

    center: Point
    radius: float


class Rectangle(DataModel):
    """A Rectangle.

    Used for DStability Calculation Options
    """

    bl_corner: Point  # bottom left
    width: float
    height: float
