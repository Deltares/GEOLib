"""

Usage::

    >>> dstab = DStabilityModel.parse("test.stix")
    >>> dstab.execute()
    >>> dstab.output
    <dict>

"""

import re
from enum import Enum
from typing import List, Optional, Union, Type

from pathlib import Path
from pydantic import BaseModel as DataClass
from pydantic import DirectoryPath

from geolib.geometry import Point
from geolib.models import BaseModel, BaseModelStructure
from geolib.soils import Soil

from .dstability_parserprovider import DStabilityParserProvider
from .loads import DStabilityLoad
from .reinforcements import DStabilityReinforcement
from .serializer import DStabilityInputSerializer
from .internal import Waternet, SoilCollection, DStabilityStructure


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


class DStabilityModel(BaseModel):
    """D-Stability is software for soft soil slope stability.

    This model can read, modify and create
    *.stix files
    """

    datastructure: BaseModelStructure = DStabilityStructure()

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

    current_stage: int = 0
    current_id: int = 100  # todo > after reading inputfiles, check for the next id or think about another implementation of the id

    datastructure: DStabilityStructure = DStabilityStructure()

    def _get_next_id(self) -> int:
        self.current_id += 1
        return self.current_id

    @property
    def waternets(self) -> List[Waternet]:
        return self.datastructure.waternets

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
        self.soils.add_soil(soil)
        return soil.id

    def remove_soil(self, id: int) -> None:
        """
        Remove a soil from to the model.

        Args:
            id (int): the code of the soil

        Returns:
            bool: True for succes, False otherwise
        """
        for idx, soil in enumerate(self.soils.Soils):
            if soil.Id == id:
                del self.soils.Soils[idx]
                return

        raise ValueError(f"The soil with code {id} is not found.")

    def edit_soil(self, id: int, **kwargs) -> None:
        """
        Edit an existing soil with parameter names based on the soil class members

        Args:
            id (int): the id of the soil
            kwargs (dict): the parameters and new values

        Returns:
            bool: True for succes, False otherwise
        """
        soil = self.soils.get_soil(id)

        if soil is None:
            raise ValueError(f"Unknown soil id {id}.")

        for k, v in kwargs.items():
            try:
                setattr(soil, k, v)
            except AttributeError:
                raise ValueError(f"Unknown soil parameter {k}.")

        self.soils.edit_soil(soil)

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_layer(
        self, points: List[int], material: Soil, state_point=Optional[Point], stage=None,
    ) -> int:
        """Create layer with Soil in model. 

        For probabilistic values; If state_point is None, the centroid will be used.
        """

    def add_head_line(
            self,
            points: List[Point],
            label: str = "",
            notes: str = "",
            is_phreatic_line: bool = False,
            stage_id: int = None
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

        persitable_headline = waternet.add_head_line(
            str(self._get_next_id()),
            label,
            notes,
            points,
            is_phreatic_line
        )
        return int(persitable_headline.Id)

    def add_reference_line(
        self,
        points: List[Point],
        bottom_headline_id: int,
        top_head_line_id: int,
        label: str = "",
        notes: str = "",
        stage_id: int = None
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
            str(top_head_line_id)
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
        self, load: DStabilityLoad, x: Optional[float], z: Optional[float], stage=None,
    ) -> int:
        """Add a load to the object. Coordinates are required for loads except the Earthquake model."""

    def set_consolidation(
        self,
        layerid: Optional[int],
        loadid: Optional[int],
        percentages: List[float],
        stage=None,
    ):
        """Set layer consolidation percentages for a load or layer.

        Either a layerid needs to be given and loadid set to None, or vice versa.
        The number of percentages given should equal the current layers.
        """

    def add_reinforcement(
        self,
        reinforcement: DStabilityReinforcement,
        startpoint: Point,
        endpoint: Optional[Point],
        stage=None,
    ):
        """Add reinforcement to model.

        A start point is required, an end point is only required for Textile and ForbiddenLine.
        """

    def set_model(self, analysis_method: DStabilityAnalysisMethod, stage=None):
        """Sets the calculation type based on the given input and parameters."""
