import abc
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Type, Union

from pydantic import DirectoryPath, FilePath

from geolib.geometry import Point
from geolib.models import BaseDataClass, BaseModel
from geolib.soils import Soil
from .dgeoflow_parserprovider import DGeoflowParserProvider

from ...utils import camel_to_snake, snake_to_camel

from .internal import (
    DGeoflowStructure,
    SoilCollection, SoilLayerCollection, PersistableSoilLayer,
)

from .serializer import DGeoflowInputSerializer, DGeoflowInputZipSerializer


class DGeoflowObject(BaseModel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_DGeoflow_sub_structure(self):
        raise NotImplementedError


class DGeoflowModel(BaseModel):
    """D-Geoflow is software for soft soil piping calculations.

    This model can read, modify and create
    .flox files
    """

    current_scenario: int = -1
    datastructure: DGeoflowStructure = DGeoflowStructure()
    current_id: int = -1

    def __init__(self, *args, **data) -> None:
        super().__init__(*args, **data)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def parser_provider_type(self) -> Type[DGeoflowParserProvider]:
        return DGeoflowParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DGeoflowConsole/D-GEO Suite Stability GEOLIB Console.exe")  # TODO: To be adapted

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

    # @property
    # def output(self) -> DGeoflowResult:
    #     # TODO Make something that works for all scenarios
    #     return self.get_result(self.current_scenario)

    # def get_result(self, scenario_id: int) -> Dict:
    #     """
    #     Returns the results of a scenario. Calculation results are based on analysis type and calculation type.
    #
    #     Args:
    #         scenario_id (int): Id of a scenario.
    #
    #     Returns:
    #         dict: Dictionary containing the analysis results of the scenario.
    #
    #     Raises:
    #         ValueError: No results or calculationsettings available
    #     """
    #     result = self._get_result_substructure(scenario_id)
    #     return result  # TODO snake_case keys?
    #
    # def _get_result_substructure(self, scenario_id: int) -> DGeoflowResult:
    #     if self.datastructure.has_result(scenario_id):
    #         result_id = self.datastructure.scenarios[scenario_id].ResultId
    #         calculation_settings = self.datastructure.calculationsettings[scenario_id]
    #         analysis_type = calculation_settings.AnalysisType
    #         calculation_type = calculation_settings.CalculationType
    #
    #         results = self.datastructure.get_result_substructure(
    #             analysis_type, calculation_type
    #         )
    #
    #         for result in results:
    #             if result.Id == result_id:
    #                 return result
    #
    #     raise ValueError(f"No result found for result id {scenario_id}")

    def serialize(self, location: Union[FilePath, DirectoryPath]):
        """Support serializing to directory while developing for debugging purposes."""
        if not location.is_dir():
            serializer = DGeoflowInputZipSerializer(ds=self.datastructure)
        else:
            serializer = DGeoflowInputSerializer(ds=self.datastructure)
        serializer.write(location)
        self.filename = location

    def add_scenario_2(self, label: str, notes: str, set_current=True) -> int:
        """Add a new scenario to the model.

        Args:
            label: Label for the scenario
            notes: Notes for the scenario
            set_current: Whether to make the new scenario the current scenario.

        Returns:
            the id of the new scenario
        """
        new_id = self._get_next_id()
        new_scenario_id, new_unique_id = self.datastructure.add_default_scenario(
            label, notes, new_id
        )

        if set_current:
            self.current_scenario = new_scenario_id
        self.current_id = new_unique_id
        return new_scenario_id

    def copy_scenario(self, label: str, notes: str, set_current=True) -> int:
        """Copy an existing scenario and add it to the model.

        Args:
            label: Label for the scenario
            notes: Notes for the scenario
            set_current: Whether to make the new scenario the current scenario.

        Returns:
            the id of the new scenario
        """
        new_id = self._get_next_id()
        new_scenario_id, new_unique_id = self.datastructure.duplicate_scenario(
            self.current_scenario, label, notes, new_id
        )

        if set_current:
            self.current_scenario = new_scenario_id
        self.current_id = new_unique_id
        return new_scenario_id

    def add_point(self, point: Point, scenario=None) -> int:
        """Add point, which should be unique in the model and return the created point id."""

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
        return persistant_soil.Code

    def edit_soil(self, code: str, **kwargs: dict) -> None:
        """
        Edit an existing soil with parameter names based on the soil class members

        Args:
            code (str): the code of the soil
            kwargs (dict): the parameters and new values for example 'cohesion=2.0, friction_angel=25.0'

        Returns:
            bool: True for succes, False otherwise
        """
        return self.soils.edit_soil(code, **kwargs)

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_layer(
            self,
            points: List[Point],
            soil_code: str,
            label: str = "",
            notes: str = "",
            scenario_id: int = None,
    ) -> int:
        """
        Add a soil layer to the model

        Args:
            points (List[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            soil_code (str): code of the soil for this layer
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_id (int): scenario to add to, defaults to 0

        Returns:
            int: id of the added layer
        """
        scenario_id = scenario_id if scenario_id else self.current_scenario

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

    def add_layeractivation(self, scenario_id: int = None, layer_id: int = None) -> int:
        """
        Add a layer activation to the model

        Args:
            scenario_id (int): scenario to add to, defaults to 0
            layer_id (int): layer to add to

        Returns:
            int: id of the added layeractivation
        """
        scenario_id = scenario_id if scenario_id else self.current_scenario
        layeractivationscollection = self.datastructure.layer_activations[scenario_id]

        persistable_layer = self.get_layer(scenario_id, layer_id)
        layeractivationscollection.add_layeractivation(layer_id=persistable_layer.LayerId)

        return int(layeractivationscollection.Id)

    def add_meshproperties(self,
                           element_size: float = 1.0,
                           label: str = "",
                           scenario_id: int = None,
                           layer_id: int = None) -> int:
        """
        Add a mesh properties to the model

        Args:
            element_size: size of the mesh elements for the discretization, defaults to 1.0
            scenario_id (int): scenario to add to, defaults to 0
            layer_id (int): layer to add to

        Returns:
            int: id of the added meshproperties collection
        """
        scenario_id = scenario_id if scenario_id else self.current_scenario
        meshpropertiescollection = self.datastructure.mesh_properties[scenario_id]

        persistable_layer = self.get_layer(scenario_id, layer_id)
        meshpropertiescollection.add_meshproperty(layer_id=persistable_layer.LayerId, element_size=element_size,
                                                  label=label)

        return int(meshpropertiescollection.Id)

    def add_boundarycondition(self, points: List[Point], head_level: float, label: str = "", notes: str = "",
                              scenario_id: int = None) -> int:
        """
        Add boundary conditions to the model

        Args:
            points (List[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            head_level (float): level of the hydraulic head for the boundary condition
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            scenario_id (int): scenario to add to, defaults to 0

        Returns:
            int: id of the boundary conditions collection
        """
        scenario_id = scenario_id if scenario_id else self.current_scenario
        boundaryconditions = self.datastructure.boundary_conditions[scenario_id]

        boundaryconditions.add_boundarycondition(label, notes, points, head_level)

        return int(boundaryconditions.Id)

    def add_scenario(self, scenario_id: int = None, boundaryconditions_id: int = None, layeractivations_id: int = None,
                     soillayers_id: int = None, geometry_id: int = None, meshproperties_id: int = None, label: str = "",
                     notes: str = "",
                     calculations_notes: str = "", stage_notes: str = "", calculations_label: str = None,
                     stage_label: str = None) -> int:
        """
        Add a scenario to the model

        Args:
            scenario_id (int): scenario to add to, defaults to 0
            boundaryconditions_id (int): id of the boundary conditions collection to add tothe scenario
            layeractivations_id (int): id of the layer activation collection to add tothe scenario
            soillayers_id (int): id of the soil layers to add to the scenario
            geometry_id (int): id of the geometry to add to the scenario
            meshproperties_id (int): id of the mesh properties to add to the scenario
            label (str): label of the scenario, defaults to empty string
            notes (str): notes of the scenario, defaults to empty string
            calculations_notes (str): notes of the calculation, defaults to empty string
            stage_notes (str): notes of the stage, defaults to empty string
            calculations_label (str): label of the calculation, defaults to empty string
            stage_label (str): label of the stage, defaults to empty string

        Returns:
            int: id of the scenario
        """
        scenario_id = scenario_id if scenario_id else self.current_scenario

        scenarios = self.datastructure.scenarios[scenario_id]

        scenarios.Label = label
        scenarios.Notes = notes
        scenarios.GeometryId = geometry_id
        scenarios.SoilLayersId = soillayers_id
        scenarios.add_calculation(label=calculations_label, notes=calculations_notes,
                                  mesh_properties_id=meshproperties_id)
        scenarios.add_stage(label=stage_label, notes=stage_notes,
                            boundaryconditions_collection_id=boundaryconditions_id,
                            layeractivation_collection_id=layeractivations_id)
        return int(scenarios.Id)
