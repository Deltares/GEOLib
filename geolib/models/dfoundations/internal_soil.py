import logging
from enum import IntEnum
from pathlib import Path

from pydantic import Field, StringConstraints
from typing_extensions import Annotated

from geolib.models.dseries_parser import DSeriesUnmappedNameProperties
from geolib.models.internal import Bool
from geolib.utils import csv_as_namedtuples

logger = logging.getLogger(__name__)


class SoilTypeNl(IntEnum):
    GRAVEL = 0
    SAND = 1
    LOAM = 2
    CLAY = 3
    PEAT = 4
    SANDYLOAM = 5
    TERTCLAY = 6
    CLAYEYSAND = 7


class MaxConeResistType(IntEnum):
    STANDARD = 0
    MANUAL = 1


class Soil(DSeriesUnmappedNameProperties):
    name: Annotated[str, StringConstraints(min_length=1, max_length=25)]
    soilcolor: int = 10871211  # could be color
    soilsoiltype: SoilTypeNl = SoilTypeNl.SAND
    soilgamdry: Annotated[float, Field(ge=0.0, le=100)] = 20.00
    soilgamwet: Annotated[float, Field(ge=0.0, le=100)] = 20.00
    soilinitialvoidratio: Annotated[float, Field(ge=0.0, le=20.0)] = 0.001001
    soildiameterd50: Annotated[float, Field(ge=0.0, le=1000.0)] = 0.20000
    soilminvoidratio: Annotated[float, Field(ge=0.0, le=1.0)] = 0.400
    soilmaxvoidratio: Annotated[float, Field(ge=0.0, le=1.0)] = 0.800
    soilcohesion: Annotated[float, Field(ge=0.0, le=1000.0)] = 30.00
    soilphi: Annotated[float, Field(ge=0.0, le=89.0)]
    soilcu: Annotated[float, Field(ge=0.0, le=1000.0)] = 0.00
    soilmaxconeresisttype: MaxConeResistType = MaxConeResistType.STANDARD
    soilmaxconeresist: Annotated[float, Field(ge=0.0, le=1000000.0)] = 0.00
    soilusetension: Bool = Bool.TRUE
    soilca: Annotated[float, Field(ge=0.0, le=10.0)] = 0.0040000
    soilccindex: Annotated[float, Field(ge=0.0, le=20.0)] = 0.1260000

    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            name = None
            for key, value in kwargs.items():
                fields = self.model_fields
                if key not in fields:
                    name = key + value
                    break
            if name:
                kwargs["name"] = name
                kwargs.pop(key)
        super().__init__(*args, **kwargs)

    @classmethod
    def default_soils(cls, model: str = "BEARING_PILES") -> list["Soil"]:
        currentfolder = Path(__file__).parent
        name = model.lower()
        filename = currentfolder / f"soil_csv/{name}_soils.csv"
        if not filename.exists():
            logger.warning(f"No default soils supported for {model}")
            return []

        soils = [
            Soil(
                name=name,
                soilsoiltype=soilsoiltype,
                soilgamdry=soilgamdry,
                soilgamwet=soilgamwet,
                soilphi=soilphi,
                soilcohesion=soilcohesion,
                soilcu=soilcu,
                soilccindex=soilccindex,
                soilca=soilca,
                soilinitialvoidratio=soilinitialvoidratio,
                soilcolor=soilcolor,
            )
            for name, soilsoiltype, soilgamdry, soilgamwet, soilphi, soilcohesion, soilcu, soilccindex, soilca, soilinitialvoidratio, soilcolor in csv_as_namedtuples(
                filename
            )
        ]
        return soils
