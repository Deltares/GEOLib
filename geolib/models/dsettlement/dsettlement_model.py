import logging
from datetime import timedelta
from operator import attrgetter
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import List, Optional, Type, Union

from pydantic import BaseModel as DataClass
from pydantic import FilePath
from pydantic.types import confloat, constr, PositiveInt, conint

from geolib.geometry import Point
from geolib.models import BaseModel, MetaData, BaseModelStructure
from geolib.soils import Soil as Soil_Input

from .drains import VerticalDrain
from .dsettlement_parserprovider import DSettlementParserProvider
from .internal import (
    Boundary,
    Curve,
    DSeriePoint,
    DSettlementStructure,
    Layer,
    Layers,
    NonUniformLoad,
    NonUniformLoads,
    OtherLoads,
    PointForLoad,
    Points,
    ResidualTimes,
    Verticals,
    PiezoLines,
    PhreaticLine,
    Dimension,
    StrainType,
    SoilModel,
    ConsolidationModel,
    CalculationOptions,
    Model,
)
from .internal_soil import SoilInternal
from .loads import (
    CircularLoad,
    RectangularLoad,
    TankLoad,
    TrapeziformLoad,
    UniformLoad,
)
from .serializer import DSettlementInputSerializer

DataClass.Config.validate_assignment = True


