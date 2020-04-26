import logging
from datetime import timedelta
from operator import attrgetter
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import List, Optional, Type, Union

from pydantic import BaseModel as DataClass
from pydantic import FilePath
from pydantic.types import confloat, constr

from geolib.geometry import Point
from geolib.models import BaseModel, MetaData
from geolib.soils import Soil

from .drains import VerticalDrain
from .dsettlement_parserprovider import DSettlementParserProvider
from .internal import (
    Boundary,
    Curve,
    DSeriePoint,
    Layer,
    Layers,
    NonUniformLoad,
    NonUniformLoads,
    OtherLoads,
    PointForLoad,
    Points,
    ResidualTimes,
    Verticals,
)
from .loads import (
    CircularLoad,
    OtherLoad,
    RectangularLoad,
    TankLoad,
    TrapeziformLoad,
    UniformLoad,
)
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

    @property
    def console_path(self) -> Path:
        return Path("DSettlementConsole/DSettlementConsole.exe")

    def execute(self, timeout: int = 30) -> Union[CompletedProcess, Exception]:
        """Execute a Model and wait for `timeout` seconds."""
        self.serialize(self.input_fn)
        return run(
            [str(self.meta.console_folder / self.console_path), "/b", str(self.input_fn)],
            timeout=timeout,
        )

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

    @property
    def accuracy(self):
        return self.datastructure.geometry_data.accuracy

    @property
    def curves(self):
        return self.datastructure.geometry_data.curves

    @property
    def boundaries(self):
        return self.datastructure.geometry_data.boundaries

    # 1.2.1 Soil profile
    # To create multiple layers
    def add_boundary(self, points: List[DSeriePoint], twod=True) -> int:
        """Add boundary to model."""
        # Divide points into curves and boundary
        # Check point uniqueness
        tolerance = self.accuracy.accuracy
        points = [
            self.points.add_point_if_unique(point, tolerance=tolerance)
            for point in points
        ]
        sorted_points = sorted(points, key=lambda point: (point.X, point.Y, point.Z))
        curves = self.curves.create_curves(sorted_points)
        boundary = self.boundaries.create_boundary(curves)
        return boundary.id

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""
        return self.datastructure.geometry_data.points

    def add_head_line(self, label, points: List[int], is_phreatic=False) -> int:
        pass

    @property
    def layers(self):
        return self.datastructure.geometry_data.layers

    def add_layer(
        self,
        boundary_top: int,
        boundary_bottom: int,
        material: Soil,
        head_line_top: int,
        head_line_bottom: int,
        overwrite: bool = False,  # TODO overwrite if layer already exists
    ) -> int:
        """Create layer based on boundary ids.

        .. todo::
            Determine how a 1D geometry would fit in here.
        """

        # Required until we can parse
        if isinstance(self.layers, str):
            logging.warning("Replacing unparsed Layers!")
            self.layers = Layers()

        # Can be used after Soils are implemented
        # soilname = self.soils.add_soil(material)
        layer = Layer(
            material=material.name,
            piezo_top=head_line_top,
            piezo_bottom=head_line_bottom,
            boundary_top=boundary_top,
            boundary_bottom=boundary_bottom,
        )
        layer = self.layers.add_layer(layer)
        return layer.id

    # TODO check whether this needs to be done
    # def set_limits(self, x_min: float, x_max: float):
    #     """Set limits of geometry.

    #     .. todo::
    #         Determine how to handle points/layers outside of limits.
    #     """

    # 1.2.2 Loads
    @property
    def other_loads(self):
        """Enables easy access to the other loads in the internal dict-like datastructure."""
        return self.datastructure.other_loads

    def add_other_load(
        self,
        name: constr(min_length=1, max_length=25),
        time: timedelta,
        point: Point,
        other_load: Union[
            TrapeziformLoad, RectangularLoad, CircularLoad, TankLoad, UniformLoad
        ],
    ) -> None:
        internal_other_load = other_load._to_internal(name, time, point)
        if isinstance(self.other_loads, str):
            logging.warning("Replacing unparsed OtherLoads!")
            self.datastructure.other_loads = OtherLoads()
        self.other_loads.add_load(name, internal_other_load)

    @property
    def non_uniform_loads(self):
        """Enables easy access to the non-uniform loads in the internal dict-like datastructure."""
        return self.datastructure.non__uniform_loads

    def add_non_uniform_load(
        self,
        name: constr(min_length=1, max_length=25),
        points: List[Point],
        time_start: timedelta,
        gamma_dry: float,
        gamma_wet: float,
        time_end: Optional[timedelta] = None,
    ):
        """Create non uniform load.

        Sequence of loading is based on time_start.
        """
        # If end time is determined in D-Settlement then temporary value is True
        if time_end is None:
            time_end = timedelta(days=0)
            temporary = False
        else:
            temporary = True

        # List of points should be converted for the internal part of the code
        points_for_load = [PointForLoad.from_point(point) for point in points]

        non_uniform_load = NonUniformLoad(
            time=time_start.days,
            endtime=time_end.days,
            gammadry=gamma_dry,
            gammawet=gamma_wet,
            temporary=temporary,
            points=points_for_load,
        )

        if isinstance(self.non_uniform_loads, str):
            logging.warning("Replacing unparsed NonUniformLoads!")
            self.datastructure.non__uniform_loads = NonUniformLoads()
        self.non_uniform_loads.add_load(name, non_uniform_load)

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
