import logging
from enum import Enum, IntEnum
from inspect import cleandoc
from math import isclose
from operator import attrgetter
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic.types import PositiveInt, confloat, conint, conlist, constr

from geolib.geometry.one import Point
from geolib.models import BaseDataClass
from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.dseries_parser import (
    DSerieListStructure,
    DSerieMatrixStructure,
    DSerieOldTableStructure,
    DSeriesInlineMappedProperties,
    DSeriesMatrixTreeStructureCollection,
    DSeriesNoParseSubStructure,
    DSeriesRepeatedGroupedProperties,
    DSeriesStructure,
    DSeriesStructureCollection,
    DSeriesTableStructure,
    DSeriesTreeStructure,
    DSeriesTreeStructureCollection,
    DSeriesUnmappedNameProperties,
    DSerieVersion,
)
from geolib.models.dsettlement.dsettlement_structures import (
    ComplexVerticalSubstructure,
    DSerieRepeatedTableStructure,
)
from geolib.models.dsettlement.internal_soil import SoilInternal
from geolib.models.dsettlement.probabilistic_calculation_types import (
    ProbabilisticCalculationType,
)
from geolib.models.internal import Bool
from geolib.models.utils import get_required_class_field
from geolib.soils import DistributionType, HorizontalBehaviourType, Soil
from geolib.soils import StorageTypes as StorageTypes_external
from geolib.utils import make_newline_validator

from .drain_types import DrainGridType, DrainSchedule, DrainType

logger = logging.getLogger(__name__)


TOLERANCE = 1e-10
ZERO_ITEMS = "    0 = number of items"
REQ_RUN_LINES = 2


class DSeriePoint(DSeriesTreeStructure):
    """
    Converting points from geolib co-ordinate system to the d-settlement UI
    Internal setting of the geometry differs from API.
    Here co-ordinate system is the same as in the the d-settlement UI.
    So axis z of the geolib needs to be modified to y axis, which represents the depth.
    """

    id: PositiveInt
    X: float
    Y: float
    Z: float

    tolerance: float = TOLERANCE

    @classmethod
    def get_structure_required_fields(cls) -> List[Tuple[str, Type]]:
        point_required_field_names = [
            required_field[0] for required_field in get_required_class_field(cls)
        ]
        return [
            field_tuple
            for field_tuple in super().get_structure_required_fields()
            if field_tuple[0] in point_required_field_names
        ]

    @classmethod
    def from_point(cls, p: Point):
        return cls(id=1, X=p.x, Y=p.z, Z=p.y)

    def __eq__(self, other: object):
        if isinstance(other, DSeriePoint):
            return (
                isclose(self.X, other.X, abs_tol=self.tolerance)
                and isclose(self.Y, other.Y, abs_tol=self.tolerance)
                and isclose(self.Z, other.Z, abs_tol=self.tolerance)
            )
        return NotImplemented


class SoilCollection(DSeriesStructureCollection):
    soil: List[SoilInternal] = []

    def add_soil_if_unique(self, soil, tolerance=TOLERANCE) -> None:
        for added_soil in self.soil:
            if soil.name == added_soil.name:
                raise NameError(f"Soil with name {soil.name} already exists.")
        self.soil.append(soil)


class Version(DSerieVersion):
    soil: int = 1005
    geometry: int = 1000
    d__settlement: int = 1007


class Points(DSeriesMatrixTreeStructureCollection):
    """Representation of [POINTS] group."""

    points: List[DSeriePoint] = []

    def add_point_if_unique(self, point: DSeriePoint, tolerance=TOLERANCE) -> DSeriePoint:
        if point in self.points:
            point = self.points[self.points.index(point)]
        else:
            point = self.add_point(point)
        return point

    def add_point(self, point: DSeriePoint) -> DSeriePoint:
        new_point_id = max(self.points, key=attrgetter("id")).id + 1 if self.points else 1
        point.id = new_point_id
        self.points.append(point)
        return point

    def __getitem__(self, point_id: int) -> Point:
        for point in self.points:
            if point.id == point_id:
                return point
        raise KeyError(f"Can't find point with id {point_id}.")


