"""

Usage::

    >>> dstab = DStabilityModel.parse("test.stix")
    >>> dstab.execute()
    >>> dstab.output
    <dict>

"""
import abc
import re
from enum import Enum
from pathlib import Path
from typing import List, Optional, Type, Union, Dict, Set

from pydantic import BaseModel as DataClass
from pydantic import DirectoryPath

from geolib.geometry import Point
from geolib.models import BaseModel
from geolib.soils import Soil

from .dstability_parserprovider import DStabilityParserProvider
from .internal import (
    AnalysisType,
    BishopSlipCircleResult,
    CalculationType,
    DStabilityStructure,
    DStabilityResult,
    SoilCollection,
    SpencerSlipPlaneResult,
    UpliftVanSlipCircleResult,
    Waternet,
)
from .loads import DStabilityLoad, Consolidation
from .reinforcements import DStabilityReinforcement
from .serializer import DStabilityInputSerializer


class DStabilityCalculationType(Enum):
    """Set Type of Calculation."""

    BoundarySearch = 1
    SingleCalc = 2


class DStabilityCalculationModel(Enum):
    """Set Type of Calculation."""

    Bishop = 1
    UpliftVan = 2
    Spencer = 3


class DStabilityAnalysisMethod(DataClass):
    """Options to choose for calculation.

    .. todo::
        Determine proper classes for the 6
        possible options, including swarms etc.
    """


