import abc
from enum import Enum
from pathlib import Path
from typing import BinaryIO

import matplotlib.pyplot as plt
from pydantic import DirectoryPath, FilePath
from shapely.geometry import LineString, Polygon
from shapely.ops import polygonize
from shapely.validation import make_valid

from geolib.geometry import Point
from geolib.models import BaseModel
from geolib.soils import Soil

from .analysis import DStabilityAnalysisMethod
from .dstability_parserprovider import DStabilityParserProvider
from .internal import (
    AnalysisType,
    BishopSlipCircleResult,
    CalculationSettings,
    DStabilityResult,
    DStabilityStructure,
    PersistableExcavation,
    PersistableLayer,
    PersistablePoint,
    PersistableSoil,
    PersistableStateCorrelation,
    Scenario,
    SoilCollection,
    SoilCorrelation,
    SoilLayerCollection,
    SoilVisualisation,
    SpencerSlipPlaneResult,
    UpliftVanSlipCircleResult,
    Waternet,
)
from .loads import Consolidation, DStabilityLoad
from .reinforcements import DStabilityReinforcement
from .serializer import DStabilityInputSerializer, DStabilityInputZipSerializer
from .states import DStabilityStateLinePoint, DStabilityStatePoint


class DStabilityCalculationType(Enum):
    """Set Type of Calculation."""

    BoundarySearch = 1
    SingleCalc = 2


class DStabilityCalculationModel(Enum):
    """Set Type of Calculation."""

    Bishop = 1
    UpliftVan = 2
    Spencer = 3


