.. _dstability:

D-Stability
========================

D-Stability model
-----------------

.. automodule:: geolib.models.dstability.dstability_model
.. automodule:: geolib.models.dstability.analysis



Loads
----------------

.. automodule:: geolib.models.dstability.loads



Reinforcements
-------------------------

.. automodule:: geolib.models.dstability.reinforcements


States
------

.. automodule:: geolib.models.dstability.states


Geometry
--------

Add layer
_________
For the geometry it is import to set the geometry points in the correct order. I.e. per polygon, set the points in
clockwise or anticlockwise  order. Furthermore it is import to add all points which are part or touch a
certain polygon. This procedure is automatically done when the user creates a geometry via the user interface. However
when the user wants to create a geometry via Geolib, it is important to specify all points for each layer. An example
is illustrated below.

The following valid code will produce a correct geometry, note that the clay layer is a rectangular layer, but still
requires 6 geometry points. This is because the dike layer touches the clay layer at two points. If the clay layer is
only generated the 4 corner points, a valid geometry is generated, however unexpected results can occur.

.. code-block:: python

    import geolib
    from geolib.geometry import Point
    from pathlib import Path

    ds = geolib.DStabilityModel()

    clay_points = [Point(x=-50, z=-10),
                   Point(x=-50, z=-5),
                   Point(x=0, z=-5),
                   Point(x=20, z=-5),
                   Point(x=50, z=-5),
                   Point(x=50, z=-10)]

    dike_points = [Point(x=5, z=2),
                   Point(x=15, z=2),
                   Point(x=20, z=-5),
                   Point(x=0, z=-5)]

    soil_clay= geolib.soils.Soil()
    soil_dike = geolib.soils.Soil()
    soil_clay.code = 'clay'
    soil_dike.code = 'dike'

    ds.add_soil(soil_clay)
    ds.add_soil(soil_dike)

    ds.add_layer(clay_points, soil_clay.code)
    ds.add_layer(dike_points, soil_dike.code)

    ds.filename = Path('geometry_example.stix')
    ds.serialize(ds.filename)

..  image:: /figures/dstability/geometry_example.png
    :width: 800

Output
------

.. autoclass:: geolib.models.dstability.internal.UpliftVanResult
.. autoclass:: geolib.models.dstability.internal.UpliftVanParticleSwarmResult
.. autoclass:: geolib.models.dstability.internal.UpliftVanReliabilityResult
.. autoclass:: geolib.models.dstability.internal.SpencerGeneticAlgorithmResult
.. autoclass:: geolib.models.dstability.internal.SpencerReliabilityResult
.. autoclass:: geolib.models.dstability.internal.SpencerResult
.. autoclass:: geolib.models.dstability.internal.BishopBruteForceResult
.. autoclass:: geolib.models.dstability.internal.BishopReliabilityResult
.. autoclass:: geolib.models.dstability.internal.BishopResult

.. autoclass:: geolib.models.dstability.internal.PersistableSoilContribution
.. autoclass:: geolib.models.dstability.internal.PersistableStageContribution
.. autoclass:: geolib.models.dstability.internal.PersistableSpencerSlice
.. autoclass:: geolib.models.dstability.internal.PersistableStateLinePointContribution
.. autoclass:: geolib.models.dstability.internal.PersistableStatePointContribution
.. autoclass:: geolib.models.dstability.internal.PersistablePoint
.. autoclass:: geolib.models.dstability.internal.PersistableSlice

.. autoclass:: geolib.models.dstability.internal.SpencerSlipPlaneResult
.. autoclass:: geolib.models.dstability.internal.UpliftVanSlipCircleResult
.. autoclass:: geolib.models.dstability.internal.BishopSlipCircleResult
