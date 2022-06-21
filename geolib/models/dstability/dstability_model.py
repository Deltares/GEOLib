import abc
import re
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Type, Union

from pydantic import DirectoryPath, FilePath

from geolib.geometry import Point
from geolib.models import BaseDataClass, BaseModel
from geolib.soils import Soil

from ...utils import camel_to_snake, snake_to_camel
from .analysis import DStabilityAnalysisMethod
from .dstability_parserprovider import DStabilityParserProvider
from .internal import (
    AnalysisType,
    BishopSlipCircleResult,
    CalculationType,
    DStabilityResult,
    DStabilityStructure,
    PersistablePoint,
    SoilCollection,
    SpencerSlipPlaneResult,
    Stage,
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

    current_stage: int = -1
    datastructure: DStabilityStructure = DStabilityStructure()
    current_id: int = -1

    def __init__(self, *args, **data) -> None:
        super().__init__(*args, **data)
        self.current_id = self.datastructure.get_unique_id()

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

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    def parse(self, *args, **kwargs):
        super().parse(*args, **kwargs)
        self.current_id = self.datastructure.get_unique_id()

    @property
    def waternets(self) -> List[Waternet]:
        return self.datastructure.waternets

    @property
    def output(self) -> DStabilityResult:
        # TODO Make something that works for all stages
        return self.get_result(self.current_stage)

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
        return result  # TODO snake_case keys?

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

    def get_slipcircle_result(
        self, stage_id: int
    ) -> Union[BishopSlipCircleResult, UpliftVanSlipCircleResult]:
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

    def serialize(self, location: Union[FilePath, DirectoryPath]):
        """Support serializing to directory while developing for debugging purposes."""
        if not location.is_dir():
            serializer = DStabilityInputZipSerializer(ds=self.datastructure)
        else:
            serializer = DStabilityInputSerializer(ds=self.datastructure)
        serializer.write(location)
        self.filename = location

    def add_stage(self, label: str, notes: str, set_current=True) -> int:
        """Add a new stage to the model.

        Args:
            label: Label for the stage
            notes: Notes for the stage
            set_current: Whether to make the new stage the current stage.

        Returns:
            the id of the new stage
        """
        new_id = self._get_next_id()
        new_stage_id, new_unique_id = self.datastructure.add_default_stage(
            label, notes, new_id
        )

        if set_current:
            self.current_stage = new_stage_id
        self.current_id = new_unique_id
        return new_stage_id

    def copy_stage(self, label: str, notes: str, set_current=True) -> int:
        """Copy an existing stage and add it to the model.

        Args:
            label: Label for the stage
            notes: Notes for the stage
            set_current: Whether to make the new stage the current stage.

        Returns:
            the id of the new stage
        """
        new_id = self._get_next_id()
        new_stage_id, new_unique_id = self.datastructure.duplicate_stage(
            self.current_stage, label, notes, new_id
        )

        if set_current:
            self.current_stage = new_stage_id
        self.current_id = new_unique_id
        return new_stage_id

    @property
    def stages(self) -> List[Stage]:
        return self.datastructure.stages

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

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        waternet = self.waternets[stage_id]

        persistable_headline = waternet.add_head_line(
            str(self._get_next_id()), label, notes, points, is_phreatic_line
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

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        waternet = self.waternets[stage_id]

        persistable_referenceline = waternet.add_reference_line(
            str(self._get_next_id()),
            label,
            notes,
            points,
            str(bottom_headline_id),
            str(top_head_line_id),
        )
        return int(persistable_referenceline.Id)

    def add_state_point(
        self,
        state_point: DStabilityStatePoint,
        stage_id: int = None,
    ) -> int:
        """
        Add state point to the model

        Args:
            state_point (DStabilityStatePoint): DStabilityStatePoint class
            stage_id (int): stage_id (int): stage to add to, defaults to the current stage

        Returns:
            int: id of the added add_state_point

        Todo:
            Check if point lies within the given layer
        """
        stage_id = stage_id if stage_id else self.current_stage

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        states = self.datastructure.states[stage_id]

        # check if the given layer id is valid
        try:
            _ = self.datastructure.geometries[stage_id].get_layer(state_point.layer_id)
        except ValueError:
            raise ValueError(f"No layer with id '{state_point.layer_id} in this geometry")

        # todo > check if point is in layer

        state_point.id = (
            self._get_next_id()
        )  # the user does not know the id so we have to add it
        persistable_statepoint = state_point._to_internal_datastructure()
        states.add_state_point(persistable_statepoint)
        return int(persistable_statepoint.Id)

    def add_state_line(
        self,
        points: List[Point],
        state_points: List[DStabilityStateLinePoint],
        stage_id: int = None,
    ) -> None:
        """
        Add state line. From the Soils, only the state parameters are used.

        points are a list of points with x,z
        state_point are a list of DStabilit.. where ONLY the x is used, the Z will be calculated

        No result PersistableStateLine has no Id
        """
        # 1. check of de gegeven points aanwezig zijn in de layers want ze MOETEN op een
        #    punt uit een layer liggen
        # 2. voeg deze punten toe aan de PersistableStateLine.Points
        # 3. voeg op alle x coordinaten in DStabilityStateLinePoint[] een PersistableStateLinePoint object toe
        #    let op dat points.xmin <= x <= points.xmax
        # 4. voeg de PersistableStateLine toe aan de interne datastructuur
        # 5. geef de id terug
        stage_id = stage_id if stage_id else self.current_stage

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        states = self.datastructure.states[stage_id]

        # each point should belong to a layer
        persistable_points = []

        for point in points:
            point.id = self._get_next_id()  # assign a new id
            persistable_points.append(PersistablePoint(X=point.x, Z=point.z))

        persistable_state_line_points = []
        for state_point in state_points:
            state_point.id = self._get_next_id()  # assign a new id
            persistable_state_line_points.append(state_point._to_internal_datastructure())

        states.add_state_line(persistable_points, persistable_state_line_points)

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
        if self.datastructure.has_soil_layers(stage_id) and self.datastructure.has_loads(
            stage_id
        ):
            if consolidations is None:
                consolidations = self._get_default_consolidations(stage_id)
            else:
                self._verify_consolidations(consolidations, stage_id)
            self.datastructure.loads[stage_id].add_load(load, consolidations)
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

        if self.datastructure.has_soil_layer(
            stage_id, soil_layer_id
        ) and self.datastructure.has_loads(stage_id):
            if consolidations is None:
                consolidations = self._get_default_consolidations(stage_id, soil_layer_id)
            else:
                self._verify_consolidations(consolidations, stage_id, soil_layer_id)

            self.datastructure.loads[stage_id].add_layer_load(
                soil_layer_id, consolidations
            )
        else:
            raise ValueError(f"No soil layers found found for stage id {stage_id}")

    def _get_default_consolidations(
        self, stage_id: int, exclude_soil_layer_id: Optional[int] = None
    ) -> List[Consolidation]:
        """Length of the consolidations is equal to the amount of soil layers.

        If exclude_soil_layer_id is provided, that specific soil layer id is not included in the consolidations.
        """
        if self.datastructure.has_soil_layers(stage_id):
            soil_layer_ids = self.datastructure.soillayers[stage_id].get_ids(
                exclude_soil_layer_id
            )
            return [Consolidation(layer_id=layer_id) for layer_id in soil_layer_ids]

        raise ValueError(f"No soil layers found for stage id {stage_id}")

    def _verify_consolidations(
        self,
        consolidations: List[Consolidation],
        stage_id: int,
        exclude_soil_layer_id: Optional[int] = None,
    ) -> None:
        if self.datastructure.has_soil_layers(stage_id):
            consolidation_soil_layer_ids: Set[str] = {
                str(c.layer_id) for c in consolidations
            }
            soil_layer_ids = self.datastructure.soillayers[stage_id].get_ids(
                exclude_soil_layer_id
            )

            if consolidation_soil_layer_ids != soil_layer_ids:
                raise ValueError(
                    f"Received consolidations ({consolidation_soil_layer_ids}) should contain all soil layer ids ({soil_layer_ids})"
                )
        else:
            raise ValueError(f"No soil layers found for stage id {stage_id}")

    def add_reinforcement(
        self,
        reinforcement: DStabilityReinforcement,
        stage_id: Optional[int] = None,
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

    def set_model(self, analysis_method: DStabilityAnalysisMethod, stage_id=None):
        """Sets the model and applies the given parameters

        Args:
            analysis_method (DStabilityAnalysisMethod): A subclass of DStabilityAnalysisMethod.
            stage_id: Id used to identify the stage to which the analysis method is linked.

        Raises:
            ValueError: When the provided analysismethod is no subclass of DStabilityAnalysisMethod,
            an invalid stage_id is provided, the analysis method is not known or the datastructure is no longer valid.
        """
        stage_id = stage_id if stage_id else self.current_stage

        if not self.datastructure.has_stage(stage_id):
            raise IndexError(f"stage {stage_id} is not available")

        calculationsettings = self.datastructure.calculationsettings[stage_id]

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