class Curve(DSeriesTreeStructure):
    """Curve is a Line consisting of two points (by reference)."""

    id: PositiveInt = 1
    points: conlist(int, min_items=2, max_items=2)

    def __eq__(self, other: object) -> bool:
        """
        Check if points in two lines are equal.

        Args:
            other (Line): an other line

        Returns: boolean

        """
        if not isinstance(other, Curve):
            return NotImplemented
        else:
            return self.points == other.points


class Curves(DSeriesTreeStructureCollection):
    """Representation of [CURVES] group."""

    curves: List[Curve] = []

    def create_curve(self, a: DSeriePoint, b: DSeriePoint):
        assert a.id != b.id
        curve = Curve(points=[a.id, b.id])
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

    def __getitem__(self, curve_id: int) -> Curve:
        for curve in self.curves:
            if curve.id == curve_id:
                return curve
        raise KeyError(f"Can't find curve with id {curve_id}.")


class Boundary(DSeriesTreeStructure):
    id: conint(ge=0) = 0
    curves: List[int] = []

    def __eq__(self, other: object) -> bool:
        """
        Check if curves in two Boundary are equal.

        Arguments:
            other (Boundary): an other Boundary

        Returns: boolean

        """
        if not isinstance(other, Boundary):
            return NotImplemented
        else:
            return self.curves == other.curves


class Boundaries(DSeriesTreeStructureCollection):
    """Representation of [BOUNDARIES] group."""

    boundaries: List[Boundary] = []

    def create_boundary(self, curves: List[Curve]) -> Boundary:
        boundary = Boundary(curves=[curve.id for curve in curves])

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

    def __getitem__(self, boundary_id: int) -> Boundary:
        for boundary in self.boundaries:
            if boundary.id == boundary_id:
                return boundary
        raise KeyError(f"Can't find boundary with id {boundary_id}.")


class Layer(DSeriesTreeStructure):
    id: PositiveInt = 1
    material: str = ""  # reference to soil name
    piezo_top: conint(ge=0, le=99) = 0  # reference to head line
    piezo_bottom: conint(ge=0, le=99) = 0  # reference to head line
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
            return NotImplemented
        else:
            return (
                self.boundary_top == other.boundary_top
                and self.boundary_bottom == other.boundary_bottom
            )


class Layers(DSeriesTreeStructureCollection):
    """Representation of [LAYERS] group."""

    layers: List[Layer] = []

    def add_layer(self, layer: Layer):

        if layer in self.layers:
            existing_layer = self.layers[self.layers.index(layer)]
            logger.warning(
                f"It's not possible to replace existing layers: {existing_layer}"
            )
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

    def __getitem__(self, layer_id: int) -> Layer:
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        raise KeyError(f"Can't find layer with id {layer_id}.")


class PiezoLine(DSeriesTreeStructure):
    id: PositiveInt = 1
    curves: List[int] = []

    def __eq__(self, other: object):
        if isinstance(other, PiezoLine):
            return self.curves == other.curves
        return NotImplemented


class PiezoLines(DSeriesTreeStructureCollection):
    """Representation of [PIEZO LINES] group."""

    piezolines: List[PiezoLine] = []

    def create_piezoline(self, curves: List[Curve]) -> PiezoLine:
        piezoline = PiezoLine(curves=[curve.id for curve in curves])

        if piezoline in self.piezolines:
            return self.piezolines[self.piezolines.index(piezoline)]
        else:
            new_piezoline_id = (
                max(self.piezolines, key=attrgetter("id")).id + 1
                if len(self.piezolines) > 0
                else 1
            )
            piezoline.id = new_piezoline_id
            self.piezolines.append(piezoline)
        return piezoline

    def __getitem__(self, piezo_line_id: int) -> PiezoLine:
        for piezo_line in self.piezolines:
            if piezo_line.id == piezo_line_id:
                return piezo_line
        raise KeyError(f"Can't find headline with id {piezo_line_id}.")


