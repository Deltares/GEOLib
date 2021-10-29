import abc
from enum import Enum
from typing import Dict, List, Optional, Type, Union

from pydantic import PositiveInt, confloat

from geolib.models import BaseDataClass

from ...geometry.one import Point
from ...utils import snake_to_camel
from .internal import (
    AnalysisType,
    NullablePersistablePoint,
    OptionsType,
    PersistableBishopBruteForceSettings,
    PersistableBishopSettings,
    PersistableCircle,
    PersistableGeneticSlipPlaneConstraints,
    PersistableGridEnhancements,
    PersistablePoint,
    PersistableSearchArea,
    PersistableSearchGrid,
    PersistableSlipPlaneConstraints,
    PersistableSpencerGeneticSettings,
    PersistableSpencerSettings,
    PersistableTangentArea,
    PersistableTangentLines,
    PersistableTwoCirclesOnTangentLine,
    PersistableUpliftVanParticleSwarmSettings,
    PersistableUpliftVanSettings,
)


class DStabilityObject(BaseDataClass, metaclass=abc.ABCMeta):
    """Base Class for objects in the analysis module."""

    @abc.abstractmethod
    def _to_internal_datastructure(self):
        """Convert to internal datastructure"""
        raise NotImplementedError


class DStabilityAnalysisMethod(DStabilityObject):
    _analysis_type: AnalysisType

    @property
    def analysis_type(self) -> AnalysisType:
        return self._analysis_type


class DStabilityCircle(DStabilityObject):
    """Generates a circle object

    Args:
        center (Point): Center of the circle.
        radius (float): Radius of the circle.
    """

    center: Point
    radius: confloat(gt=0)

    def _to_internal_datastructure(self) -> PersistableCircle:
        return PersistableCircle(
            Center=PersistablePoint(X=self.center.x, Z=self.center.z), Radius=self.radius
        )


class DStabilitySearchGrid(DStabilityObject):
    """Generates a search grid object

    Args:
        bottom_left (Point): Bottom left position of the search grid.
        number_of_points_in_x (int): Number of points to the right
        number_of_points_in_z (int): Number op points upwards
        space (float): Space between the points in x and z direction
    """

    bottom_left: Point
    number_of_points_in_x: PositiveInt
    number_of_points_in_z: PositiveInt
    space: confloat(gt=0)

    def _to_internal_datastructure(self) -> PersistableSearchGrid:
        return PersistableSearchGrid(
            BottomLeft=PersistablePoint(X=self.bottom_left.x, Z=self.bottom_left.z),
            NumberOfPointsInX=self.number_of_points_in_x,
            NumberOfPointsInZ=self.number_of_points_in_z,
            Space=self.space,
        )


class DStabilitySearchArea(DStabilityObject):
    """Generates a search area object

    Args:
        height (float): Height of the search area.
        top_left (Point): Top left position of the search area
        width (float): Width of the search area
    """

    height: confloat(gt=0)
    top_left: Point
    width: confloat(gt=0)

    def _to_internal_datastructure(self) -> PersistableSearchArea:
        return PersistableSearchArea(
            Height=self.height,
            TopLeft=NullablePersistablePoint(X=self.top_left.x, Z=self.top_left.z),
            Width=self.width,
        )


class DStabilitySlipPlaneConstraints(DStabilityObject):
    """Generates a slip plane constraints object

    Args:
        is_size_constraints_enabled (bool): enabel size constraints, defaults to False
        is_zone_a_constraints_enabled (bool): enable constraints for zone A, defaults to False
        is_zone_b_constraints_enabled (bool): enable constraints for zone B, defaults to False
        minimum_slip_plane_depth (float): minimum slip plane depth, defaults to 0.0
        minimum_slip_plane_length (float): minimum slip plane length, defaults to 0.0
        width_zone_a (float): width of zone A, defaults to 0.0
        width_zone_b (float): width of zone B, defaults to 0.0
        x_left_zone_a (float): x coordinate of left point of zone A, defaults to 0.0
        x_left_zone_b (float): x coordinate of left point of zone B, defaults to 0.0
    """

    is_size_constraints_enabled: bool = False
    is_zone_a_constraints_enabled: bool = False
    is_zone_b_constraints_enabled: bool = False
    minimum_slip_plane_depth: float = 0.0
    minimum_slip_plane_length: float = 0.0
    width_zone_a: float = 0.0
    width_zone_b: float = 0.0
    x_left_zone_a: float = 0.0
    x_left_zone_b: float = 0.0

    def _to_internal_datastructure(self) -> PersistableSlipPlaneConstraints:
        data = {**{snake_to_camel(name): value for name, value in self.dict().items()}}
        return PersistableSlipPlaneConstraints(**data)