class DSettlementModel(BaseModel):
    """
    D-Settlement is a dedicated tool for predicting soil settlements
    by external loading.

    This model can read, modify and create
    *.sli files, read *.sld and *.err files.
    """

    datastructure: BaseModelStructure = DSettlementStructure()

    @property
    def parser_provider_type(self) -> Type[DSettlementParserProvider]:
        return DSettlementParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DSettlementConsole/DSettlementConsole.exe")

    def execute(self, timeout: int = 30) -> Union[CompletedProcess, ValueError]:
        """Execute a Model and wait for `timeout` seconds."""
        if self.filename is None:
            raise ValueError("Set filename or serialize first!")
        if not self.filename.exists():
            logging.warning("Serializing before executing.")
            self.serialize(self.filename)
        return run(
            [str(self.meta.console_folder / self.console_path), "/b", str(self.filename)],
            timeout=timeout,
            cwd=self.filename.parent,
        )

    def serialize(self, filename: FilePath):
        serializer = DSettlementInputSerializer(ds=self.datastructure.dict())
        serializer.write(filename)
        self.filename = filename

    def add_soil(self, soil_input: Soil_Input) -> None:
        """ Soil is converted in the internal structure and added in soil_collection."""
        soil_new = SoilInternal.convert_from_external_to_internal(soil_input)
        self.datastructure.soil_collection.add_soil_if_unique(soil_new)

    # 1.2.3 Models
    def set_model(
        self,
        constitutive_model: SoilModel,
        consolidation_model: ConsolidationModel,
        is_two_dimensional: bool,
        strain_type: StrainType,
        is_vertical_drain: bool,
        is_fit_for_settlement_plate: bool,
        is_probabilistic: bool,
        is_horizontal_displacements: bool,
        is_secondary_swelling: bool,
        is_waspan: bool,
    ):
        """
        Sets the D-settlement Model. Initializes CalculationOptions and Model if the type is str
        Args:
            constitutive_model (SoilModel): enum
            consolidation_model (ConsolidationModel): enum
            is_two_dimensional (bool): true if geometry is 2 dimensional
            strain_type (StrainType): enum
            is_vertical_drain (bool): true if vertical drain is present
            is_fit_for_settlement_plate (bool): true if fit for settlement plate
            is_probabilistic (bool): true if probabilistic calculation should be made
            is_horizontal_displacements (bool): true if horizontal displacements should be calculated
            is_secondary_swelling (bool): true if secondary swelling is present
            is_waspan (bool): true if waspan

        Returns:
            Model
        """
        if isinstance(self.datastructure.calculation_options, str):
            logging.warning("Calculation options are overwritten")
            self.datastructure.calculation_options = CalculationOptions()

        if isinstance(self.datastructure.model, str):
            logging.warning("Model options are overwritten")
            self.datastructure.model = Model()

        model_options = self.datastructure.model

        model_options.dimension = (
            Dimension.TWO_D if is_two_dimensional else Dimension.ONE_D
        )
        model_options.consolidation_model = consolidation_model
        model_options.soil_model = constitutive_model
        model_options.strain_type = strain_type
        model_options.is_vertical_drains = is_vertical_drain
        model_options.is_fit_for_settlement_plate = is_fit_for_settlement_plate
        model_options.is_probabilistic = is_probabilistic
        model_options.is_horizontal_displacements = is_horizontal_displacements
        model_options.is_secondary_swelling = is_secondary_swelling
        model_options.is_waspan = is_waspan

        return model_options

    def set_any_calculation_options(self, **kwargs):
        """
        Sets calculation options and initializes or removes data when necessary
        Args:
            **kwargs: Type variable, keyword arguments
        Kwargs:
            precon_pressure_within_layer (PreconPressureWithinLayer): type of preconsolidation pressure within the layer
            is_imaginary_surface (bool): true if imaginary surface
            imaginary_surface_layer (PositivInt): index of layer
            is_submerging (bool): true if submerging
            use_end_time_for_fit (bool): true if end time should be used for fit
            is_maintain_profile (bool): true if profile should be maintained
            maintain_profile_material_name (str): name of the profile
            maintain_profile_time (conint(ge=0, le=100000)): time for maintain profile [days]
            maintain_profile_gamma_dry (confloat(ge=-100, le=100)): unit weight above phreatic line for
                maintain profile [kN/m3]
            maintain_profile_gamma_wet (confloat(ge=-100, le=100)): unit weight below phreatic line for
                maintain profile [kN/m3]
            dispersion_conditions_layer_boundaries_top (DispersionConditionLayerBoundary): dispersion condition at the
                top of the layer
            dispersion_conditions_layer_boundaries_top (DispersionConditionLayerBoundary): dispersion condition at the
                bottom of the layer
            stress_distribution_soil (StressDistributionSoil): type of stress distribution of the soil
            stress_distribution_loads (StressDistributionLoads): type of stress distribution loads
            iteration_stop_criteria_submerging (confloat(ge=0.0, le=1.0)): submerging iteration stop criteria
            iteration_stop_criteria_submerging_layer_height(confloat(ge=0, le=99.999)):  minimum settlement for
                submerging iteration stop criteria [m]
            maximum_iteration_steps_for_submerging (conint(ge=1, le=100)): maximum iteraion steps for submerging
            iteration_stop_criteria_desired_profile (confloat(ge=0, le=1)): iteration stop criteria for desired profile
            load_column_width_imaginary_surface (confloat(ge=0.05, le=10000)): load column width of the imaginary
                surface [m]
            load_column_width_non_uniform_loads (confloat(ge=0.05, le=10000)): load column width of non-uniform loads [m]
            load_column_width_trapeziform_loads (confloat(ge=0.05, le=10000)): load column width of trapeziform loads [m]
            end_of_consolidation (conint(ge=1, le=100000)): end of settlement calculation [days]
            number_of_subtime_steps (conint(ge=1, le=100)): number of subtime steps [-]
            reference_time (confloat(ge=0.001, le=1000000)): reference time [day]
            dissipation (bool): true if dissipation calculation should be added
            x_coord_dissipation (float): x-coordinate of the dissipation vertical [m]
            use_fit_factors (bool): true if fit parameters should be used
            x_coord_fit (float): x-coordinate of the fit [m]
            is_predict_settlements_omitting_additional_load_steps (bool): true if output of settlements by partial
                loading

        Returns:
            calculation options
        """
        if isinstance(self.datastructure.calculation_options, str):
            logging.warning("Calculation options are overwritten")
            self.datastructure.calculation_options = CalculationOptions()

        if isinstance(self.datastructure.model, str):
            logging.warning("Model options are overwritten")
            self.datastructure.model = Model()

        calculation_options = self.datastructure.calculation_options.dict()
        calculation_options.update(**kwargs)
        self.datastructure.calculation_options = CalculationOptions.set_options(
            **calculation_options
        )

        return calculation_options

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
    def add_boundary(self, points: List[Point], twod=True) -> int:
        """Add boundary to model."""
        # Divide points into curves and boundary
        # Check point uniqueness
        tolerance = self.accuracy.accuracy
        points = [
            self.points.add_point_if_unique(
                DSeriePoint.from_point(point), tolerance=tolerance
            )
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

    @property
    def headlines(self):
        return self.datastructure.geometry_data.piezo_lines

    def add_head_line(self, points: List[Point], is_phreatic=False) -> int:
        """Add head line to model."""
        # New points have to be created, whether points at the same location exist or not
        # This means that new points from geometry will re-use head line points,
        # So first create geometry, then add headlines.
        points = [
            self.points.add_point(DSeriePoint.from_point(point)) for point in points
        ]
        sorted_points = sorted(points, key=lambda point: (point.X, point.Y, point.Z))
        curves = self.curves.create_curves(sorted_points)

        piezo_line = self.headlines.create_piezoline(curves)
        if is_phreatic:
            self.datastructure.geometry_data.phreatic_line.phreaticline = piezo_line.id
        return piezo_line.id

    @property
    def layers(self):
        return self.datastructure.geometry_data.layers

    def add_layer(
        self,
        boundary_top: int,
        boundary_bottom: int,
        material_name: str,
        head_line_top: int,
        head_line_bottom: int,
        overwrite: bool = False,  # TODO overwrite if layer already exists
    ) -> int:
        """Create layer based on boundary ids.

        .. todo::
            Determine how a 1D geometry would fit in here.
        """

        # Can be used after Soils are implemented
        # TODO:: add check that the soil name exist
        # TODO:: add soil together with the layer
        # soilname = self.soils.add_soil(material)
        layer = Layer(
            material=material_name,
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
        internal_other_load = other_load._to_internal(time, point)
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
        points = [DSeriePoint.from_point(point) for point in locations]
        verticals = Verticals(locations=points)
        self.datastructure.verticals = verticals