class UseProbabilisticDefaultsBoundaries(DSerieListStructure):
    useprobabilisticdefaultsboundaries: List[Bool] = []

    def append_use_probabilistic_defaults_boundary(
        self, use_probabilistic_boundary: bool
    ):
        self.useprobabilisticdefaultsboundaries.append(
            Bool(int(use_probabilistic_boundary))
        )


class StdvBoundaries(DSerieListStructure):
    stdvboundaries: List[float] = []

    def append_stdv_boundary(self, stdv_boundary: float):
        self.stdvboundaries.append(stdv_boundary)


class DistributionBoundaries(DSerieListStructure):
    distributionboundaries: List[DistributionType] = []

    def append_distribution_boundary(self, distribution_boundary: DistributionType):
        if (distribution_boundary is DistributionType.Normal) or (
            distribution_boundary is DistributionType.Undefined
        ):
            self.distributionboundaries.append(distribution_boundary)
        else:
            raise ValueError(
                f"Enumeration member {repr(distribution_boundary)} is not supported for probabilistic boundary, please select Normal Distribution"
            )


class Accuracy(DSeriesUnmappedNameProperties):
    accuracy: confloat(ge=1e-10) = 1e-3


class PhreaticLine(DSeriesUnmappedNameProperties):
    phreatic_line: conint(ge=0, lt=99) = 0


class GeometryData(DSeriesStructure):
    """Representation of [GEOMETRY DATA] group."""

    accuracy: Accuracy = Accuracy()
    points: Points = Points()
    curves: Curves = Curves()
    boundaries: Boundaries = Boundaries()
    use_probabilistic_defaults_boundaries: UseProbabilisticDefaultsBoundaries = (
        UseProbabilisticDefaultsBoundaries()
    )
    stdv_boundaries: StdvBoundaries = StdvBoundaries()
    distribution_boundaries: DistributionBoundaries = DistributionBoundaries()
    piezo_lines: PiezoLines = PiezoLines()
    phreatic_line: PhreaticLine = PhreaticLine()
    world_co__ordinates: str = cleandoc(
        """
          0.000 - X world 1 -
          0.000 - Y world 1 -
          0.000 - X world 2 -
          0.000 - Y world 2 -
          """
    )
    layers: Layers = Layers()
    layerloads: str = ""

    def boundary_area_above_horizontal(self, boundary: Boundary, y: float = 0.0) -> float:
        """Area above horizontal line defined by y-coordinate."""
        area = 0.0

        for curve_id in boundary.curves:
            curve = self.get_curve(curve_id)
            points = [self.get_point(pid) for pid in curve.points]
            _y = (points[0].Y + points[1].Y) / 2 - y
            area += (points[1].X - points[0].X) * _y

        return area

    # Only do this before serializing, as it mutates
    # the ids of boundaries that we've already given
    # back to the user!
    def sort_boundaries(self):
        self.boundaries.boundaries.sort(
            key=lambda boundary: self.boundary_area_above_horizontal(boundary)
        )
        # sort probabilistic values
        self.sort_probabilistic_list_based_on_new_indexes()

        for i, boundary in enumerate(self.boundaries.boundaries):
            for layer in self.layers.layers:
                if layer.boundary_top == boundary.id:
                    layer.boundary_top = i
                if layer.boundary_bottom == boundary.id:
                    layer.boundary_bottom = i

            if boundary.id != i:
                logger.warning(
                    f"Boundary id {boundary.id} has changed to {i} in sorting process"
                )
            boundary.id = i

    def sort_probabilistic_list_based_on_new_indexes(self):
        new_indexes = self.create_list_of_indexes()
        self.use_probabilistic_defaults_boundaries.useprobabilisticdefaultsboundaries = self.sort_based_on_new_indexes(
            new_indexes,
            self.use_probabilistic_defaults_boundaries.useprobabilisticdefaultsboundaries,
        )
        self.stdv_boundaries.stdvboundaries = self.sort_based_on_new_indexes(
            new_indexes, self.stdv_boundaries.stdvboundaries,
        )
        self.distribution_boundaries.distributionboundaries = self.sort_based_on_new_indexes(
            new_indexes, self.distribution_boundaries.distributionboundaries,
        )

    def pre_process(self):
        self.sort_boundaries()
        self.sort_probabilistic_list_based_on_new_indexes()

    def create_list_of_indexes(self) -> List:
        return [boundary.id for boundary in self.boundaries.boundaries]

    def sort_based_on_new_indexes(self, new_indexes: List, unsorted_list: List) -> List:
        return [unsorted_list[i] for i in new_indexes]

    def get_point(self, point_id: int) -> Optional[DSeriePoint]:
        return self.points[point_id]

    def get_curve(self, curve_id: int) -> Optional[Curve]:
        return self.curves[curve_id]

    def get_boundary(self, boundary_id: int) -> Optional[Boundary]:
        return self.boundaries[boundary_id]

    def get_layer(self, layer_id: int) -> Optional[Layer]:
        return self.layers[layer_id]


