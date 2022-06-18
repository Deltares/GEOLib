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
    SoilCollection,
)

from .serializer import DGeoflowInputSerializer, DGeoflowInputZipSerializer


class DGeoflowObject(BaseModel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_DGeoflow_sub_structure(self):
        raise NotImplementedError


class DGeoflowModel(BaseModel):
    """D-Stability is software for soft soil slope stability.

    This model can read, modify and create
    .stix files
    """

    current_stage: int = -1
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
        return Path("DGeoflowConsole/D-GEO Suite Stability GEOLIB Console.exe") # TODO: To be adapted

    @property
    def soils(self) -> SoilCollection:
        """Enables easy access to the soil in the internal dict-like datastructure. Also enables edit/delete for individual soils."""
        return self.datastructure.soils

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)
        self.current_id = self.datastructure.get_unique_id()

    # @property
    # def output(self) -> DGeoflowResult:
    #     # TODO Make something that works for all stages
    #     return self.get_result(self.current_stage)

    # def get_result(self, stage_id: int) -> Dict:
    #     """
    #     Returns the results of a stage. Calculation results are based on analysis type and calculation type.
    #
    #     Args:
    #         stage_id (int): Id of a stage.
    #
    #     Returns:
    #         dict: Dictionary containing the analysis results of the stage.
    #
    #     Raises:
    #         ValueError: No results or calculationsettings available
    #     """
    #     result = self._get_result_substructure(stage_id)
    #     return result  # TODO snake_case keys?

    # def _get_result_substructure(self, stage_id: int) -> DGeoflowResult:
    #     if self.datastructure.has_result(stage_id):
    #         result_id = self.datastructure.stages[stage_id].ResultId
    #         calculation_settings = self.datastructure.calculationsettings[stage_id]
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
    #     raise ValueError(f"No result found for result id {stage_id}")


    def serialize(self, location: Union[FilePath, DirectoryPath]):
        """Support serializing to directory while developing for debugging purposes."""
        if not location.is_dir():
            serializer = DGeoflowInputZipSerializer(ds=self.datastructure)
        else:
            serializer = DGeoflowInputSerializer(ds=self.datastructure)
        serializer.write(location)
        self.filename = location

    def add_point(self, point: Point, stage=None) -> int:
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
        stage_id: int = None,
    ) -> int:
        """
        Add a soil layer to the model

        Args:
            points (List[Point]): list of Point classes, in clockwise order (non closed simple polygon)
            soil_code (str): code of the soil for this layer
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            stage_id (int): stage to add to, defaults to 0

        Returns:
            int: id of the added layer
        """
        stage_id = stage_id if stage_id else self.current_stage

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        geometry = self.datastructure.geometries[stage_id]
        soillayerscollection = self.datastructure.soillayers[stage_id]

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

    #TODO: Check if below is still needed for DGeoflow

    # def set_model(self, analysis_method: DGeoflowAnalysisMethod, stage_id=None):
    #     """Sets the model and applies the given parameters
    #
    #     Args:
    #         analysis_method (DGeoflowAnalysisMethod): A subclass of DGeoflowAnalysisMethod.
    #         stage_id: Id used to identify the stage to which the analysis method is linked.
    #
    #     Raises:
    #         ValueError: When the provided analysismethod is no subclass of DGeoflowAnalysisMethod,
    #         an invalid stage_id is provided, the analysis method is not known or the datastructure is no longer valid.
    #     """
    #     stage_id = stage_id if stage_id else self.current_stage
    #
    #     if not self.datastructure.has_stage(stage_id):
    #         raise IndexError(f"stage {stage_id} is not available")
    #
    #     calculationsettings = self.datastructure.calculationsettings[stage_id]
    #
    #     _analysis_method_mapping = {
    #         AnalysisType.BISHOP: calculationsettings.set_bishop,
    #         AnalysisType.BISHOP_BRUTE_FORCE: calculationsettings.set_bishop_brute_force,
    #         AnalysisType.SPENCER: calculationsettings.set_spencer,
    #         AnalysisType.SPENCER_GENETIC: calculationsettings.set_spencer_genetic,
    #         AnalysisType.UPLIFT_VAN: calculationsettings.set_uplift_van,
    #         AnalysisType.UPLIFT_VAN_PARTICLE_SWARM: calculationsettings.set_uplift_van_particle_swarm,
    #     }
    #
    #     try:
    #         _analysis_method_mapping[analysis_method.analysis_type](
    #             analysis_method._to_internal_datastructure()
    #         )
    #     except KeyError:
    #         raise ValueError(
    #             f"Unknown analysis method {analysis_method.analysis_type.value} found"
    #         )
