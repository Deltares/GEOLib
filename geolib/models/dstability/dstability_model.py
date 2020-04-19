"""

Usage::

    >>> dstab = DStabilityModel.parse("test.stix")
    >>> dstab.execute()
    >>> dstab.output
    <dict>

"""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel as DataClass
from pydantic import DirectoryPath

from geolib.geometry import Point
from geolib.models import BaseModel
from geolib.soils import Soil

from .dstability_parserprovider import DStabilityParserProvider
from .loads import DStabilityLoad
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


class DStabilityModel(BaseModel):
    """D-Stability is software for soft soil slope stability.
    
    This model can read, modify and create
    \*.stix files
    """

    @property
    def parser_provider_type(self) -> DStabilityParserProvider:
        return DStabilityParserProvider

    current_stage: int = 0

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

    @property
    def points(self):
        """Enables easy access to the points in the internal dict-like datastructure. Also enables edit/delete for individual points."""

    def add_layer(
        self,
        points: List[int],
        material: Soil,
        state_point=Optional[Point],
        stage=None,
    ) -> int:
        """Create layer with Soil in model. 
        
        For probabilistic values; If state_point is None, the centroid will be used.
        """

    def add_head_line(
        self, label: str, points: List[int], is_phreatic=False, stage=None
    ) -> int:
        """Add a hydraulic headline to the object."""
        pass

    def add_reference_line(
        self,
        label: str,
        points: List[int],
        above_headline_id: int,
        below_headline_id: int,
        stage=None,
    ):
        """BB. Add a reference line to the object."""

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