class PointForLoad(BaseDataClass):
    """Different from DSeriePoint as it does not
    belong in [POINTS]."""

    X: float
    Y: float

    @classmethod
    def from_point(cls, p: Point):
        return cls(X=p.x, Y=p.z)


class NonUniformLoad(BaseDataClass):
    time: int = 0
    gammadry: float = 10
    gammawet: float = 10
    temporary: Bool = False
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
            return None


class WaterLoad(BaseDataClass):
    name: str = ""
    time: int = 0
    phreatic_line: int = 1
    headlines: List[List[int]] = [[]]


class WaterLoads(DSeriesNoParseSubStructure):
    """Representation of [WATER LOADS] group."""

    waterloads: List[WaterLoad] = []

    def add_waterload(
        self, name: str, time: int, phreatic_line: int, headlines: List[List[int]]
    ):
        self.waterloads.append(
            WaterLoad(
                name=name, time=time, phreatic_line=phreatic_line, headlines=headlines
            )
        )


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


class LoadValuesTrapeziform(BaseDataClass):
    gamma: float = 0
    height: float = 0
    xl: float = 0
    xm: float = 0
    xr: float = 0
    Xp: float = 0
    Yp: float = 0


class LoadValuesCircular(BaseDataClass):
    weight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    R: float = 0.01


class LoadValuesRectangular(BaseDataClass):
    weight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    xwidth: float = 0.01
    zwidth: float = 0.01


class LoadValuesUniform(BaseDataClass):
    unit_weight: float = 0
    gamma: float = 0
    height: float = 0
    y_application: float = 0


class LoadValuesTank(BaseDataClass):
    wallweight: float = 0
    internalweight: float = 0
    alpha: float = 0
    Xcp: float = 0
    Ycp: float = 0
    Zcp: float = 0
    Rintern: float = 0.01
    dWall: float = 0.01


class OtherLoad(BaseDataClass):
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
            return None


class Dimension(Enum):
    ONE_D = 0
    TWO_D = 1


class ConsolidationModel(Enum):
    DARCY = 0
    TERZAGHI = 1


class SoilModel(Enum):
    NEN_KOPPEJAN = 0
    NEN_BJERRUM = 1
    ISOTACHE = 2


class StrainType(Enum):
    LINEAR = 0
    NATURAL = 1


