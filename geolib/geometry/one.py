"""
For all geometries and locations we try to use
a single Point class. 

In 1D applications it's only used to 
specify, for example height, other fields left None.

For profiles used in 1D applications, see :class:`~geolib.soils.layers.ProfileLayer`

"""
from math import isclose
from typing import Optional

from geolib.models import BaseDataClass

NODATA = -999.0  # TODO why is this implemented instead of None?


class Point(BaseDataClass):
    """A single Point Class."""

    label: Optional[str] = ""
    id: Optional[int]
    x: float = NODATA
    y: float = NODATA
    z: float = NODATA
    tolerance: float = 1e-4

    def __eq__(self, other):

        if isinstance(other, Point):
            return (
                isclose(self.x, other.x, abs_tol=self.tolerance)
                and isclose(self.y, other.y, abs_tol=self.tolerance)
                and isclose(self.z, other.z, abs_tol=self.tolerance)
            )
        else:
            return NotImplemented