class DStabilityGeneticSlipPlaneConstraints(DStabilityObject):
    """Generates slip plane constraints object for the Spencer method

    Args:
        is_enabled (bool): Height of the search area.
        minimum_angle_between_slices (float): Minimum angle between slices, defaults to 0.
        minimum_thrust_line_percentage_inside_slices (float): Minimum thrustline percentage inside slices, defaults to 0.
    """

    is_enabled: bool = False
    minimum_angle_between_slices: float = 0.0
    minimum_thrust_line_percentage_inside_slices: float = 0.0

    def _to_internal_datastructure(self) -> PersistableGeneticSlipPlaneConstraints:
        data = {**{snake_to_camel(name): value for name, value in self.dict().items()}}
        return PersistableGeneticSlipPlaneConstraints(**data)


class DStabilityBishopAnalysisMethod(DStabilityAnalysisMethod):
    """Generates slip plane constraints object for the Bishop method

    Args:
        circle (DStabilityCircle): Bishop circle definition
    """

    _analysis_type: AnalysisType = AnalysisType.BISHOP
    circle: DStabilityCircle

    def _to_internal_datastructure(self) -> PersistableBishopSettings:
        return PersistableBishopSettings(Circle=self.circle._to_internal_datastructure())


class DStabilityBishopBruteForceAnalysisMethod(DStabilityAnalysisMethod):
    """Generates slip plane constraints object for the Bishop Brute Force method

    Args:
        extrapolate_search_space (bool): Extrapolate the search space, defaults to True
        search_grid (DStabilitySearchGrid):
        slip_plane_constraints (DStabilitySlipPlaneConstraints):
        bottom_tangent_line_z (float):
        number_of_tangent_lines (int):
        space_tangent_lines (float):
    """

    _analysis_type: AnalysisType = AnalysisType.BISHOP_BRUTE_FORCE
    extrapolate_search_space: bool = True
    search_grid: DStabilitySearchGrid
    slip_plane_constraints: DStabilitySlipPlaneConstraints = (
        DStabilitySlipPlaneConstraints()
    )
    bottom_tangent_line_z: float
    number_of_tangent_lines: PositiveInt
    space_tangent_lines: confloat(gt=0)

    def _to_internal_datastructure(self) -> PersistableBishopBruteForceSettings:
        return PersistableBishopBruteForceSettings(
            GridEnhancements=PersistableGridEnhancements(
                ExtrapolateSearchSpace=self.extrapolate_search_space
            ),
            SearchGrid=self.search_grid._to_internal_datastructure(),
            SlipPlaneConstraints=self.slip_plane_constraints._to_internal_datastructure(),
            TangentLines=PersistableTangentLines(
                BottomTangentLineZ=self.bottom_tangent_line_z,
                NumberOfTangentLines=self.number_of_tangent_lines,
                Space=self.space_tangent_lines,
            ),
        )


class DStabilitySpencerAnalysisMethod(DStabilityAnalysisMethod):
    """Generates slip plane for the Spencer method

    Args:
        slipplane ([Point]): The points of the slipplane
    """

    _analysis_type: AnalysisType = AnalysisType.SPENCER
    slipplane: List[Point]

    def _to_internal_datastructure(self) -> PersistableSpencerSettings:
        return PersistableSpencerSettings(
            SlipPlane=[PersistablePoint(X=point.x, Z=point.z) for point in self.slipplane]
        )


