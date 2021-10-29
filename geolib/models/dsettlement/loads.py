from abc import ABCMeta, abstractmethod
from datetime import timedelta
from typing import Optional

from pydantic import constr

from geolib.geometry import Point
from geolib.models import BaseDataClass

from .internal import (
    LoadValuesCircular,
    LoadValuesRectangular,
    LoadValuesTank,
    LoadValuesTrapeziform,
    LoadValuesUniform,
)
from .internal import OtherLoad as _OtherLoad
from .internal import TypeOtherLoads


class OtherLoad(BaseDataClass, metaclass=ABCMeta):
    """Other Load Class to inherit from."""

    load_type: Optional[TypeOtherLoads]

    @abstractmethod
    def _to_internal(self, time: timedelta, p: Point):
        """Creates internal datastructure from generic load"""


class TrapeziformLoad(OtherLoad):
    """
    Create a trapeziform load with the given name and properties.

    Arguments:
        gamma -- The weight of the load per m\ :sup:`3`

    .. image:: /figures/dsettlement/trapeziform.png
        :height: 200px
        :width: 400 px
        :scale: 50 %
        :align: center

    """

    gamma: float = 0
    height: float = 0
    xl: float = 0
    xm: float = 0
    xr: float = 0

    def _to_internal(self, time: timedelta, p: Point) -> _OtherLoad:

        load_values = LoadValuesTrapeziform(
            gamma=self.gamma,
            height=self.height,
            xl=self.xl,
            xm=self.xm,
            xr=self.xr,
            Xp=p.x,
            Yp=p.z,
        )
        other_load = _OtherLoad(
            time=time.days,
            load_type=TypeOtherLoads.Trapeziform,
            load_values_trapeziform=load_values,
        )
        return other_load


class CircularLoad(OtherLoad):
    """Create a circular load with the given name and properties.

    Arguments:
        weight: The mangitude of the load.
        alpha: The shape factor alpha is used to specify the shape of the contact pressure.

    .. image:: /figures/dsettlement/circular.png
        :height: 200px
        :width: 400 px
        :scale: 50 %
        :align: center

    """

    weight: float = 0
    alpha: float = 0
    R: float = 0.01

    def _to_internal(self, time: timedelta, p: Point) -> _OtherLoad:
        load_values = LoadValuesCircular(
            weight=self.weight, alpha=self.alpha, Xcp=p.x, Ycp=p.z, Zcp=p.y, R=self.R,
        )
        other_load = _OtherLoad(
            time=time.days,
            load_type=TypeOtherLoads.Circular,
            load_values_circular=load_values,
        )
        return other_load


class RectangularLoad(OtherLoad):
    """Create a rectangular load with the given name and properties

    Arguments:
        weight: The mangitude of the load.
        alpha: The shape factor alpha is used to specify the shape of the contact pressure

    .. image:: /figures/dsettlement/rectangural.png
        :height: 200px
        :width: 400 px
        :scale: 50 %
        :align: center

    """

    weight: float = 0  # kN/m2
    alpha: float = 0
    xwidth: float = 0.01
    zwidth: float = 0.01

    def _to_internal(self, time: timedelta, p: Point) -> _OtherLoad:
        load_values = LoadValuesRectangular(
            weight=self.weight,
            alpha=self.alpha,
            Xcp=p.x,
            Ycp=p.z,
            Zcp=p.y,
            xwidth=self.xwidth,
            zwidth=self.zwidth,
        )
        other_load = _OtherLoad(
            time=time.days,
            load_type=TypeOtherLoads.Rectangular,
            load_values_rectangular=load_values,
        )
        return other_load


# TODO This is a 1D Load and should not be other load?
class UniformLoad(OtherLoad):
    """Create a uniform load with the given name and properties.

    Arguments:
        unit_weight: The weight of the load per m\ :sup:`3`

    .. image:: /figures/dsettlement/uniform.png
        :height: 200px
        :width: 400 px
        :scale: 50 %
        :align: center

    """

    unit_weight: float = 0
    gamma: float = 0
    height: float = 0
    y_application: float = 0

    def _to_internal(self, time: timedelta, point: Point) -> _OtherLoad:
        load_values = LoadValuesUniform(
            unit_weight=self.unit_weight,
            height=self.height,
            y_application=point.z,
            gamma=self.gamma,
        )
        other_load = _OtherLoad(
            time=time.days,
            load_type=TypeOtherLoads.Uniform,
            load_values_uniform=load_values,
        )
        return other_load


class TankLoad(OtherLoad):
    """Create a tank load with the given name and properties.

    Arguments:
        wallweight: The magnitude of the load induced by the weight of the material in which the tank is made.
        alpha: The shape factor alpha is used to specify the shape of the contact pressure.
        internalweight: The magnitude of the load induced by the weight of the material stored in the tank.

    .. image:: /figures/dsettlement/tank.png
        :height: 200px
        :width: 400 px
        :scale: 50 %
        :align: center

    """

    wallweight: float = 0
    internalweight: float = 0
    alpha: float = 0
    Rintern: float = 0.01
    dWall: float = 0.01

    def _to_internal(self, time: timedelta, p: Point) -> _OtherLoad:
        load_values = LoadValuesTank(
            wallweight=self.wallweight,
            alpha=self.alpha,
            internalweight=self.internalweight,
            Xcp=p.x,
            Ycp=p.z,
            Zcp=p.y,
            Rintern=self.Rintern,
            dWall=self.dWall,
        )
        other_load = _OtherLoad(
            time=time.days, load_type=TypeOtherLoads.Tank, load_values_tank=load_values,
        )
        return other_load
