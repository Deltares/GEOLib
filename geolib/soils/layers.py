"""
Profile and Layer classes which are used by both D-Foundations and DSheetPiling.
D-Foundations often requires more parameters, which are unused for DSheetPiling.

"""

from typing import List

from geolib.geometry.one import Point
from geolib.models import BaseDataClass
from geolib.soils import Soil


class CPT(BaseDataClass):
    """Internal Placeholder CPT measurements as used in D-Foundations/D-Sheetpiling.

    It is here because input files can contain CPTs coupled to a Profile.

    .. todo::
        Add Friction and other parameters?
    """

    z: List[float]
    qc: List[float]


class CPTRule(BaseDataClass):
    """Placeholder class for CPT interpretation options."""


class ProfileLayer(BaseDataClass):
    """Layer in a Profile. Note that we add the vertical location of
    the layer with a Point class.

    .. todo::
        * Will the ocr be added to the Soil class?
        * Decouple pore_pressures into special Class/Line
    """

    top: Point
    material: Soil
    pore_pressure_top: float  # absolute (needs calculation to ad.)
    pore_pressure_bottom: float  # absolute (needs calculation to ad.)
    ocr: float
    reduction_cone_resistance: float


class Profile(BaseDataClass):
    """D-Foundations Profile.

    .. todo::
        * Determine extra fields related to Excavations

    """

    label: str
    layers: List[ProfileLayer]
    phreatic_level: float
    pile_tip_level: float
    overconsolidation_ratio: float
    top_positive_skin_friction: float
    bottom_positive_skin_friction: float
    expected_ground_level_settlement: float
    min_layer_thickness: float
    cpt: CPT
    cpt_rule: CPTRule
