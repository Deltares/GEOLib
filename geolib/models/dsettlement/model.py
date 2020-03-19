from enum import Enum
from typing import List

from geolib.models import Model


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class DSettlement(Model):
    """
    DSettlement is a dedicated tool for predicting soil settlements by external loading.
    
    This model can read, modify and create *.sli files, read *.sld and *.err files.
    """

    def __init__(self):
        pass

    # 1.2.1 Soil profile
    # To create multiple layers
    def create_points(self, x:float, y:float):
        """Summary line.

        Extended description of function.

        Args:
            arg1: Description of arg1
            arg2: Description of arg2

        Returns:
            Description of return value

        """
        pass

    def points(self):
        pass

    def create_pl_line(self, points: List[int], is_phreatic=False):
        pass

    def create_layer(self, points: List[int], material:str, pl_line_top, pl_line_bottom):
        pass

    def update_geometry(self):
        pass

    def set_limits(sefl):
        pass

    # To create soil properties
    def create_soil(self):
        pass

    # To create verticals
    def create_vertical(self, xcoord: float, zcoord):
        """At least one vertical is required to calculate."""
        pass

    # 1.2.2 Loads
    def create_uniform_load(self, name:str, time:int, unit_weight:float, height:float, y_application:float):
        """VI. Create a uniform load with the given name and properties.
        
        TODO Get bla.
        """
        pass

    def create_non_uniform_load(self):
        pass

    def set_calculation_times(self, time:int):
        """VI. (Re)set calculation time(s)."""
        pass

    # 1.2.3 Models
    def set_model(constitutive_model, consolidation_model):
        pass

    # Added
    def is_valid(geometry=True, integrity=True):
        pass
