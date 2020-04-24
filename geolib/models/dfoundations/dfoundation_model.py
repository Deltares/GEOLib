from enum import Enum
from typing import List

from pydantic import BaseModel as DataModel

from geolib.geometry import Point
from geolib.models import BaseModel
from geolib.soils import Soil
from geolib.soils.layers import Profile

from .piles import Pile


class ConstructionSequence(Enum):
    CPT_EXCAVATION_INSTALL = 1
    # ...


class CalculationType(Enum):
    DESIGN_CALCULATION = 0
    INDICATION_BEARING_CAPACITY = 2
    # ...


class ModelType(DataModel):
    calculation_type: CalculationType
    rigid: bool
    unit_weight_water: float = 5.0
    # ...


class BearingPiles(ModelType):
    pass


class TensionPiles(ModelType):
    pass


class DFoundationsModel(BaseModel):
    """D-Foundations enables the user to calculate piles (bearing and tension) 
    and shallow foundation in accordance with the Dutch (and Belgian) standards.

    This model can read, modify and create
    *.foi files, read *.fod and *.err files.
    """

    @property
    def parser_provider_type(self):
        raise NotImplementedError("Not implemented yet.")

    def serialize(self):
        """TODO: To implement."""

    def set_model(self, model: ModelType, sequence: ConstructionSequence, **kwargs):
        """(Re)Set ModelType (Bearing/Tension)(NL/BE) and ConstructionSequence for model."""

    def add_profile(self, profile: Profile, location: Point):
        """Add profile on location to the model. Requires setup of the Profile and Location first."""

    def add_pile(self, pile: Pile, location: Point):
        """Add pile on location to the model. Requires setup of the Pile and Location first."""

    @property
    def piles(self):
        """Enables easy access to the piles in the internal dict-like datastructure. Also enables edit/delete for individual Piles."""

    @property
    def profiles(self):
        """Enables easy access to the profiles in the internal dict-like datastructure. Also enables edit/delete for individual Piles."""
