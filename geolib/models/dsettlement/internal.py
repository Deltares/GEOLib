from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel as DataClass
from pydantic.types import conint

from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.dseries_parser import (
    DSeriesStructure,
    DSeriesKeyValueSubStructure,
    DSeriesNameKeyValueSubStructure,
    DSeriesListSubStructure,
    DSeriesNoParseSubStructure,
)
from geolib.geometry.one import Point

DataClass.Config.arbitrary_types_allowed = True


class DSeriePoint(DataClass):
    """
        Converting points from geolib co-ordinate system to the d-settlement UI
        Internal setting of the geometry differs from API.
        Here co-ordinate system is the same as in the the d-settlement UI.
        So axis z of the geolib needs to be modified to y axis, which represents the depth.
    """

    X: float
    Y: float
    Z: float

    @classmethod
    def from_point(cls, p: Point):
        return cls(X=p.x, Y=p.z, Z=p.y)


class Soil(DSeriesNoParseSubStructure):
    name: str


class SoilCollection(DSeriesListSubStructure):
    soil: Union[List[Soil], List[str]]


class Version(DSeriesKeyValueSubStructure):
    soil: int = 1005
    geometry: int = 1000
    d__settlement: int = 1007


class ResidualTimes(DSeriesNoParseSubStructure):
    time_steps: List[conint(ge=0)]


class Verticals(DSeriesNoParseSubStructure):
    # total mesh is default value that is written in sli file but not read
    total_mesh: int = 100
    locations: List[DSeriePoint]


class DSettlementStructure(DSeriesStructure):
    version: Version
    soil_collection: Union[SoilCollection, str]
    geometry_data: str
    run_identification: str
    model: str
    verticals: Union[Verticals, str]
    water: str
    non__uniform_loads: str
    water_loads: str
    other_loads: str
    calculation_options: str
    residual_times: Union[ResidualTimes, str]
    filter_band_width: str
    pore_pressure_meters: str
    non__uniform_loads_pore_pressures: str
    other_loads_pore_pressures: str
    calculation_options_pore_pressures: str
    vertical_drain: str
    probabilistic_data: str
    probabilistic_defaults: str
    fit_options: str
    fit_calculation: str
    eps: str
    fit: str
