.. _geomdev:

Geometry
========================

1D Geometry
-------------------------

.. automodule:: geolib.geometry.one
    :members:
    :undoc-members:

2D Geometry
-------------------------

Two-dimensional geometry is handled differently by the two programs
using this geometry, namely D-Settlement and D-Stability.

In our API we use the D-Settlement approach::
    - add_point(Point) -> point_id:int
    - add_layer(List[point_id]) -> layer_id:int

Where we use references to previously added points to ensure
topological consistency. This is why we have not introduced a LineString
object as of yet.

Note however that for D-Settlement this List of points should
form a LineString (ordered in X), while for D-Stability they should 
form an ordered Ring (Polygon).