class Model(DSeriesNoParseSubStructure):
    dimension: Dimension = Dimension.TWO_D
    consolidation_model: ConsolidationModel = ConsolidationModel.DARCY
    soil_model: SoilModel = SoilModel.NEN_KOPPEJAN
    strain_type: StrainType = StrainType.LINEAR
    is_vertical_drains: Bool = Bool.FALSE
    is_fit_for_settlement_plate: Bool = Bool.FALSE
    is_probabilistic: Bool = Bool.FALSE
    is_horizontal_displacements: Bool = Bool.FALSE
    is_secondary_swelling: Bool = Bool.FALSE
    is_waspan: Bool = Bool.FALSE


class PreconPressureWithinLayer(Enum):
    CONSTANT_NO_CORRECTION = 0
    CONSTANT_CORRECTION_T0 = 1
    CONSTANT_CORRECTION_ALL_T = 2
    VARIABLE_NO_CORRECTION = 3
    VARIABLE_CORRECTION_T0 = 4
    VARIABLE_CORRECTION_ALL_T = 5


class DispersionConditionLayerBoundary(Enum):
    UNDRAINED = 0
    DRAINED = 1


class DispersionConditionsLayerBoundaries(DSeriesNoParseSubStructure):
    dispersion_conditions_layer_boundaries_top: DispersionConditionLayerBoundary = (
        DispersionConditionLayerBoundary.DRAINED
    )
    dispersion_conditions_layer_boundaries_bottom: DispersionConditionLayerBoundary = (
        DispersionConditionLayerBoundary.DRAINED
    )


class StressDistributionSoil(Enum):
    BUISMAN = 0
    BOUSSINESQ = 1


class StressDistributionLoads(Enum):
    NONE = 0
    SIMULATE = 1


class CalculationOptions(DSeriesNoParseSubStructure):
    precon_pressure_within_layer: PreconPressureWithinLayer = (
        PreconPressureWithinLayer.CONSTANT_NO_CORRECTION
    )
    is_imaginary_surface: Bool = Bool.FALSE
    imaginary_surface_layer: Optional[PositiveInt]
    is_submerging: Bool = Bool.FALSE
    use_end_time_for_fit: Bool = Bool.FALSE
    is_maintain_profile: Bool = Bool.FALSE
    maintain_profile_material_name: str = "Superelevation"
    maintain_profile_time: conint(ge=0, le=100000) = 0
    maintain_profile_gamma_dry: confloat(ge=-100, le=100) = 10
    maintain_profile_gamma_wet: confloat(ge=-100, le=100) = 10
    dispersion_conditions_layer_boundaries_top: DispersionConditionLayerBoundary = (
        DispersionConditionLayerBoundary.DRAINED
    )
    dispersion_conditions_layer_boundaries_bottom: DispersionConditionLayerBoundary = (
        DispersionConditionLayerBoundary.DRAINED
    )
    stress_distribution_soil: StressDistributionSoil = StressDistributionSoil.BUISMAN
    stress_distribution_loads: StressDistributionLoads = StressDistributionLoads.SIMULATE
    iteration_stop_criteria_submerging: confloat(ge=0.0, le=1.0) = 0.0
    iteration_stop_criteria_submerging_layer_height: confloat(ge=0, le=99.999) = 0
    maximum_iteration_steps_for_submerging: conint(ge=1, le=100) = 1
    iteration_stop_criteria_desired_profile: confloat(ge=0, le=1) = 0.1
    load_column_width_imaginary_surface: confloat(ge=0.05, le=10000) = 1
    load_column_width_non_uniform_loads: confloat(ge=0.05, le=10000) = 1
    load_column_width_trapeziform_loads: confloat(ge=0.05, le=10000) = 1
    end_of_consolidation: conint(ge=1, le=100000) = 100000
    number_of_subtime_steps: conint(ge=1, le=100) = 2
    reference_time: confloat(ge=0.001, le=1000000) = 1
    dissipation: Bool = Bool.FALSE
    x_coord_dissipation: float = 0.0
    use_fit_factors: Bool = Bool.FALSE
    x_coord_fit: float = 0.0
    is_predict_settlements_omitting_additional_load_steps: Bool = Bool.FALSE

    @classmethod
    def set_options(cls, **kwargs):
        cls_instance = cls(**kwargs)
        if cls_instance.is_imaginary_surface == Bool.FALSE:
            cls_instance.imaginary_surface_layer = None
        elif cls_instance.imaginary_surface_layer is None:
            cls_instance.imaginary_surface_layer = 1
        return cls_instance


