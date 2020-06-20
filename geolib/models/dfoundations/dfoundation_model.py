import logging
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Type, Union

from pydantic import BaseModel as DataModel
from pydantic import FilePath

from geolib.geometry import Point
from geolib.models import BaseModel, BaseModelStructure

from .dfoundations_parserprovider import DFoundationsParserProvider
from .internal import DFoundationsStructure
from .piles import Pile
from .serializer import DFoundationsInputSerializer


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


class Profile(DataModel):
    pass


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

    datastructure: BaseModelStructure = DFoundationsStructure()

    @property
    def parser_provider_type(self) -> Type[DFoundationsParserProvider]:
        return DFoundationsParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DFoundationsConsole/DFoundationsConsole.exe")

    def serialize(self, filename: FilePath):
        serializer = DFoundationsInputSerializer(ds=self.datastructure.dict())
        serializer.write(filename)
        self.filename = filename

    def execute(self, timeout: int = 30) -> Union[CompletedProcess, ValueError]:
        """Execute a Model and wait for `timeout` seconds."""
        if self.filename is None:
            raise ValueError("Set filename or serialize first!")
        if not self.filename.exists():
            logging.warning("Serializing before executing.")
            self.serialize(self.filename)
        return run(
            [str(self.meta.console_folder / self.console_path), "/b", str(self.filename)],
            timeout=timeout,
            cwd=self.filename.parent,
        )

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
