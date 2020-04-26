import logging
from enum import Enum, IntEnum
from math import isclose
from operator import attrgetter
from typing import Dict, List, Optional, Union

from pydantic import BaseModel as DataClass
from pydantic.types import PositiveInt, confloat, conint, conlist, constr

from geolib.geometry.one import Point
from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.dseries_parser import (
    DSeriesKeyValueSubStructure,
    DSeriesListSubStructure,
    DSeriesNameKeyValueSubStructure,
    DSeriesNoParseSubStructure,
    DSeriesStructure,
)

DataClass.Config.arbitrary_types_allowed = True

TOLERANCE = 1e-10


class DSeriePoint(DataClass):
    """
        Converting points from geolib co-ordinate system to the d-settlement UI
        Internal setting of the geometry differs from API.
        Here co-ordinate system is the same as in the the d-settlement UI.
        So axis z of the geolib needs to be modified to y axis, which represents the depth.
    """

    id: PositiveInt = 1
    X: float
    Y: float
    Z: float

    tolerance: float = TOLERANCE

    @classmethod
    def from_point(cls, p: Point):
        return cls(X=p.x, Y=p.z, Z=p.y)

    def __eq__(self, other: object):
        if isinstance(other, DSeriePoint):
            return (
                isclose(self.X, other.X, abs_tol=self.tolerance)
                and isclose(self.Y, other.Y, abs_tol=self.tolerance)
                and isclose(self.Z, other.Z, abs_tol=self.tolerance)
            )
        return NotImplemented


class Soil(DSeriesNoParseSubStructure):
    name: str = "test soil"


class SoilCollection(DSeriesListSubStructure):
    soil: Union[List[Soil], List[str]] = []


class Version(DSeriesKeyValueSubStructure):
    soil: int = 1005
    geometry: int = 1000
    d__settlement: int = 1007


class Points(DSeriesNoParseSubStructure):
    """Representation of [POINTS] group."""

    points: List[DSeriePoint] = []

    def add_point_if_unique(self, point, tolerance=TOLERANCE) -> DSeriePoint:
        # tolerance = self.datastructure.geometry_data.accuracy.accuracy

        if point in self.points:
            point = self.points[self.points.index(point)]
        else:
            new_point_id = (
                max(self.points, key=attrgetter("id")).id + 1 if self.points else 1
            )
            point.id = new_point_id
            self.points.append(point)
        return point


class Curve(DataClass):
    """Curve is a Line consisting of two points (by reference)."""

    id: PositiveInt = 1
    points: conlist(DSeriePoint, min_items=2, max_items=2)

    def __eq__(self, other: object) -> bool:
        """
        Check if points in two lines are equal.

        Args:
            other (Line): an other line

        Returns: boolean

        """
        if not isinstance(other, Curve):
            raise NotImplementedError()
        else:
            return self.points == other.points


class Curves(DSeriesNoParseSubStructure):
    """Representation of [CURVES] group."""

    curves: List[Curve] = []

    def create_curve(self, a: DSeriePoint, b: DSeriePoint):

        curve = Curve(points=[a, b])
        if curve in self.curves:
            return self.curves[self.curves.index(curve)]
        else:
            new_curve_id = (
                max(self.curves, key=attrgetter("id")).id + 1
                if len(self.curves) > 0
                else 1
            )
            curve.id = new_curve_id
            self.curves.append(curve)

        return curve

    def create_curves(self, sorted_points: List[DSeriePoint]) -> List[Curve]:

        new_curves = [
            self.create_curve(sorted_points[i], sorted_points[i + 1])
            for i in range(len(sorted_points) - 1)
        ]
        return new_curves


class Boundary(DataClass):
    id: conint(ge=0) = 0
    curves: List[Curve] = []

    def area_above_horizontal(self, y: float = 0.0) -> float:
        """Area above horizontal line defined by y-coordinate."""
        area = 0.0

        for curve in self.curves:
            _y = curve.points[0].Y + curve.points[1].Y / 2 - y
            area += (curve.points[1].X - curve.points[0].X) * _y

        return area

    def __eq__(self, other: object) -> bool:
        """
        Check if curves in two Boundary are equal.

        Arguments:
            other (Boundary): an other Boundary

        Returns: boolean

        """
        if not isinstance(other, Boundary):
            raise NotImplementedError()
        else:
            return self.curves == other.curves