class DStabilitySpencerGeneticAnalysisMethod(DStabilityAnalysisMethod):
    """Generates the input for the genetic spencer algorithm

    Args:
        options_type (OptionsType): DEFAULT or THOROUGH, defaults to DEFAULT
        slip_plane_a (List[Point]): upper slip plane boundary
        slip_plane_b (List[Point]): lower slip line boundary
        slip_plane_constraints (DStabilityGeneticSlipPlaneConstraints): constraints for the slip plane
    """

    _analysis_type: AnalysisType = AnalysisType.SPENCER_GENETIC
    options_type: OptionsType = OptionsType.DEFAULT
    slip_plane_a: List[Point]
    slip_plane_b: List[Point]
    slip_plane_constraints: DStabilityGeneticSlipPlaneConstraints = (
        DStabilityGeneticSlipPlaneConstraints()
    )

    def _to_internal_datastructure(self) -> PersistableSpencerGeneticSettings:
        return PersistableSpencerGeneticSettings(
            OptionsType=self.options_type,
            SlipPlaneA=[
                PersistablePoint(X=point.x, Z=point.z) for point in self.slip_plane_a
            ],
            SlipPlaneB=[
                PersistablePoint(X=point.x, Z=point.z) for point in self.slip_plane_b
            ],
            SlipPlaneConstraints=self.slip_plane_constraints._to_internal_datastructure(),
        )


class DStabilityUpliftVanAnalysisMethod(DStabilityAnalysisMethod):
    """Generates the input for the uplift van analysis

    Args:
        first_circle (DStabilityCircle): The location of the left circle for the slipplane.
        second_circle_center (Point): The center of the circle on the right side of the slipplane
    """

    _analysis_type: AnalysisType = AnalysisType.UPLIFT_VAN
    first_circle: DStabilityCircle
    second_circle_center: Point

    def _to_internal_datastructure(self) -> PersistableUpliftVanSettings:
        return PersistableUpliftVanSettings(
            SlipPlane=PersistableTwoCirclesOnTangentLine(
                FirstCircleCenter=NullablePersistablePoint(
                    X=self.first_circle.center.x, Z=self.first_circle.center.z
                ),
                FirstCircleRadius=self.first_circle.radius,
                SecondCircleCenter=NullablePersistablePoint(
                    X=self.second_circle_center.x, Z=self.second_circle_center.z
                ),
            )
        )


class DStabilityUpliftVanParticleSwarmAnalysisMethod(DStabilityAnalysisMethod):
    """Generates the input for the uplift van analysis

    Args:
        options_type (OptionsType): DEFAULT or THOROUGH, defaults to DEFAULT
        search_area_a (DStabilitySearchArea): The search area for the circle on the left side of the slip plane
        search_area_b (DStabilitySearchArea): The search area for the circle on the right side of the slip plane
        slip_plane_constraints (DStabilitySlipPlaneConstraints): Slip plane constraints
        tangent_area_height (float): height of the tangent lines search area
        tangent_area_top_z (float): top z coordinate of the tangent lines area
    """

    _analysis_type: AnalysisType = AnalysisType.UPLIFT_VAN_PARTICLE_SWARM
    options_type: OptionsType = OptionsType.DEFAULT
    search_area_a: DStabilitySearchArea
    search_area_b: DStabilitySearchArea
    slip_plane_constraints: DStabilitySlipPlaneConstraints = (
        DStabilitySlipPlaneConstraints()
    )
    tangent_area_height: float
    tangent_area_top_z: float

    def _to_internal_datastructure(self) -> PersistableUpliftVanParticleSwarmSettings:
        return PersistableUpliftVanParticleSwarmSettings(
            OptionsType=self.options_type,
            SearchAreaA=self.search_area_a._to_internal_datastructure(),
            SearchAreaB=self.search_area_b._to_internal_datastructure(),
            SlipPlaneConstraints=self.slip_plane_constraints._to_internal_datastructure(),
            TangentArea=PersistableTangentArea(
                Height=self.tangent_area_height, TopZ=self.tangent_area_top_z
            ),
        )
