"""
For all geometries and locations we try to use
a single Point class. 

In 1D applications it's only used to 
specify, for example height, other fields left None.

For profiles used in 1D applications, see :class:`~geolib.soils.layers.ProfileLayer`

"""
from typing import Optional

from pydantic import BaseModel as DataModel


class Point(DataModel):
    """A single Point Class.

    """

    label: str = ""
    id: Optional[int]
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
