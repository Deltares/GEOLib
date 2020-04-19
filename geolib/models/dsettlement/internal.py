from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel as DataClass

from geolib.models.base_model import BaseModelStructure
from geolib.models.dseries_parser import DSeriesStructure, DSeriesKeyValueSubStructure, DSeriesNameKeyValueSubStructure, DSeriesListSubStructure, DSeriesNoParseSubStructure

DataClass.Config.arbitrary_types_allowed = True


class Soil(DSeriesNoParseSubStructure):
    name: str

class SoilCollection(DSeriesListSubStructure):
    soil: Union[List[Soil], List[str]]

class Version(DSeriesKeyValueSubStructure):
    soil: int = 1005
    geometry: int = 1000
    d__settlement: int = 1007


class DSettlementStructure(DSeriesStructure):
    version: Version
    soil_collection: Union[SoilCollection, str]
    geometry_data: str
    run_identification: str
    model: str
    verticals: str
    water: str
    non__uniform_loads: str
    water_loads: str
    other_loads: str
    calculation_options: str
    residual_times: str
    filter_band_width: str
    pore_pressure_meters: str
    non__uniform_loads_pore_pressures: str
    other_loads_pore_pressures: str
    calculation_options_pore_pressures: str
    vertical_drain: str
    probabilistic_data: str
    probabilistic_defaults: str
    fit_options: str
    fit_calculation: str
    eps: str
    fit: str
