from typing import Optional

from pydantic import BaseModel as DataModel

from .one import Point


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