class VerticalDrain(DSeriesNoParseSubStructure):
    # geometry of drain
    drain_type: DrainType = DrainType.STRIP
    range_from: confloat(ge=-10000000.000, le=10000000.000) = 0
    range_to: confloat(ge=-10000000.000, le=10000000.000) = 0
    bottom_position: confloat(ge=-10000000.000, le=10000000.000) = 0
    center_to_center: confloat(ge=0.001, le=1000) = 3
    width: confloat(ge=0.001, le=1000) = 0.1
    diameter: confloat(ge=0.001, le=1000) = 0.1
    thickness: confloat(ge=0.001, le=1000) = 0.003
    grid: DrainGridType = DrainGridType.UNDERDETERMINED
    # schedule
    schedule_type: DrainSchedule = DrainSchedule.OFF
    begin_time: confloat(ge=0, le=100000) = 0
    end_time: confloat(ge=0, le=100000) = 0
    under_pressure_for_strips_and_columns: confloat(ge=0, le=100000) = 35
    under_pressure_for_sand_wall: confloat(ge=0, le=100000) = 35
    start_of_drainage: confloat(ge=0, le=100000) = 0
    phreatic_level_in_drain: confloat(ge=-10000000.000, le=10000000.000) = 0
    water_head_during_dewatering: confloat(
        ge=-10000000.000, le=10000000.000
    ) = 0  # relevant for strip and column
    tube_pressure_during_dewatering: confloat(
        ge=-10000000.000, le=10000000.000
    ) = 0  # relevant for the sand wall
    time: List[confloat(ge=0, le=100000)] = []
    underpressure: List[confloat(ge=0, le=100000)] = []
    water_level: List[confloat(ge=-10000000.000, le=10000000.000)] = []


class InternalProbabilisticCalculationType(IntEnum):
    FOSMOrDeterministic = 0
    ProbabilityOfFailureFORM = 1
    BandWidthAndProbabilityOfFailureMonteCarlo = 2


class ProbabilisticData(DSeriesInlineMappedProperties):
    reliability_x_co__ordinate: float = 0
    residual_settlement: confloat(ge=0, le=1000) = 1
    maximum_drawings: conint(ge=0, le=999999999) = 100
    maximum_iterations: conint(ge=1, le=50) = 15
    reliability_type: InternalProbabilisticCalculationType = (
        InternalProbabilisticCalculationType.FOSMOrDeterministic
    )
    is_reliability_calculation: Bool = Bool.FALSE

    def set_probabilistic_data(
        self,
        point_of_vertical: Point,
        residual_settlement: float,
        maximum_number_of_samples: int,
        maximum_iterations: int,
        reliability_type: ProbabilisticCalculationType,
        is_reliability_calculation: bool,
    ):
        if (
            reliability_type == ProbabilisticCalculationType.SettlementsDeterministic
            and is_reliability_calculation
        ):
            raise ValueError(
                f"is_reliability_calculation is set to True but reliability type {repr(reliability_type)} is not probabilistic."
            )
        return ProbabilisticData(
            reliability_x_co__ordinate=point_of_vertical.x,
            residual_settlement=residual_settlement,
            maximum_drawings=maximum_number_of_samples,
            maximum_iterations=maximum_iterations,
            reliability_type=self.externaltointernalprobabilisticcalculationtype(
                reliability_type
            ),
            is_reliability_calculation=Bool(int(is_reliability_calculation)),
        )

    def externaltointernalprobabilisticcalculationtype(
        self, reliability_type: ProbabilisticCalculationType
    ) -> InternalProbabilisticCalculationType:
        map_values = {
            -1: InternalProbabilisticCalculationType.FOSMOrDeterministic,
            0: InternalProbabilisticCalculationType.FOSMOrDeterministic,
            1: InternalProbabilisticCalculationType.ProbabilityOfFailureFORM,
            2: InternalProbabilisticCalculationType.BandWidthAndProbabilityOfFailureMonteCarlo,
        }
        return map_values[reliability_type.value]


