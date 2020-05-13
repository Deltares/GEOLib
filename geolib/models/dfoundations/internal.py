import logging
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel as DataClass

from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.dseries_parser import (
    ComplexVerticalSubstructure,
    DSerieListStructure,
    DSerieMatrixStructure,
    DSerieOldTableStructure,
    DSerieRepeatedTableStructure,
    DSerieSingleStructure,
    DSeriesKeyValueSubStructure,
    DSeriesListSubStructure,
    DSeriesListTreeStructureCollection,
    DSeriesMatrixTreeStructure,
    DSeriesNameKeyValueSubStructure,
    DSeriesNoParseSubStructure,
    DSeriesSinglePropertyGroup,
    DSeriesStructure,
    DSeriesTreeStructure,
    DSerieTableStructure,
)

DataClass.Config.arbitrary_types_allowed = True


class Layer(DSeriesTreeStructure):
    name: str
    material: int
    top_level: float
    excess_pore_pressure_top: float
    excess_pore_pressure_bottom: float
    ocr_value: float
    reduction_core_resistance: float


class Profile(DSeriesTreeStructure):
    name: str
    matching_cpt: int
    x_coordinate: float
    y_coordinate: float
    phreatic_level: float
    pile_tip_level: float
    overconsolidation_ratio: float
    top_of_positive_skin_friction: float
    bottom_of_negative_skin_friction: float
    expected_ground_level_settlement: float
    placement_depth_of_foundation: float
    concentration_value_frohlich: float
    top_tension_zone: float
    reduction_of_core_resistance: float
    excavation_level: float
    excavation_width_infinite: bool
    excavation_length_infinite: bool
    distance_edge_pile_to_excavation_boundary: float
    layers: List[Layer] = []


class Profiles(DSeriesListTreeStructureCollection):
    profiles: List[Profile] = []


class DFoundationsInputStructure(DSeriesStructure):
    """Representation of complete .foi file."""

    version: str = ""
    version_externals: str = ""
    model: str = ""
    soil_collection: str = ""
    run_identification: str = ""
    cpt_list: str = ""
    profiles: str = ""
    slopes: str = ""
    types___bearing_piles: str = ""
    types___bearing_piles_belgian: str = ""
    types___tension_piles_cur: str = ""
    types___shallow_foundations: str = ""
    loads: str = ""
    positions___bearing_piles: str = ""
    positions___bearing_piles_belgian: str = ""
    positions___tension_piles_cur: str = ""
    positions___shallow_foundations: str = ""
    calculation_options: str = ""
    calculationtype: str = ""
    preliminary_design: str = ""
    de_beer: str = ""
    location_map: str = ""


class DFoundationsOutputStructure(DSeriesStructure):
    results_at_cpt_test_level: str
    verification_results: str
    footnote_warnings: str


class DFoundationsStructure(DSeriesStructure):
    input_data: DFoundationsInputStructure = DFoundationsInputStructure()
    dumpfile_output: Optional[DFoundationsOutputStructure]
    calculation_warnings: Optional[str]


class DFoundationsDumpStructure(DSeriesStructure):
    dumpfile: DFoundationsStructure = DFoundationsStructure()