class Boundaries(DSeriesNoParseSubStructure):
    """Representation of [BOUNDARIES] group."""

    boundaries: List[Boundary] = []

    # Only do this before serializing, as it mutates
    # the ids of boundaries that we've already given
    # back to the user!
    def sort(self):
        # TODO Explain resorting
        self.boundaries.sort(key=lambda boundary: boundary.area_above_horizontal())
        for i, boundary in enumerate(self.boundaries):
            boundary.id = i

    def create_boundary(self, curves: List[Curve]) -> Boundary:
        boundary = Boundary(curves=curves)

        # Return the id of existing one
        if boundary in self.boundaries:
            return self.boundaries[self.boundaries.index(boundary)]
        else:
            new_boundary_id = (
                max(self.boundaries, key=attrgetter("id")).id + 1
                if len(self.boundaries) > 0
                else 0
            )
            boundary.id = new_boundary_id
            self.boundaries.append(boundary)

        return boundary


class Layer(DataClass):
    id: PositiveInt = 1
    material: str = ""  # reference to soil name
    piezo_top: int = 0  # reference to head line
    piezo_bottom: int = 0  # reference to head line
    boundary_top: int  # reference to boundary
    boundary_bottom: int  # reference to boundary

    def __eq__(self, other: object) -> bool:
        """
        Check if curves in two Boundary are equal.

        Arguments:
            other (Boundary): an other Boundary

        Returns: boolean

        """
        if not isinstance(other, Layer):
            raise NotImplementedError()
        else:
            return (
                self.boundary_top == other.boundary_top
                and self.boundary_bottom == other.boundary_bottom
            )


class Layers(DSeriesNoParseSubStructure):
    """Representation of [LAYERS] group."""

    layers: List[Layer] = []

    def add_layer(self, layer: Layer):

        if layer in self.layers:
            existing_layer = self.layers[self.layers.index(layer)]
            logging.warning(f"Layer {existing_layer} already exists")
            return existing_layer
        else:
            new_layer_id = (
                max(self.layers, key=attrgetter("id")).id + 1
                if len(self.layers) > 0
                else 1
            )
            layer.id = new_layer_id
            self.layers.append(layer)

        return layer


class Accuracy(DSeriesNoParseSubStructure):
    """Representation of [ACCURACY] group."""

    accuracy: confloat(ge=1e-10) = 1e-3


class GeometryData(DSeriesStructure):
    """Representation of [GEOMETRY DATA] group."""

    accuracy: Union[Accuracy, str] = Accuracy()
    points: Union[Points, str] = Points()
    curves: Union[Curves, str] = Curves()
    boundaries: Union[Boundaries, str] = Boundaries()
    use_probabilistic_defaults_boundaries: str = ""
    stdv_boundaries: str = ""
    distribution_boundaries: str = ""
    piezo_lines: str = ""
    phreatic_line: str = ""
    world_co__ordinates: str = ""
    layers: Union[Layers, str] = Layers()
    layerloads: str = ""


class PointForLoad(DataClass):
    """Different from DSeriePoint as it does not
    belong in [POINTS]."""

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
    """Representation of [RESIDUAL TIMES] group."""

    time_steps: List[conint(ge=0)] = []


class Verticals(DSeriesNoParseSubStructure):
    """Representation of [VERTICALS] group."""

    # total mesh is default value that is written in sli file but not read
    total_mesh: int = 100
    locations: List[DSeriePoint] = []


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
    """Representation of complete .sli file."""

    version: Version = Version()
    soil_collection: Union[SoilCollection, str] = SoilCollection()
    geometry_data: Union[GeometryData, str] = GeometryData()
    run_identification: str = ""
    model: str = ""
    verticals: Union[Verticals, str] = Verticals()
    water: str = ""
    non__uniform_loads: Union[NonUniformLoads, str] = NonUniformLoads()
    water_loads: str = ""
    other_loads: Union[OtherLoads, str] = OtherLoads()
    calculation_options: str = ""
    residual_times: Union[ResidualTimes, str] = ResidualTimes()
    filter_band_width: str = ""
    pore_pressure_meters: str = ""
    non__uniform_loads_pore_pressures: str = ""
    other_loads_pore_pressures: str = ""
    calculation_options_pore_pressures: str = ""
    vertical_drain: str = ""
    probabilistic_data: str = ""
    probabilistic_defaults: str = ""
    fit_options: str = ""
    fit_calculation: str = ""
    eps: str = ""
    fit: str = ""
