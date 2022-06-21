from abc import ABCMeta, abstractmethod
from datetime import timedelta
from typing import List, Optional, Union

from geolib.models import BaseDataClass

from .drain_types import DrainGridType, DrainSchedule, DrainType
from .internal import VerticalDrain as vd


class ScheduleValues(BaseDataClass, metaclass=ABCMeta):
    """ScheduleValues to inherit from"""

    schedule: Optional[DrainSchedule]

    @abstractmethod
    def _to_internal(self):
        """Creates internal datastructure from generic schedule values"""
        return


class ScheduleValuesOff(ScheduleValues):
    """Drainage Schedule with strips or columns is Off

    Arguments:
        Start of drainage -- The time t at which the drain becomes active. D-SETTLEMENT assumes
            that the water head in the drain equals the phreatic level.
        Phreatic level in drain -- The water head in the drain during drainage.
    """

    start_of_drainage: timedelta
    phreatic_level_in_drain: float

    def _to_internal(self, verticaldrains: vd) -> vd:
        verticaldrains.schedule_type = DrainSchedule.OFF
        verticaldrains.start_of_drainage = self.start_of_drainage.days
        verticaldrains.phreatic_level_in_drain = self.phreatic_level_in_drain
        return verticaldrains


class ScheduleValuesSimpleInput(ScheduleValues):
    """Drainage Schedule with strips or columns: Simple Input

    Arguments:
        Start of drainage -- The time t at which the drain becomes active. D-SETTLEMENT assumes
            that the water head in the drain equals the phreatic level.
        Begin time -- The time at which dewatering (i.e. a certain water level and air pressure) starts.
        End time -- The time at which dewatering stops.
        Underpressure -- The enforced underpressure during dewatering.
        Water head during dewatering -- The vertical level where the negative pore pressure equals the enforced underpressure during dewatering.
        Phreatic level in drain -- The water head in the drain during drainage.
    """

    start_of_drainage: timedelta
    phreatic_level_in_drain: float
    begin_time: float
    end_time: float
    underpressure: float
    water_head_during_dewatering: Optional[float]
    tube_pressure_during_dewatering: Optional[float]

    def _to_internal(self, verticaldrains: vd) -> vd:
        verticaldrains.schedule_type = DrainSchedule.SIMPLE_INPUT
        verticaldrains.start_of_drainage = self.start_of_drainage.days
        verticaldrains.phreatic_level_in_drain = self.phreatic_level_in_drain
        verticaldrains.begin_time = self.begin_time
        verticaldrains.end_time = self.end_time
        verticaldrains.water_head_during_dewatering = self.water_head_during_dewatering
        verticaldrains.tube_pressure_during_dewatering = (
            self.tube_pressure_during_dewatering
        )
        verticaldrains.under_pressure_for_strips_and_columns = self.underpressure
        verticaldrains.under_pressure_for_sand_wall = self.underpressure
        return verticaldrains


class ScheduleValuesDetailedInput(ScheduleValues):
    """Drainage Schedule with strips or columns: Detailed Input

    Arguments:
        Time -- The time at which dewatering is active.
        Underpressure -- This value is zero for vertical drains without enforced underpressure.
        Water head -- The vertical level where the negative pore pressure equals the enforced underpressure during dewatering.
    """

    time: List[timedelta] = []
    underpressure: List[float] = []
    water_level: List[float] = []

    def _to_internal(self, verticaldrains: vd) -> vd:
        verticaldrains.schedule_type = DrainSchedule.DETAILED_INPUT
        verticaldrains.time = [onetime.days for onetime in self.time]
        verticaldrains.underpressure = self.underpressure
        verticaldrains.water_level = self.water_level
        return verticaldrains


class VerticalDrain(BaseDataClass):
    """Vertical Drain Class to inherit from.
    This class refers to the input window "Vertical Drains" of the D-Settlement program.

    Arguments:
        range_from -- left limit to the drained area
        range_to -- right limit to the drained area
        bottom_position -- The (vertical) Y co-ordinate of the bottom end of the vertical drain.
        center_to_center -- The actual spacing between the drains.
        diameter -- The diameter of the Column drain.
        thickness -- The actual thickness of the Strip drain.
        grid -- The geometry of the grid.
    """

    drain_type: DrainType = DrainType.STRIP
    range_from: float
    range_to: float
    bottom_position: float
    center_to_center: float
    width: Optional[float]
    diameter: Optional[float]
    thickness: Optional[float]
    grid: DrainGridType = DrainGridType.UNDERDETERMINED
    schedule: ScheduleValues = None

    def _to_internal(self) -> vd:
        internal_vertical_drains = vd(
            drain_type=self.drain_type,
            range_from=self.range_from,
            range_to=self.range_to,
            bottom_position=self.bottom_position,
            center_to_center=self.center_to_center,
            width=self.width,
            diameter=self.diameter,
            thickness=self.thickness,
            grid=self.grid,
        )
        internal_vertical_drains = self.schedule._to_internal(internal_vertical_drains)
        return internal_vertical_drains