class DSettlementStructure(DSeriesStructure):
    """Representation of complete .sli file."""

    version: Version = Version()
    soil_collection: SoilCollection = SoilCollection()
    geometry_data: GeometryData = GeometryData()
    geometry_1d_data: Optional[str]
    run_identification: str = 2 * "\n"
    model: Union[Model, str] = Model()
    verticals: Union[Verticals, str] = Verticals()
    water: Union[float, str] = 9.81
    non__uniform_loads: Union[NonUniformLoads, str] = NonUniformLoads()
    water_loads: Union[WaterLoads, str] = WaterLoads()
    other_loads: Union[OtherLoads, str] = OtherLoads()
    calculation_options: Union[CalculationOptions, str] = CalculationOptions()
    residual_times: Union[ResidualTimes, str] = ResidualTimes()
    filter_band_width: str = cleandoc(
        """
        1 : Number of items
        0.05
        """
    )
    pore_pressure_meters: str = ZERO_ITEMS
    non__uniform_loads_pore_pressures: str = ZERO_ITEMS
    other_loads_pore_pressures: str = ZERO_ITEMS
    calculation_options_pore_pressures: str = cleandoc(
        """
        1 : Shear stress = TRUE
        1 : calculation method of lateral stress ratio (k0) = Nu
        """
    )
    vertical_drain: Union[VerticalDrain, str] = VerticalDrain()
    probabilistic_data: ProbabilisticData = ProbabilisticData()
    probabilistic_defaults: str = cleandoc(
        """
        ProbDefGamDryVar=0.05
        ProbDefGamWetVar=0.05
        ProbDefPOPVar=0.25
        ProbDefOCRVar=0.25
        ProbDefPcVar=0.25
        ProbDefPermeabilityVerVar=2.50
        ProbDefRatioHorVerPermeabilityCvVar=0.25
        ProbDefCvVar=0.50
        ProbDefCpVar=0.30
        ProbDefCp1Var=0.30
        ProbDefCsVar=0.30
        ProbDefCs1Var=0.30
        ProbDefApVar=0.30
        ProbDefASecVar=0.30
        ProbDefRRCrVar=0.25
        ProbDefCRCcVar=0.25
        ProbDefCaVar=0.25
        ProbDefPriCompIndexVar=0.25
        ProbDefSecCompIndexVar=0.25
        ProbDefSecCompRateVar=0.25
        ProbDefCpCor=0.01
        ProbDefCsCor=0.01
        ProbDefCs1Cor=0.01
        ProbDefApCor=0.01
        ProbDefASecCor=0.01
        ProbDefRRCrCor=0.01
        ProbDefCaCor=0.01
        ProbDefPriCompIndexCor=0.01
        ProbDefSecCompRateCor=0.01
        ProbDefGamDryDist=2
        ProbDefGamWetDist=2
        ProbDefPOPDist=2
        ProbDefOCRDist=2
        ProbDefPcDist=2
        ProbDefPermeabilityVerDist=2
        ProbDefRatioHorVerPermeabilityCvDist=2
        ProbDefCvDist=2
        ProbDefCpDist=2
        ProbDefCp1Dist=2
        ProbDefCsDist=2
        ProbDefCs1Dist=2
        ProbDefApDist=2
        ProbDefASecDist=2
        ProbDefRRCrDist=2
        ProbDefCRCcDist=2
        ProbDefCaDist=2
        ProbDefPriCompIndexDist=2
        ProbDefSecCompIndexDist=2
        ProbDefSecCompRateDist=2
        ProbDefLayerStd=0.10
        ProbDefLayerDist=0
        """
    )
    fit_options: str = cleandoc(
        """
        Fit Maximum Number of Iterations=5
        Fit Required Iteration Accuracy=0.0001000000
        Fit Required Correlation Coefficient=0.990
        """
    )
    fit_calculation: str = cleandoc(
        """
        Is Fit Calculation=0
        Fit Vertical Number=-1
        """
    )
    eps: str = cleandoc(
        """
        0.00 = Dry unit weight
        0.00 = Saturated unit weight
        0.00 = Load
        0.00 = Height above surface
        """
    )
    fit: str = ZERO_ITEMS

    # Custom validator
    _validate_run_identification = make_newline_validator(
        "run_identification", req_newlines=REQ_RUN_LINES
    )

    def validate_options(self):
        """
        Todo validation calculation options with geometry. I.e. validate x coordinate related options and layer related
            options
        Returns:

        """

    def check_x_in_vertical(self, point_of_vertical: Point):
        check_that_x_in_verticals = False
        for point in self.verticals.locations:
            if abs(point.X - point_of_vertical.x) <= point_of_vertical.tolerance:
                check_that_x_in_verticals = True
        if not (check_that_x_in_verticals):
            raise ValueError(
                f"The x-coordinate of point_of_vertical does not correspond to an existing vertical."
            )

    def get_headlines_for_layers(self):
        return [[l.piezo_top, l.piezo_bottom] for l in self.geometry_data.layers.layers]


