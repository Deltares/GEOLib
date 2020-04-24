from datetime import timedelta
from typing import List, Optional, Type

from pydantic import BaseModel as DataClass
from pydantic import FilePath
from pydantic.types import confloat

from geolib.geometry import Point
from geolib.models import BaseModel, MetaData
from geolib.soils import Soil

from .drains import VerticalDrain
from .dsettlement_parserprovider import DSettlementParserProvider
from .internal import DSettlementStructure, DSeriePoint, Verticals, ResidualTimes
from .loads import OtherLoad
from .serializer import DSettlementInputSerializer

DataClass.Config.validate_assignment = True


class CalculationModel(DataClass):
    pass


class ConsolidationModel(DataClass):
    pass


class DSettlementModel(BaseModel):
    """
    D-Settlement is a dedicated tool for predicting soil settlements
    by external loading.

    This model can read, modify and create
    *.sli files, read *.sld and *.err files.
    """

    @property
    def parser_provider_type(self) -> Type[DSettlementParserProvider]:
        return DSettlementParserProvider

    def serialize(self, filename: str):
        serializer = DSettlementInputSerializer(ds=self.datastructure.dict())
        serializer.write(filename)

    # 1.2.3 Models
    def set_model(
        self,
        constitutive_model: CalculationModel,
        consolidation_model: ConsolidationModel,
        vertical_drain: Optional[VerticalDrain],
        two_dimensional=True,
        water_unit_weight=9.81,
    ):
        pass

    # 1.2.1 Soil profile
    # To create multiple layers
    def add_point(self, point: Point):
        """Add point to model."""

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_head_line(self, label, points: List[int], is_phreatic=False) -> int:
        pass

    def add_layer(
        self,
        points: List[int],
        material: Soil,
        head_line_top: int,
        head_line_bottom: int,
    ):
        """Create layer based on point ids. These should ordered in the x direction.

        .. todo::
            Determine how a 1D geometry would fit in here.
        """

    def set_limits(self, x_min: float, x_max: float):
        """Set limits of geometry. 

        .. todo::
            Determine how to handle points/layers outside of limits.
        """

    # To create verticals
    def add_vertical(self, point: Point):
        """At least one vertical is required to calculate."""

    # 1.2.2 Loads
    def add_uniform_load(
        self,
        name: str,
        time: int,
        unit_weight: float,
        height: float,
        y_application: float,
    ):
        """Create a uniform load with the given name and properties.
        """

    def add_non_uniform_load(
        self,
        name: str,
        points: List[Point],
        time_start: int,
        time_end: Optional[int],
        gamma_dry: float,
        gamma_wet: float,
        sequence_id: Optional[int],
    ):
        """Create non uniform load.

        Sequence of loading is based on order of creation, but can 
        be overridden with sequence_id.
        """

    def add_other_load(self, point: Point, load: OtherLoad, time: int):
        """Create other load."""

    def add_water_load(self, time: timedelta, phreatic_line_id: int):
        """Create water load for a time in days, based on a phreatic line.

        Edit the head lines for each layer with `create layer`.
        """

    def set_calculation_times(self, time_steps: List[timedelta]):
        """(Re)set calculation time(s).

        Sets a list of calculation times, sorted from low to high with a minimum of 0.

        Args:
            time_steps: List of time steps, type: float >= 0

        Returns:

        """
        time_steps.sort()
        residual_times = ResidualTimes(
            time_steps=[timestep.days for timestep in time_steps]
        )
        self.datastructure.residual_times = residual_times

    def set_verticals(self, locations: List[Point]) -> None:
        """
            Set calculation verticals in geometry.
            X and Y coordinates should be defined for each vertical.

            .. todo::
                Add check that checks that the verticals are not outside of the geometry boundaries. [GEOLIB-12]
        """
        pointlist = []
        for point in locations:
            pointlist.append(DSeriePoint.from_point(point))
        verticals = Verticals(locations=pointlist)
        self.datastructure.verticals = verticals
