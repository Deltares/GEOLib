from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel as DataModel

from geolib.geometry import Point
from geolib.models import BaseModel
from geolib.soils import Soil
from geolib.soils.layers import Profile

from .constructions import DiaphragmWall, Pile, Sheet
from .loads import (
    Earthquake,
    HorizontalLineLoad,
    Moment,
    NormalForce,
    SoilDisplacement,
    SurchargeLoad,
    UniformLoad,
)
from .supports import Anchor, RigidSupport, SpringSupport, Strut


class CalculationType(Enum):
    """Calculation Options for each Model."""


class ModelType(DataModel):
    """Base Class for Model types (Pile, Sheet, Wall)."""

    calculation_type: CalculationType


class Side(Enum):
    """Class to determine passive side."""

    AUTO = 0
    LEFT = 1  # TODO check left/right numbers
    RIGHT = 2


class DSheetpilingModel(BaseModel):
    """DSheetPiling is a tool used to design sheetpile and diaphragm walls and horizontally loaded piles.

    This model can read, modify and create
    \*.shi files, read \*.shd and \*.err files.
    """

    current_stage: int = 0
    water_weight: float = 9.81

    @property
    def parser_provider_type(self):
        raise NotImplementedError("Not implemented yet.")

    def add_stage(
        self,
        label: str,
        notes: str,
        copy=True,
        passive_side=Side,
        pile_top_displacement=Optional[float],
        set_current=True,
    ) -> int:
        """Add a new stage to the model. Copies current stage if copy is True. Returns a unique id."""

    def set_model(self, model: ModelType, elastic=True, stage=None):
        """(Re)Set ModelType (Pile, Sheet, Wall) for stage in model."""

    def add_phreatic_line(self, left=Point, right=Point, stage=None):
        """Set water level. Only the y of the Point is used."""

    def add_surface(self, left=List[Point], right=List[Point], stage=None):
        """Add surface to model. 

        .. todo::
            Determine how whether both should have positive X direction
        """

    def add_profile(self, left: Profile, right=Profile, stage=None):
        """Add profile on either left/rightside of the model. Requires setup of the Profile first.
        
        .. todo::
            Can we use the add_layer method here as well?
        """

    def add_sheet(
        self,
        sheet: Union[Sheet, DiaphragmWall],
        location_top: Point,
        location_bottom: Point,
    ):
        """Add sheet/wall on location (only y is used) to the model. Requires setup of the Sheet/Wall and Locations first."""

    def add_pile(self, pile: Pile, location_top: Point, location_bottom: Point):
        """Add pile on location (only y is used) to the model. Requires setup of the Pile and Locations first."""

    def add_uniform_load(self, load: UniformLoad, stage=None):
        """Add uniform load."""

    def add_non_uniform_load(
        self,
        left: Union[None, SurchargeLoad],
        sheet: Union[
            None, Moment, HorizontalLineLoad, NormalForce, SoilDisplacement, Earthquake
        ],
        right: Union[None, SurchargeLoad],
        location: Point,
        stage=None,
    ):
        """Add all other loads. Only SoilDisplacement and Earthquake are valid for a Pile construction."""

    def add_support(
        self,
        left: Union[None, Anchor, Strut],
        sheet: Union[SpringSupport, RigidSupport],
        right: Union[None, Anchor, Strut],
        position: Point,
        stage=None,
    ):
        """Add support. Only Spring and Rigid supports are valid for a Pile construction."""

    @property
    def sheets(self):
        """Enables easy access to the sheets in the internal dict-like datastructure. Also enables edit/delete for individual Sheets."""

    @property
    def profiles(self):
        """Enables easy access to the profiles in the internal dict-like datastructure. Also enables edit/delete for individual Profiles."""