class DStabilityObject(BaseModel, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_dstability_sub_structure(self):
        raise NotImplementedError


class DStabilityModel(BaseModel):
    """D-Stability is software for soft soil slope stability.

    This model can read, modify and create
    .stix files
    """

    @property
    def parser_provider_type(self) -> Type[DStabilityParserProvider]:
        return DStabilityParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DStabilityConsole/D-GEO Suite Stability GEOLIB Console.exe")

    @property
    def soils(self) -> SoilCollection:
        """Enables easy access to the soil in the internal dict-like datastructure. Also enables edit/delete for individual soils."""
        return self.datastructure.soils
    
    current_id: int = 100  # todo > after reading inputfiles, check for the next id or think about another implementation of the id
    current_stage: int = 0
    datastructure: DStabilityStructure = DStabilityStructure()

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    @property
    def waternets(self) -> List[Waternet]:
        return self.datastructure.waternets

    @property
    def output(self):
        # TODO Make something that works for all stages
        return self.results(self.current_stage)

    def get_result(self, stage_id: int) -> Dict:
        """
        Returns the results of a stage. Calculation results are based on analysis type and calculation type.

        Args:
            stage_id (int): Id of a stage.

        Returns:
            dict: Dictionary containing the analysis results of the stage.

        Raises:
            ValueError: No results or calculationsettings available
        """
        result = self._get_result_substructure(stage_id)
        return result.dict()  # TODO snake_case keys?

    def _get_result_substructure(self, stage_id: int) -> DStabilityResult:
        if self.datastructure.has_result(stage_id):
            result_id = self.datastructure.stages[stage_id].ResultId
            calculation_settings = self.datastructure.calculationsettings[stage_id]
            analysis_type = calculation_settings.AnalysisType
            calculation_type = calculation_settings.CalculationType

            results = self.datastructure.get_result_substructure(
                analysis_type, calculation_type
            )

            for result in results:
                if result.Id == result_id:
                    return result

        raise ValueError(f"No result found for result id {stage_id}")

    def get_slipcircle_result(self, stage_id: int) -> Union[BishopSlipCircleResult, UpliftVanSlipCircleResult]:
        """
        Get the slipcircle(s) of the calculation result of a given stage.

        Args:
            stage_id (int): stage for which to get the available results

        Returns:
            Dict: dictionary of the available slipcircles per model for the given stage
        
        Raises:
            ValueError: Result is not available for provided stage id
            AttributeError: When the result has no slipcircle. Try get the slipplane
        """
        result = self._get_result_substructure(stage_id)
        return result.get_slipcircle_output()

    def get_slipplane_result(self, stage_id: int = 0) -> SpencerSlipPlaneResult:
        """
        Get the slipplanes of the calculations result of a stage.

        Args:
            stage_id (int): stage for which to get the available results

        Returns:
            dict: dictionary of the available slip planes per model for the given stage
        
        Raises:
            ValueError: Result is not available for provided stage id
            AttributeError: When the result has no slipplane. Try get the slipcircle
        """
        result = self._get_result_substructure(stage_id)
        return result.get_slipplane_output()

    def serialize(self, foldername: DirectoryPath):

        serializer = DStabilityInputSerializer(ds=self.datastructure)
        serializer.write(foldername)

    def add_stage(self, label: str, notes: str, copy=True, set_current=True) -> int:
        """Add a new stage to the model. Copies current stage if copy is True. Returns a unique id."""

    def add_point(self, point: Point, stage=None) -> int:
        """Add point, which should be unique in the model and return the created point id.

        .. todo::
            Determine a default axis order, the Z/Y axes are swapped in DStability compared to D-Settlement.
        """

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
        stage_id: int = None
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

        Todo:
            * the initial geometry does not have an id
        """
        stage_id = stage_id if stage_id else self.current_stage

        try:
            geometry = self.datastructure.geometries[stage_id]
            soillayerscollection = self.datastructure.soillayers[stage_id]
        except IndexError:
            raise IndexError(f"stage {stage_id} is not available")

        # do we have this soil code?
        if not self.soils.has_soilcode(soil_code):
            raise ValueError(f"The soil with code {soil_code} is not defined in the soil collection.")

        # add the layer to the geometry
        # the checks on the validity of the points are done in the PersistableLayer class
        persistable_layer = geometry.add_layer(
            id=str(self._get_next_id()),
            label=label,
            points=points,
            notes=notes
        )

        # add the connection between the layer and the soil to soillayers
        soil = self.soils.get_soil(soil_code)
        soillayerscollection.add_soillayer(
            layer_id=persistable_layer.Id,
            soil_id=soil.id
        )
        return int(persistable_layer.Id)

    def add_head_line(
        self,
        points: List[Point],
        label: str = "",
        notes: str = "",
        is_phreatic_line: bool = False,
        stage_id: int = None,
    ) -> int:
        """
        Add head line to the model

        Args:
            points (List[Point]): list of Point classes
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            is_phreatic_line (bool): set as phreatic line, defaults to False
            stage_id (int): stage to add to, defaults to current stage

        Returns:
            bool: id of the added headline
        """
        stage_id = stage_id if stage_id else self.current_stage

        try:
            waternet = self.waternets[stage_id]
        except IndexError:
            raise IndexError(f"stage {stage_id} is not available")

        persistable_headline = waternet.add_head_line(
            str(self._get_next_id()),
            label,
            notes,
            points,
            is_phreatic_line
        )
        return int(persistable_headline.Id)

    def add_reference_line(
        self,
        points: List[Point],
        bottom_headline_id: int,
        top_head_line_id: int,
        label: str = "",
        notes: str = "",
        stage_id: int = None,
    ) -> int:
        """
        Add reference line to the model

        Args:
            points (List[Point]): list of Point classes
            bottom_headline_id (int): id of the headline to use as the bottom headline
            top_head_line_id (int): id of the headline to use as the top headline
            label (str): label defaults to empty string
            notes (str): notes defaults to empty string
            stage_id (int): stage to add to, defaults to 0

        Returns:
            int: id of the added reference line
        """
        stage_id = stage_id if stage_id else self.current_stage

        try:
            waternet = self.waternets[stage_id]
        except IndexError:
            raise IndexError(f"stage {stage_id} is not available")

        persistable_referenceline = waternet.add_reference_line(
            str(self._get_next_id()),
            label,
            notes,
            points,
            str(bottom_headline_id),
            str(top_head_line_id),
        )
        return int(persistable_referenceline.Id)

    def add_state_line(
        self,
        label: str,
        points: List[int],
        state_point: int,
        above_material: Soil,
        below_material: Soil,
    ):
        """Add state line. From the Soils, only the state parameters are used."""

    def add_load(
        self,
        load: DStabilityLoad,
        consolidations: Optional[List[Consolidation]] = None,
        stage_id: Optional[int] = None,
    ) -> None:
        """Add a load to the object.

        The geometry should be defined before adding loads.

        If no consolidations are provided, a Consolidation with default values will be made for each SoilLayer.
        It is not possible to set consolidation degrees of loads afterwards since they don't have an id.

        Args:
            load: A subclass of DStabilityLoad.
            stage_id: Id used to identify the stage to which the load is linked. If no stage_id is proved, the current stage_id will be taken.

        Raises:
            ValueError: When the provided load is no subclass of DStabilityLoad, an invalid stage_id is provided, or the datastructure is no longer valid.
        """
        stage_id = stage_id if stage_id is not None else self.current_stage

        if not issubclass(type(load), DStabilityLoad):
            raise ValueError(
                f"load should be a subclass of DstabilityReinforcement, received {load}"
            )
        if self.datastructure.has_soil_layers(stage_id) and self.datastructure.has_loads(stage_id):
            if consolidations is None:
                consolidations = self._get_default_consolidations(stage_id)
            else:
                self._verify_consolidations(consolidations, stage_id)
            self.datastructure.loads[stage_id].add_load(load)
        else:
            raise ValueError(f"No loads found for stage id {stage_id}")

    def add_soil_layer_consolidations(
        self,
        soil_layer_id: int,
        consolidations: Optional[List[Consolidation]] = None,
        stage_id: int = None,
    ) -> None:
        """Add consolidations for a layer (layerload).

        Consolidations cannot be added when adding soil layers since in the consolidations, all other soil layers need to be referred.
        Therefore, all soillayers in a stage should be defined before setting consolidation and
        the number of consolidations given should equal the amount of layers.

        Args:
            soil_layer_id: Consolidation is set for this soil layer id.
            consolidations: List of Consolidation. Must contain a Consolidation for every other layer.
            stage_id: Id used to identify the stage to which the load is linked. If no stage_id is proved, the current stage_id will be taken.

        Raises:
            ValueError: When the provided load is no subclass of DStabilityLoad, an invalid stage_id is provided, or the datastructure is no longer valid.
        """
        stage_id = stage_id if stage_id is not None else self.current_stage

        if self.datastructure.has_soil_layer(stage_id, soil_layer_id) and self.datastructure.has_loads(stage_id):
            if consolidations is None:
                consolidations = self._get_default_consolidations(stage_id)
            else:
                self._verify_consolidations(consolidations, stage_id)

            self.datastructure.loads[stage_id].add_layer_load(soil_layer_id, consolidations)
        else:
            raise ValueError(f"No soil layers found found for stage id {stage_id}")

    def _get_default_consolidations(self, stage_id: int) -> List[Consolidation]:
        """Length of the consolidations is equal to the amount of soil layers"""
        if self.datastructure.has_soil_layers(stage_id):
            soil_layer_ids: Set[str] = {layer.LayerId for layer in self.datastructure.soillayers[stage_id].SoilLayers}
            return [Consolidation(layer_id=layer_id) for layer_id in soil_layer_ids]

        raise ValueError(f"No soil layers found for stage id {stage_id}")

    def _verify_consolidations(self, consolidations: List[Consolidation], stage_id: int) -> None:
        if self.datastructure.has_soil_layers(stage_id):
            consolidation_soil_layer_ids: Set[str] = {str(c.layer_id) for c in consolidations}
            soil_layer_ids: Set[str] = {layer.LayerId for layer in self.datastructure.soillayers[stage_id].SoilLayers}
            if consolidation_soil_layer_ids != soil_layer_ids:
                raise ValueError(f"Received consolidations ({consolidation_soil_layer_ids}) should contain all soil layer ids ({soil_layer_ids})")
        else:
            raise ValueError(f"No soil layers found for stage id {stage_id}")

    def add_reinforcement(
        self, reinforcement: DStabilityReinforcement, stage_id: Optional[int] = None,
    ) -> None:
        """Add a reinforcement to the model.

        Args:
            reinforcement: A subclass of DStabilityReinforcement.
            stage_id: Id used to identify the stage to which the reinforcement is linked.

        Returns:
            int: Assigned id of the reinforcements (collection object of all reinforcements for a stage).

        Raises:
            ValueError: When the provided reinforcement is no subclass of DStabilityReinforcement, an invalid stage_id is provided, or the datastructure is no longer valid.
        """
        stage_id = stage_id if stage_id is not None else self.current_stage

        if not issubclass(type(reinforcement), DStabilityReinforcement):
            raise ValueError(
                f"reinforcement should be a subclass of DstabilityReinforcement, received {reinforcement}"
            )

        if self.datastructure.has_reinforcements(stage_id):
            self.datastructure.reinforcements[stage_id].add_reinforcement(reinforcement)
        else:
            raise ValueError(
                    f"No reinforcements found for stage found with id {stage_id}"
                )

    def set_model(self, analysis_method: DStabilityAnalysisMethod, stage=None):
        """Sets the calculation type based on the given input and parameters."""