class DStabilityObject(BaseModel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_dstability_sub_structure(self):
        raise NotImplementedError


class DStabilityModel(BaseModel):
    """D-Stability is software for soft soil slope stability.

    This model can read, modify and create
    .stix files
    """

    current_scenario: int = -1
    current_stage: int = -1
    current_calculation: int = -1
    datastructure: DStabilityStructure = DStabilityStructure()
    current_id: int = -1

    def __init__(self, *args, **data) -> None:
        super().__init__(*args, **data)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def parser_provider_type(self) -> type[DStabilityParserProvider]:
        return DStabilityParserProvider

    @property
    def default_console_path(self) -> Path:
        return Path("DStabilityConsole/D-Stability Console.exe")

    @property
    def custom_console_path(self) -> Path:
        return self.get_meta_property("dstability_console_path")

    @property
    def soils(self) -> SoilCollection:
        """Enables easy access to the soil in the internal dict-like datastructure. Also enables edit/delete for individual soils."""
        return self.datastructure.soils

    @property
    def soil_correlations(self) -> SoilCorrelation:
        return self.datastructure.soilcorrelation

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def waternets(self) -> list[Waternet]:
        return self.datastructure.waternets

    @property
    def output(self) -> list[DStabilityResult]:
        def _get_result_or_none(scenario_index, calculation_index) -> DStabilityResult:
            if self.has_result(
                scenario_index=int(scenario_index),
                calculation_index=int(calculation_index),
            ):
                return self.get_result(
                    scenario_index=int(scenario_index),
                    calculation_index=int(calculation_index),
                )
            else:
                return None

        all_results = []

        for scenario_index, scenario in enumerate(self.datastructure.scenarios):
            for calculation_index, _ in enumerate(scenario.Calculations):
                all_results.append(
                    _get_result_or_none(
                        scenario_index=scenario_index, calculation_index=calculation_index
                    )
                )

        return all_results

    def has_result(
        self,
        scenario_index: int | None = None,
        calculation_index: int | None = None,
    ) -> bool:
        """
        Returns whether a calculation has a result.

        Args:
            scenario_index (int | None): Index of a scenario, if None the current scenario is used.
            calculation_index (int | None): Index of a calculation, if None the current calculation is used.

        Returns:
            bool: Value indicating whether the calculation has a result.
        """
        if calculation_index is None:
            calculation_index = self.current_calculation
        if scenario_index is None:
            scenario_index = self.current_scenario

        return self.datastructure.has_result(scenario_index, calculation_index)

    def get_result(
        self,
        scenario_index: int | None = None,
        calculation_index: int | None = None,
    ) -> DStabilityResult:
        """
        Returns the results of a calculation. Calculation results are based on analysis type and calculation type.

        Args:
            scenario_index (int | None): Index of a scenario, if None is supplied the result of the current scenario is returned.
            calculation_index (int | None): Index of a calculation, if None is supplied the result of the current calculation is returned.

        Returns:
            DStabilityResult: The analysis results of the stage.

        Raises:
            ValueError: No results or calculationsettings available
        """
        if calculation_index is None:
            calculation_index = self.current_calculation
        if scenario_index is None:
            scenario_index = self.current_scenario

        result = self._get_result_substructure(scenario_index, calculation_index)
        return result

    def _get_result_substructure(
        self, scenario_index: int | None, calculation_index: int | None
    ) -> DStabilityResult:
        scenario_index = self.get_scenario_index(scenario_index)
        calculation_index = self.get_calculation_index(calculation_index)

        if self.datastructure.has_result(scenario_index, calculation_index):
            result_id = (
                self.datastructure.scenarios[scenario_index]
                .Calculations[calculation_index]
                .ResultId
            )
            calculation_settings = self._get_calculation_settings(
                scenario_index, calculation_index
            )
            analysis_type = calculation_settings.AnalysisType
            calculation_type = calculation_settings.CalculationType

            results = self.datastructure.get_result_substructure(
                analysis_type, calculation_type
            )

            for result in results:
                if result.Id == result_id:
                    return result

        raise ValueError(f"No result found for result id {calculation_index}")

    def _get_calculation_settings(
        self, scenario_index: int, calculation_index: int
    ) -> CalculationSettings:
        calculation_settings_id = (
            self.datastructure.scenarios[scenario_index]
            .Calculations[calculation_index]
            .CalculationSettingsId
        )

        for calculation_settings in self.datastructure.calculationsettings:
            if calculation_settings.Id == calculation_settings_id:
                return calculation_settings

        raise ValueError(
            f"No calculation settings found for calculation {calculation_index} in scenario {scenario_index}."
        )

    def get_slipcircle_result(
        self,
        scenario_index: int | None = None,
        calculation_index: int | None = None,
    ) -> BishopSlipCircleResult | UpliftVanSlipCircleResult:
        """
        Get the slipcircle(s) of the calculation result of a given stage.

        Args:
            scenario_index (int | None): scenario for which to get the available results
            calculation_index (int | None): calculation for which to get the available results

        Returns:
            BishopSlipCircleResult | UpliftVanSlipCircleResult: the slipcircle for the given calculation

        Raises:
            ValueError: Result is not available for provided scenario and calculation index
            AttributeError: When the result has no slipcircle. Try get the slipplane
        """
        result = self._get_result_substructure(scenario_index, calculation_index)
        return result.get_slipcircle_output()

    def get_slipplane_result(
        self,
        scenario_index: int | None = None,
        calculation_index: int | None = None,
    ) -> SpencerSlipPlaneResult:
        """
        Get the slipplanes of the calculations result of a calculation.

        Args:
            scenario_index (int | None): scenario for which to get the available results
            calculation_index (int | None): calculation for which to get the available results

        Returns:
            SpencerSlipPlaneResult: the slip plane for the given calculation

        Raises:
            ValueError: Result is not available for provided scenario and calculation index
            AttributeError: When the result has no slipplane. Try get the slipcircle
        """
        result = self._get_result_substructure(scenario_index, calculation_index)
        return result.get_slipplane_output()

    def _get_geometry(self, scenario_index: int, stage_index: int):
        geometry_id = (
            self.datastructure.scenarios[scenario_index].Stages[stage_index].GeometryId
        )

        for geometry in self.datastructure.geometries:
            if geometry.Id == geometry_id:
                return geometry

        raise ValueError(
            f"No geometry found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_soil_layers(self, scenario_index: int, stage_index: int):
        return self.datastructure._get_soil_layers(scenario_index, stage_index)

    def _get_waternet(self, scenario_index: int, stage_index: int):
        waternet_id = (
            self.datastructure.scenarios[scenario_index].Stages[stage_index].WaternetId
        )

        for waternet in self.datastructure.waternets:
            if waternet.Id == waternet_id:
                return waternet

        raise ValueError(
            f"No waternet found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_state(self, scenario_index: int, stage_index: int):
        state_id = (
            self.datastructure.scenarios[scenario_index].Stages[stage_index].StateId
        )

        for state in self.datastructure.states:
            if state.Id == state_id:
                return state

        raise ValueError(
            f"No state found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_state_correlations(self, scenario_index: int, stage_index: int):
        state_correlations_id = (
            self.datastructure.scenarios[scenario_index]
            .Stages[stage_index]
            .StateCorrelationsId
        )

        for state_correlations in self.datastructure.statecorrelations:
            if state_correlations.Id == state_correlations_id:
                return state_correlations

        raise ValueError(
            f"No state correlations found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_excavations(self, scenario_index: int, stage_index: int):
        return self.datastructure._get_excavations(scenario_index, stage_index)

    def _get_loads(self, scenario_index: int, stage_index: int):
        return self.datastructure._get_loads(scenario_index, stage_index)

    def _get_reinforcements(self, scenario_index: int, stage_index: int):
        reinforcements_id = (
            self.datastructure.scenarios[scenario_index]
            .Stages[stage_index]
            .ReinforcementsId
        )

        for reinforcements in self.datastructure.reinforcements:
            if reinforcements.Id == reinforcements_id:
                return reinforcements

        raise ValueError(
            f"No reinforcements found for stage {stage_index} in scenario {scenario_index}."
        )

    def serialize(self, location: FilePath | DirectoryPath | BinaryIO):
        """Support serializing to directory while developing for debugging purposes."""
        if isinstance(location, Path) and location.is_dir():
            serializer = DStabilityInputSerializer(ds=self.datastructure)
        else:
            serializer = DStabilityInputZipSerializer(ds=self.datastructure)
        serializer.write(location)
        if isinstance(location, Path):
            self.filename = location

    def add_scenario(
        self, label: str = "Scenario", notes: str = "", set_current: bool = True
    ) -> int:
        """Add a new scenario to the model.

        Args:
            label (str): Label for the scenario.
            notes (str): Notes for the scenario.
            set_current (bool): Whether to make the new scenario the current scenario.

        Returns:
            the id of the new stage
        """
        new_id = self._get_next_id()
        new_scenario_id, new_unique_id = self.datastructure.add_default_scenario(
            label, notes, new_id
        )

        if set_current:
            self.current_scenario = new_scenario_id
            self.current_stage = 0
            self.current_calculation = 0

        self.current_id = new_unique_id
        return new_scenario_id

    def add_stage(
        self,
        scenario_index: int | None = None,
        label: str = "Stage",
        notes: str = "",
        set_current=True,
    ) -> int:
        """Add a new stage to the model at the given scenario index.

        Args:
            scenario_index (int | None): The scenario index to add the stage to, defaults to the current scenario.
            label (str): Label for the stage.
            notes (str): Notes for the stage.
            set_current (bool): Whether to make the new stage the current stage.

        Returns:
            the id of the new stage
        """
        scenario_index = self.get_scenario_index(scenario_index)

        new_id = self._get_next_id()
        new_stage_index, new_unique_id = self.datastructure.add_default_stage(
            scenario_index, label, notes, new_id
        )

        if set_current:
            self.current_stage = new_stage_index
        self.current_id = new_unique_id
        return new_stage_index

    def add_calculation(
        self,
        scenario_index: int | None = None,
        label: str = "Calculation",
        notes: str = "",
        set_current: bool = True,
    ) -> int:
        """Add a new calculation to the model.

        Args:
            scenario_index (int | None): The scenario index to add the calculation to, defaults to the current scenario.
            label (str): Label for the calculation.
            notes (str): Notes for the calculation.
            set_current (bool): Whether to make the new calculation the current calculation.

        Returns:
            the id of the new stage
        """
        scenario_index = self.get_scenario_index(scenario_index)

        new_id = self._get_next_id()
        new_calculation_index, new_unique_id = self.datastructure.add_default_calculation(
            scenario_index, label, notes, new_id
        )

        if set_current:
            self.current_calculation = new_calculation_index
        self.current_id = new_unique_id
        return new_calculation_index

    @property
    def scenarios(self) -> list[Scenario]:
        return self.datastructure.scenarios

    def add_soil(self, soil: Soil) -> int:
        """
        Add a new soil to the model. The code must be unique, the id will be generated

        Args:
            soil (Soil): a new soil

        Returns:
            int: id of the added soil
        """
        if soil.code == None:
            raise ValueError("Soil.code may not be None")
        if self.soils.has_soil_code(soil.code):
            raise ValueError(f"The soil with code {soil.code} is already defined.")

        soil.id = str(self._get_next_id())
        dstability_soil = self.soils.add_soil(soil)
        return int(dstability_soil.Id)

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_layer(
        self,
        points: list[Point],
        soil_code: str,
        label: str = "",
        notes: str = "",
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> int:
        """
        Add a soil layer to the model

        Args:
            points (list[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            soil_code (str): code of the soil for this layer
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_index (int | None): scenario to add to, defaults to the current scenario
            stage_index (int | None): stage to add to, defaults to the current stage

        Returns:
            int: id of the added layer
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        geometry = self._get_geometry(scenario_index, stage_index)
        soil_layers = self._get_soil_layers(scenario_index, stage_index)

        # Check if we have the soil code
        if not self.soils.has_soil_code(soil_code):
            raise ValueError(
                f"The soil with code {soil_code} is not defined in the soil collection."
            )

        # Make sure the points are valid
        persistable_points = self.make_points_valid(points)

        # Create the new layer
        new_layer = PersistableLayer(
            Id=str(self._get_next_id()),
            Label=label,
            Points=persistable_points,
            Notes=notes,
        )

        # Add the layer to the geometry
        self.add_layer_and_connect_points(geometry.Layers, new_layer)

        # Add the connection between the layer and the soil to soillayers
        soil = self.soils.get_soil(soil_code)
        soil_layers.add_soillayer(layer_id=new_layer.Id, soil_id=soil.Id)
        return int(new_layer.Id)

    def make_points_valid(self, points: list[Point]) -> list[PersistablePoint]:
        valid_points = make_valid(self.geolib_points_to_shapely_polygon(points))
        return self.to_dstability_points(valid_points)

    def connect_layers(self, layer1: PersistableLayer, layer2: PersistableLayer):
        """Connects two polygons by adding a the missing points on the polygon edges. Returns the two new polygons."""
        linestring1 = self.to_shapely_linestring(layer1.Points)
        linestring2 = self.to_shapely_linestring(layer2.Points)

        # Create a union of the two polygons and polygonize it creating two connected polygons
        union = linestring1.union(linestring2)
        result = [geom for geom in polygonize(union)]

        # If the result has two polygons, we return them, otherwise we return the original polygons
        if len(result) == 2:
            return result[0].exterior, result[1].exterior
        else:
            return linestring1, linestring2

    def add_layer_and_connect_points(
        self, current_layers: list[PersistableLayer], new_layer: PersistableLayer
    ):
        """Adds a new layer to the list of layers and connects the points of the new layer to the existing layers."""

        current_layers.append(new_layer)

        # Check if the new layer intersects with any of the existing layers
        for layer in current_layers:
            if layer != new_layer and self.dstability_points_to_shapely_polygon(
                layer.Points
            ).exterior.intersects(
                self.dstability_points_to_shapely_polygon(new_layer.Points).exterior
            ):
                # If it does, connect the layers
                linestring1, linestring2 = self.connect_layers(layer, new_layer)

                # Update the points of the layers
                current_layers[current_layers.index(layer)].Points = (
                    self.to_dstability_points(linestring1)
                )
                current_layers[current_layers.index(new_layer)].Points = (
                    self.to_dstability_points(linestring2)
                )

    def to_shapely_linestring(self, points: list[PersistablePoint]) -> LineString:
        converted_points = [(p.X, p.Z) for p in points]
        converted_points.append(converted_points[0])
        return LineString(converted_points)

    def dstability_points_to_shapely_polygon(
        self, points: list[PersistablePoint]
    ) -> Polygon:
        return Polygon([(p.X, p.Z) for p in points])

    def geolib_points_to_shapely_polygon(self, points: list[Point]) -> Polygon:
        return Polygon([(p.x, p.z) for p in points])

    def to_dstability_points(
        self, shapely_object: LineString | Polygon
    ) -> list[PersistablePoint]:
        if isinstance(shapely_object, LineString):
            coords = shapely_object.coords
        elif isinstance(shapely_object, Polygon):
            coords = shapely_object.exterior.coords
        else:
            raise ValueError(
                "shapely_object must be a LineString or Polygon, not {}".format(
                    type(shapely_object)
                )
            )

        persistable_points = [PersistablePoint(X=p[0], Z=p[1]) for p in list(coords)]

        # Remove duplicate points
        persistable_points = [
            i
            for n, i in enumerate(persistable_points)
            if i not in persistable_points[n + 1 :]
        ]

        # Remove last point if it is the same as the first
        if persistable_points[0] == persistable_points[-1]:
            persistable_points.pop(-1)

        return persistable_points

    def get_soil(self, code: str) -> PersistableSoil:
        """
        Gets an existing soil with the given soil code.

        Args:
            code (str): the code of the soil

        Returns:
            PersistableSoil: the soil
        """
        return self.soils.get_soil(code=code)

    def get_soil_by_name(self, name: str) -> PersistableSoil:
        """
        Gets an existing soil with the given soil name.

        Args:
            name (str): the name of the soil

        Returns:
            PersistableSoil: the soil
        """
        return self.soils.get_soil_by_name(name=name)

    def add_head_line(
        self,
        points: list[Point],
        label: str = "",
        notes: str = "",
        is_phreatic_line: bool = False,
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> int:
        """
        Add head line to the model

        Args:
            points (list[Point]): list of Point classes
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            is_phreatic_line (bool): set as phreatic line, defaults to False
            scenario_index (int | None): scenario to add to, defaults to the current scenario
            stage_index (int | None): stage to add to, defaults to the current stage

        Returns:
            bool: id of the added headline
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        waternet = self._get_waternet(scenario_index, stage_index)

        persistable_headline = waternet.add_head_line(
            str(self._get_next_id()), label, notes, points, is_phreatic_line
        )
        return persistable_headline.Id

    def add_reference_line(
        self,
        points: list[Point],
        bottom_headline_id: str | None = None,
        top_head_line_id: str | None = None,
        label: str = "",
        notes: str = "",
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> int:
        """
        Add reference line to the model

        Args:
            points (list[Point]): list of Point classes
            bottom_headline_id (int): id of the headline to use as the bottom headline
            top_head_line_id (int): id of the headline to use as the top headline
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_index (int | None): scenario to add to, defaults to the current scenario
            stage_index (int | None): stage to add to, defaults to the current stage

        Returns:
            int: id of the added reference line
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        waternet = self._get_waternet(scenario_index, stage_index)

        persistable_reference_line = waternet.add_reference_line(
            str(self._get_next_id()),
            label,
            notes,
            points,
            bottom_headline_id,
            top_head_line_id,
        )
        return int(persistable_reference_line.Id)

    def add_state_point(
        self,
        state_point: DStabilityStatePoint,
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> int:
        """
        Add state point to the model

        Args:
            state_point (DStabilityStatePoint): DStabilityStatePoint class
            scenario_index (int | None): scenario to add to, defaults to the current scenario
            stage_index (int | None): stage to add to, defaults to the current stage

        Returns:
            int: id of the added add_state_point
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        states = self._get_state(scenario_index, stage_index)

        try:
            _ = self._get_geometry(scenario_index, stage_index).get_layer(
                state_point.layer_id
            )
        except ValueError:
            raise ValueError(f"No layer with id '{state_point.layer_id} in this geometry")

        state_point.id = (
            self._get_next_id()
        )  # the user does not know the id so we have to add it
        persistable_state_point = state_point._to_internal_datastructure()
        states.add_state_point(persistable_state_point)
        return int(persistable_state_point.Id)

    def add_state_line(
        self,
        points: list[Point],
        state_points: list[DStabilityStateLinePoint],
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> int:
        """
        Add state line. From the Soils, only the state parameters are used.

        points are a list of points with x,z coordinates
        state_point are a list of DStabilityStateLinePoint where ONLY the x is used, the Z will be calculated

        Args:
            points (list[Point]): The geometry points of the state line.
            state_point (list[DStabilityStatePoint]): The list of state point values.
            scenario_index (int | None): scenario to add to, defaults to the current scenario.
            stage_index (int | None): stage to add to, defaults to the current stage.

        Returns:
            PersistableStateLine: The created state line
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        states = self._get_state(scenario_index, stage_index)

        # each point should belong to a layer
        persistable_points = []

        for point in points:
            point.id = self._get_next_id()  # assign a new id
            persistable_points.append(PersistablePoint(X=point.x, Z=point.z))

        persistable_state_line_points = []
        for state_point in state_points:
            state_point.id = self._get_next_id()  # assign a new id
            persistable_state_line_points.append(state_point._to_internal_datastructure())

        return states.add_state_line(persistable_points, persistable_state_line_points)

    def add_state_correlation(
        self,
        correlated_state_ids: list[int],
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ):
        """
        Add state correlation between the given state point ids.

        Args:
            correlated_state_ids (list[int]): The state point ids to correlate.
            scenario_index (int | None): scenario to add to, defaults to the current scenario.
            stage_index (int | None): stage to add to, defaults to the current stage.

        Returns:
            None
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        state_correlations = self._get_state_correlations(scenario_index, stage_index)

        for state_id in correlated_state_ids:
            try:
                _ = self._get_state(scenario_index, stage_index).get_state(state_id)
            except ValueError:
                raise ValueError(f"No state point with id '{state_id} in this geometry")

        persistable_state_correlation = PersistableStateCorrelation(
            CorrelatedStateIds=correlated_state_ids, IsFullyCorrelated=True
        )

        state_correlations.add_state_correlation(persistable_state_correlation)

    def add_excavation(
        self,
        points: list[Point],
        label: str,
        notes: str = "",
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ):
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        persistable_excavation = PersistableExcavation(
            Label=label,
            Notes=notes,
            Points=[PersistablePoint(X=p.x, Z=p.z) for p in points],
        )
        self._get_excavations(scenario_index, stage_index).append(persistable_excavation)

    def add_load(
        self,
        load: DStabilityLoad,
        consolidations: list[Consolidation] | None = None,
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> None:
        """Add a load to the object.

        The geometry should be defined before adding loads.

        If no consolidations are provided, a Consolidation with default values will be made for each SoilLayer.
        It is not possible to set consolidation degrees of loads afterwards since they don't have an id.

        Args:
            load: A subclass of DStabilityLoad.
            scenario_index (int | None): scenario to add to, defaults to the current scenario.
            stage_index (int | None): stage to add to, defaults to the current stage.

        Raises:
            ValueError: When the provided load is no subclass of DStabilityLoad, an invalid stage_index is provided, or the datastructure is no longer valid.
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        if not issubclass(type(load), DStabilityLoad):
            raise ValueError(
                f"load should be a subclass of DstabilityReinforcement, received {load}"
            )
        if self.datastructure.has_soil_layers(
            scenario_index, stage_index
        ) and self.datastructure.has_loads(scenario_index, stage_index):
            if consolidations is None:
                consolidations = self._get_default_consolidations(
                    scenario_index, stage_index
                )
            else:
                self._verify_consolidations(consolidations, scenario_index, stage_index)
            self._get_loads(scenario_index, stage_index).add_load(load, consolidations)
        else:
            raise ValueError(
                f"No loads found for scenario {scenario_index} stage {stage_index}"
            )

    def add_soil_layer_consolidations(
        self,
        soil_layer_id: int,
        consolidations: list[Consolidation] | None = None,
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> None:
        """Add consolidations for a layer (layerload).

        Consolidations cannot be added when adding soil layers since in the consolidations, all other soil layers need to be referred.
        Therefore, all soillayers in a stage should be defined before setting consolidation and
        the number of consolidations given should equal the amount of layers.

        Args:
            soil_layer_id: Consolidation is set for this soil layer id.
            consolidations: List of Consolidation. Must contain a Consolidation for every other layer.
            scenario_index (int | None): scenario to add to, defaults to the current scenario.
            stage_index (int | None): stage to add to, defaults to the current stage.

        Raises:
            ValueError: When the provided load is no subclass of DStabilityLoad, an invalid stage_index is provided, or the datastructure is no longer valid.
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        if self.datastructure.has_soil_layer(
            scenario_index, stage_index, soil_layer_id
        ) and self.datastructure.has_loads(scenario_index, stage_index):
            if consolidations is None:
                consolidations = self._get_default_consolidations(
                    scenario_index, stage_index, soil_layer_id
                )
            else:
                self._verify_consolidations(
                    consolidations, scenario_index, stage_index, soil_layer_id
                )

            self._get_loads(scenario_index, stage_index).add_layer_load(
                soil_layer_id, consolidations
            )
        else:
            raise ValueError(
                f"No soil layer loads found for scenario {scenario_index} stage {stage_index}"
            )

    def _get_default_consolidations(
        self,
        scenario_index: int,
        stage_index: int,
        exclude_soil_layer_id: int | None = None,
    ) -> list[Consolidation]:
        """Length of the consolidations is equal to the amount of soil layers.

        If exclude_soil_layer_id is provided, that specific soil layer id is not included in the consolidations.
        """
        if self.datastructure.has_soil_layers(scenario_index, stage_index):
            soil_layer_ids = self._get_soil_layers(scenario_index, stage_index).get_ids(
                exclude_soil_layer_id
            )
            return [Consolidation(layer_id=layer_id) for layer_id in soil_layer_ids]

        raise ValueError(f"No soil layers found for stage at index {stage_index}")

    def _verify_consolidations(
        self,
        consolidations: list[Consolidation],
        scenario_index: int,
        stage_index: int,
        exclude_soil_layer_id: int | None = None,
    ) -> None:
        if self.datastructure.has_soil_layers(scenario_index, stage_index):
            consolidation_soil_layer_ids: set[str] = {
                str(c.layer_id) for c in consolidations
            }
            soil_layer_ids = self._get_soil_layers(scenario_index, stage_index).get_ids(
                exclude_soil_layer_id
            )

            if consolidation_soil_layer_ids != soil_layer_ids:
                raise ValueError(
                    f"Received consolidations ({consolidation_soil_layer_ids}) should contain all soil layer ids ({soil_layer_ids})"
                )
        else:
            raise ValueError(f"No soil layers found for stage at index {stage_index}")

    def add_reinforcement(
        self,
        reinforcement: DStabilityReinforcement,
        scenario_index: int | None = None,
        stage_index: int | None = None,
    ) -> None:
        """Add a reinforcement to the model.

        Args:
            reinforcement: A subclass of DStabilityReinforcement.
            scenario_index (int | None): scenario to add to, defaults to the current scenario.
            stage_index (int | None): stage to add to, defaults to the current stage.

        Returns:
            int: Assigned id of the reinforcements (collection object of all reinforcements for a stage).

        Raises:
            ValueError: When the provided reinforcement is no subclass of DStabilityReinforcement, an invalid stage_index is provided, or the datastructure is no longer valid.
        """
        scenario_index = self.get_scenario_index(scenario_index)
        stage_index = self.get_stage_index(stage_index)

        if not issubclass(type(reinforcement), DStabilityReinforcement):
            raise ValueError(
                f"reinforcement should be a subclass of DstabilityReinforcement, received {reinforcement}"
            )

        if self.datastructure.has_reinforcements(scenario_index, stage_index):
            self._get_reinforcements(scenario_index, stage_index).add_reinforcement(
                reinforcement
            )
        else:
            raise ValueError(
                f"No reinforcements found for scenario {scenario_index} stage {stage_index}"
            )

    def add_soil_correlation(self, list_correlated_soil_ids: list[str]):
        """Add a soil correlation to the model.

        Args:
            list_correlated_soil_ids: A list of soil ids that are correlated.
        """
        self.soil_correlations.add_soil_correlation(list_correlated_soil_ids)

    def set_model(
        self,
        analysis_method: DStabilityAnalysisMethod,
        scenario_index: int | None = None,
        calculation_index: int | None = None,
    ) -> None:
        """Sets the model and applies the given parameters

        Args:
            analysis_method (DStabilityAnalysisMethod): A subclass of DStabilityAnalysisMethod.
            scenario_index (int | None): scenario to add to, defaults to the current scenario
            calculation_index (int | None): calculation to add to, defaults to the current calculation

        Raises:
            ValueError: When the provided analysis method is no subclass of DStabilityAnalysisMethod,
            an invalid stage_index is provided, the analysis method is not known or the datastructure is no longer valid.
        """
        scenario_index = self.get_scenario_index(scenario_index)
        calculation_index = self.get_calculation_index(calculation_index)

        calculationsettings = self._get_calculation_settings(
            scenario_index, calculation_index
        )

        _analysis_method_mapping = {
            AnalysisType.BISHOP: calculationsettings.set_bishop,
            AnalysisType.BISHOP_BRUTE_FORCE: calculationsettings.set_bishop_brute_force,
            AnalysisType.SPENCER: calculationsettings.set_spencer,
            AnalysisType.SPENCER_GENETIC: calculationsettings.set_spencer_genetic,
            AnalysisType.UPLIFT_VAN: calculationsettings.set_uplift_van,
            AnalysisType.UPLIFT_VAN_PARTICLE_SWARM: calculationsettings.set_uplift_van_particle_swarm,
        }

        try:
            _analysis_method_mapping[analysis_method.analysis_type](
                analysis_method._to_internal_datastructure()
            )
        except KeyError:
            raise ValueError(
                f"Unknown analysis method {analysis_method.analysis_type.value} found"
            )

    def get_scenario_index(self, scenario_index: int | None):
        if scenario_index is None:
            return self.current_scenario
        else:
            return scenario_index

    def get_stage_index(self, stage_index: int | None):
        if stage_index is None:
            return self.current_stage
        else:
            return stage_index

    def get_calculation_index(self, calculation_index: int | None):
        if calculation_index is None:
            return self.current_calculation
        else:
            return calculation_index

    @staticmethod
    def get_soil_id_from_layer_id(
        layers: SoilLayerCollection, layer_id: str
    ) -> str | None:
        for layer in layers.SoilLayers:
            if layer.LayerId == layer_id:
                return layer.SoilId
        return None

    @staticmethod
    def get_color_from_soil_id(
        soil_visualizations: SoilVisualisation, soil_id: str
    ) -> str:
        for soil_visualization in soil_visualizations.SoilVisualizations:
            if soil_visualization.SoilId == soil_id:
                return soil_visualization.Color
        return "#000000"

    def _get_color_of_layer(
        self, layers_collection: SoilLayerCollection, layer: PersistableLayer
    ) -> str:
        layer_id = layer.Id
        # use the layer id to get the soil type id
        soil_type_id = DStabilityModel.get_soil_id_from_layer_id(
            layers_collection, layer_id
        )
        # get the color of the soil type
        color = DStabilityModel.get_color_from_soil_id(
            self.input.soilvisualizations, soil_type_id
        )
        return color.replace("#80", "#")

    def plot(self, scenario_index: int | None = None, stage_index: int | None = None):
        geometry = self._get_geometry(scenario_index, stage_index)
        layers_collection = self._get_soil_layers(scenario_index, stage_index)
        fig, ax = plt.subplots()
        # loop over the layers
        for layer in geometry.Layers:
            # get list of x and y coordinates
            x = [p.X for p in layer.Points]
            y = [p.Z for p in layer.Points]
            # get color of layer
            color = self._get_color_of_layer(layers_collection, layer)
            # create a polygon
            ax.fill(x, y, color=color)
        plt.axis("off")
        return fig, ax
