from enum import Enum
from typing import List

from geolib.models import Model


class Material():
    pass


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class DFoundation():
    """Bearing Piles EC7-B, Shallow Foundations not supported in Viktor."""

    def __init__(self):
        pass

    def create_material(self, name: str, soiltype: Enum, gamma_unsat, gamma_sat, friction_angle, diameter_d50=0.2, color=Color):
        pass

    def _profile_layer(self, depth, material):
        pass

    def create_layer(self, layer: List[int], material:str, pl_line_top, pl_line_bottom):
        pass

    def create_profile(self, name: str, layers, measurements, x, y, phreatic_level):
        pass

    def create_pile_type(self, name: str, shape, type, sliplayer):
        pass

    def create_pile(self, type, location):
        pass

    def import_profile(self, CPT):
        pass