class Stresses(DSeriesTableStructure):
    stresses: List[Dict[str, float]]


class KoppejanSettlements(DSeriesTableStructure):
    koppejansettlements: List[Dict[str, float]]


class Depths(DSerieListStructure):
    depths: List[float]


class Leakages(DSerieListStructure):
    leakages: List[float]


class DrainedLayers(DSerieListStructure):
    drainedlayers: List[int]


class TimeSettlementPerLoad(DSerieMatrixStructure):
    timesettlementperload: List[List[float]]


class HorizontalDisplacements(DSerieMatrixStructure):
    horizontaldisplacements: List[List[float]]


class TimeDependentData(DSerieRepeatedTableStructure):
    timedependentdata: Dict[float, List[Dict[str, float]]]


class Vertical(ComplexVerticalSubstructure):
    """Representation of [Vertical] group in sld file."""

    id: int
    x: float
    z: float
    time__settlement_per_load: Optional[TimeSettlementPerLoad]
    depths: Depths
    leakages: Optional[Leakages]
    drained_layers: Optional[DrainedLayers]
    stresses: Optional[Stresses]
    koppejan_settlement: Optional[KoppejanSettlements]
    time__dependent_data: List[TimeDependentData]
    elasticity: Optional[float]
    horizontal_displacements: Optional[HorizontalDisplacements]


class ResidualSettlements(DSerieOldTableStructure):
    # TODO LIst[Dict[str, float]] but can be empty which now gives a validation error
    residualsettlements: List[Dict[str, float]]


class Results(DSeriesRepeatedGroupedProperties):
    """Representation of [results] group in sld file."""

    verticals_count: int
    vertical: List[Vertical]
    residual_settlements: List[ResidualSettlements]
    amounts_of_loads: Optional[str]
    dissipation_in_layers: Optional[str]
    reliability_calculation_results: Optional[str]


class DSettlementOutputStructure(DSeriesStructure):
    """Representation of complete .sld file, inherting
    the structure of the .sli file as well."""

    results: Results
    input_data: DSettlementStructure
