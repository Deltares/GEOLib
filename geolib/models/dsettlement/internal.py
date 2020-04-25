from enum import IntEnum
from typing import List, Optional, Union, Dict

from pydantic import BaseModel as DataClass
from pydantic.types import conint, constr

from geolib.geometry.one import Point
from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.dseries_parser import (
    DSeriesStructure,
    DSeriesKeyValueSubStructure,
    DSeriesNameKeyValueSubStructure,
    DSeriesListSubStructure,
    DSeriesNoParseSubStructure,
)

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


class PointForLoad(DataClass):
    X: float
    Z: float

    @classmethod
    def from_point(cls, p: Point):
        return cls(X=p.x, Z=p.y)


class NonUniformLoad(DataClass):
    time: int = 0
    gammadry: float = 10
    gammawet: float = 10
    temporary: bool
    endtime: int = 0
    points: List[PointForLoad]


class NonUniformLoads(DSeriesNoParseSubStructure):
    """Representation of [NON-UNIFORM LOADS] group."""

    loads: Dict[constr(min_length=1, max_length=25), NonUniformLoad] = {}

    def add_load(
        self, name: constr(min_length=1, max_length=25), load: NonUniformLoad
    ) -> Optional[ValueError]:
        if name in self.loads:
            raise ValueError(f"Load with name '{name}' already exists.")
        else:
            self.loads[name] = load
            self.loads = self.loads  # trigger validation


class ResidualTimes(DSeriesNoParseSubStructure):
    time_steps: List[conint(ge=0)]


class Verticals(DSeriesNoParseSubStructure):
    # total mesh is default value that is written in sli file but not read
    total_mesh: int = 100
    locations: List[DSeriePoint]


class TypeOtherLoads(IntEnum):
    Trapeziform = 0
    Circular = 1
    Rectangular = 2
    Uniform = 3
    Tank = 4


class LoadValuesTrapeziform(DataClass):
    gamma: float = 0
    height: float = 0
    xl: float = 0
    xm: float = 0
    xr: float = 0
    Xp: float = 0
    Yp: float = 0


class LoadValuesCircular(DataClass):
    weight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    R: float = 0.01


class LoadValuesRectangular(DataClass):
    weight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    xwidth: float = 0.01
    zwidth: float = 0.01


class LoadValuesUniform(DataClass):
    unit_weight: float = 0
    gamma: float = 0
    height: float = 0
    y_application: float = 0


class LoadValuesTank(DataClass):
    wallweight: float = 0
    internalweight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    Rintern: float = 0.01
    dWall: float = 0.01


class OtherLoad(DataClass):
    load_type: TypeOtherLoads
    time: int = 0
    load_values_trapeziform: Optional[LoadValuesTrapeziform]
    load_values_circular: Optional[LoadValuesCircular]
    load_values_rectangular: Optional[LoadValuesRectangular]
    load_values_uniform: Optional[LoadValuesUniform]
    load_values_tank: Optional[LoadValuesTank]


class OtherLoads(DSeriesNoParseSubStructure):
    """Representation of [OTHER LOADS] group."""

    loads: Dict[constr(min_length=1, max_length=25), OtherLoad] = {}

    def add_load(
        self, name: constr(min_length=1, max_length=25), load: OtherLoad
    ) -> Optional[ValueError]:
        if name in self.loads:
            raise ValueError(f"Load with name '{name}' already exists.")
        else:
            self.loads[name] = load


class DSettlementStructure(DSeriesStructure):
    version: Version
    soil_collection: Union[SoilCollection, str]
    geometry_data: str
    run_identification: str
    model: str
    verticals: Union[Verticals, str]
    water: str
    non__uniform_loads: Union[NonUniformLoads, str]
    water_loads: str
    other_loads: Union[OtherLoads, str]
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
