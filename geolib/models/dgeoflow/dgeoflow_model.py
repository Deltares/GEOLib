import abc
import re
from enum import Enum
from pathlib import Path
from typing import BinaryIO

from pydantic import DirectoryPath, FilePath

from geolib.geometry import Point
from geolib.models import BaseDataClass, BaseModel
from geolib.soils import Soil

from ...utils import camel_to_snake, snake_to_camel
from .dgeoflow_parserprovider import DGeoFlowParserProvider
from .internal import (
    CalculationType,
    CalculationTypeEnum,
    DGeoFlowResult,
    DGeoFlowStructure,
    GroundwaterFlowResult,
    InternalPipeTrajectory,
    PersistableSoil,
    PersistableSoilLayer,
    PipeLengthResult,
    Scenario,
    SoilCollection,
    SoilLayerCollection,
)
from .serializer import DGeoFlowInputSerializer, DGeoFlowInputZipSerializer


class DGeoFlowObject(BaseModel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_DGeoFlow_sub_structure(self):
        raise NotImplementedError


class DGeoFlowModel(BaseModel):
    """D-Geoflow is software for soft soil piping calculations.

    This model can read, modify and create
    .flox files
    """

    current_scenario: int = -1
    current_scenario_index: int = 0
    current_stage_index: int = 0
    current_calculation_index: int = 0
    datastructure: DGeoFlowStructure = DGeoFlowStructure()
    current_id: int = -1

    def __init__(self, *args, **data) -> None:
        super().__init__(*args, **data)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def parser_provider_type(self) -> type[DGeoFlowParserProvider]:
        return DGeoFlowParserProvider

    @property
    def default_console_path(self) -> Path:
        return Path("DGeoFlowConsole/D-GeoFlow Console.exe")

    @property
    def custom_console_path(self) -> Path:
        return self.get_meta_property("dgeoflow_console_path")

    @property
    def console_flags_post(self) -> list[str]:
        return [
            str(self.current_scenario_index + 1),
            str(self.current_calculation_index + 1),
        ]

    @property
    def soils(self) -> SoilCollection:
        """Enables easy access to the soil in the internal dict-like datastructure. Also enables edit/delete for individual soils."""
        return self.datastructure.soils

    def get_layer(self, scenario_id: int, layer_id: int) -> PersistableSoilLayer:
        """Enables easy access to the soil in the internal dict-like datastructure. Also enables edit/delete for individual soils."""
        soillayers = self.datastructure.soillayers[scenario_id]
        for layer in soillayers.SoilLayers:
            if int(layer.LayerId) == layer_id:
                return layer
        raise ValueError(f"No soil layer found with layer id {layer_id}")

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def output(self) -> DGeoFlowResult:
        return self.get_result(
            self.current_scenario_index, self.current_calculation_index
        )

    def get_result(self, scenario_index: int, calculation_index: int) -> dict:
        """
        Returns the results of a scenario. Calculation results are based on analysis type and calculation type.

        Args:
            scenario_index (int): Index of a scenario.
            calculation_index (int): Index of a calculation.

        Returns:
            dict: Dictionary containing the analysis results of the scenario.

        Raises:
            ValueError: No results or calculationsettings available
        """
        return self._get_result_substructure(scenario_index, calculation_index)

    def _get_result_substructure(
        self, scenario_index: int, calculation_index: int
    ) -> DGeoFlowResult:
        if self.datastructure.has_result(scenario_index):
            calculation = self.datastructure.scenarios[scenario_index].Calculations[
                calculation_index
            ]
            result_id = calculation.ResultsId
            calculation_type = calculation.CalculationType

            results = self.datastructure.get_result_substructure(calculation_type)

            for result in results:
                if result.Id == result_id:
                    return result

        raise ValueError(f"No result found for result id {scenario_index}")

    def serialize(self, location: FilePath | DirectoryPath | BinaryIO):
        """Support serializing to directory while developing for debugging purposes."""
        if isinstance(location, Path) and location.is_dir():
            serializer = DGeoFlowInputSerializer(ds=self.datastructure)
        else:
            serializer = DGeoFlowInputZipSerializer(ds=self.datastructure)
        serializer.write(location)

        if isinstance(location, Path):
            self.filename = location

    def add_soil(self, soil: Soil) -> int:
        """
        Add a new soil to the model. The code must be unique, the id will be generated

        Args:
            soil (Soil): a new soil

        Returns:
            int: id of the added soil
        """
        if self.soils.has_soilcode(soil.code):
            raise ValueError(f"The soil with code {soil.code} is already defined.")

        soil.id = self._get_next_id()
        persistant_soil = self.soils.add_soil(soil)
        return persistant_soil.Id

    def edit_soil(self, code: str, **kwargs: dict) -> PersistableSoil:
        """
        Edit an existing soil with parameter names based on the soil class members

        Args:
            code (str): the code of the soil
            kwargs (dict): the parameters and new values for example 'cohesion=2.0, friction_angle=25.0'

        Returns:
            PersistableSoil: the edited soil
        """
        return self.soils.edit_soil(code, **kwargs)

    def edit_soil_by_name(self, name: str, **kwargs: dict) -> PersistableSoil:
        """
        Edit an existing soil with parameter names based on the soil class members

        Args:
            name (str): the name of the soil
            kwargs (dict): the parameters and new values for example 'cohesion=2.0, friction_angle=25.0'

        Returns:
            PersistableSoil: the edited soil
        """
        return self.soils.edit_soil_by_name(name, **kwargs)

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_layer(
        self,
        points: list[Point],
        soil_code: str,
        label: str = "",
        notes: str = "",
        scenario_id: int = None,
    ) -> int:
        """
        Add a soil layer to the model

        Args:
            points (list[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            soil_code (str): code of the soil for this layer
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_id (int): scenario to add to, defaults to 0

        Returns:
            int: id of the added layer
        """
        scenario_id = scenario_id if scenario_id is not None else self.current_scenario

        if not self.datastructure.has_scenario(scenario_id):
            raise IndexError(f"scenario {scenario_id} is not available")
        geometry = self.datastructure.geometries[scenario_id]

        soillayerscollection = self.datastructure.soillayers[scenario_id]

        # do we have this soil code?
        if not self.soils.has_soilcode(soil_code):
            raise ValueError(
                f"The soil with code {soil_code} is not defined in the soil collection."
            )

        # add the layer to the geometry
        # the checks on the validity of the points are done in the PersistableLayer class
        persistable_layer = geometry.add_layer(
            id=str(self._get_next_id()), label=label, points=points, notes=notes
        )

        # add the connection between the layer and the soil to soillayers
        soil = self.soils.get_soil(soil_code)
        soillayerscollection.add_soillayer(layer_id=persistable_layer.Id, soil_id=soil.id)
        return int(persistable_layer.Id)

    def add_meshproperties(
        self,
        element_size: float = 1.0,
        label: str = "",
        scenario_id: int = None,
        layer_id: int = None,
    ) -> int:
        """
        Add a mesh properties to the model

        Args:
            element_size: size of the mesh elements for the discretization, defaults to 1.0
            scenario_id (int): scenario to add to, defaults to 0
            layer_id (int): layer to add to

        Returns:
            int: id of the added meshproperties collection
        """
        scenario_id = scenario_id if scenario_id is not None else self.current_scenario
        meshpropertiescollection = self.datastructure.mesh_properties[scenario_id]

        persistable_layer = self.get_layer(scenario_id, layer_id)
        meshpropertiescollection.add_meshproperty(
            layer_id=persistable_layer.LayerId, element_size=element_size, label=label
        )

        return int(meshpropertiescollection.Id)

    def add_boundary_condition(
        self,
        points: list[Point],
        head_level: float,
        label: str = "",
        notes: str = "",
        scenario_id: int = None,
    ) -> int:
        """
        Add boundary conditions to the model

        Args:
            points (list[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            head_level (float): level of the hydraulic head for the boundary condition
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_id (int): scenario to add to, defaults to 0

        Returns:
            int: id of the boundary conditions collection
        """
        scenario_id = scenario_id if scenario_id is not None else self.current_scenario
        boundary_conditions = self.datastructure.boundary_conditions[scenario_id]

        boundary_condition_id = self._get_next_id()
        boundary_conditions.add_boundary_condition(
            boundary_condition_id, label, notes, points, head_level
        )

        return boundary_condition_id

    @property
    def scenarios(self) -> list[Scenario]:
        return self.datastructure.scenarios

    def add_scenario(
        self, label: str = "Scenario", notes: str = "", set_current: bool = True
    ) -> int:
        """Add a new scenario to the model.

        Args:
            label: Label for the scenario.
            notes: Notes for the scenario.
            set_current: Whether to make the new scenario the current scenario.

        Returns:
            the id of the new stage
        """
        new_id = self._get_next_id()
        new_scenario_id, new_unique_id = self.datastructure.add_default_scenario(
            label, notes, new_id
        )

        if set_current:
            self.current_scenario = new_scenario_id
            self.current_stage_index = 0
            self.current_calculation_index = 0

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
            scenario_index: The scenario index to add the stage to, defaults to the current scenario.
            label: Label for the stage.
            notes: Notes for the stage.
            set_current: Whether to make the new stage the current stage.

        Returns:
            the id of the new stage
        """
        scenario_index = (
            scenario_index if scenario_index is not None else self.current_scenario
        )

        new_id = self._get_next_id()
        new_stage_index = self.datastructure.add_default_stage(
            scenario_index, label, notes, new_id
        )

        if set_current:
            self.current_stage_index = new_stage_index
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
            scenario_index: The scenario index to add the calculation to, defaults to the current scenario.
            label: Label for the calculation.
            notes: Notes for the calculation.
            set_current: Whether to make the new calculation the current calculation.

        Returns:
            the id of the new stage
        """
        scenario_index = (
            scenario_index if scenario_index is not None else self.current_scenario
        )

        new_calculation_index = self.datastructure.add_default_calculation(
            scenario_index, label, notes
        )

        if set_current:
            self.current_calculation_index = new_calculation_index
        return new_calculation_index

    def set_calculation_type(
        self,
        scenario_index: int = 0,
        calculation_index: int = 0,
        calculation_type: CalculationTypeEnum = CalculationTypeEnum.GROUNDWATER_FLOW,
    ) -> None:
        """
        Sets the calculation type of a calculation.

        Args:
            scenario_index (int): The scenario index to add to, defaults to 0.
            calculation_index (int): The calculation index to add to, defaults to 0.
            calculation_type (CalculationTypeEnum): The calculation type, defaults to GROUNDWATER_FLOW.
        """

        self.datastructure.scenarios[scenario_index].Calculations[
            calculation_index
        ].CalculationType = calculation_type

    def set_pipe_trajectory(
        self,
        scenario_index: int = 0,
        calculation_index: int = 0,
        pipe_trajectory: InternalPipeTrajectory = None,
    ) -> None:
        """
        Sets the pipe trajectory for a calculation.

        Args:
            scenario_index (int): The scenario index to add to, defaults to 0.
            calculation_index (int): The calculation index to add to, defaults to 0.
            pipe_trajectory (PipeTrajectory): The pipe trajectory.
        """

        self.datastructure.scenarios[scenario_index].Calculations[
            calculation_index
        ].PipeTrajectory = pipe_trajectory

    def set_critical_head_boundary_condition(
        self,
        scenario_index: int = 0,
        calculation_index: int = 0,
        boundary_condition_id: int = None,
    ) -> None:
        """
        Sets the critical head boundary condition for a calculation.

        Args:
            scenario_index (int): The scenario index to add to, defaults to 0.
            calculation_index (int): The calculation index to add to, defaults to 0.
            boundary_condition_id (int): The id of the critical head boundary condition.
        """

        self.datastructure.scenarios[scenario_index].Calculations[
            calculation_index
        ].CriticalHeadId = str(boundary_condition_id)

    def set_critical_head_search_parameters(
        self,
        scenario_index: int = 0,
        calculation_index: int = 0,
        minimum_head_level: float = 0,
        maximum_head_level: float = 1,
        step_size: float = 0.1,
    ) -> None:
        """
        Sets the critical head search parameters condition for a calculation.

        Args:
            scenario_index (int): The scenario index to add to, defaults to 0.
            calculation_index (int): The calculation index to add to, defaults to 0.
            minimum_head_level (float): The minimum head level to search at, defaults to 0.
            maximum_head_level (float): The maximum head level to search at, defaults to 1.
            step_size (float): The step size to search with, defaults to 0.1.
        """

        calculation = self.datastructure.scenarios[scenario_index].Calculations[
            calculation_index
        ]

        calculation.CriticalHeadSearchSpace.MinimumHeadLevel = minimum_head_level
        calculation.CriticalHeadSearchSpace.MaximumHeadLevel = maximum_head_level
        calculation.CriticalHeadSearchSpace.StepSize = step_size
