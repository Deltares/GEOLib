.. _soilsdev:

Soils
========================


Soil Libraries
-------------------------
It is possible to import various input files which will automatically generate `Soil` objects from them.
Several pre-existing soil materials as used in D-Foundations based on the NEN 9997-1 norm are defined here as well.
The Belgian Annex Soils will be added later.

Using Soil Library::

    >>> import geolib as gl
    >>> dir(gl.soils)
    <Soil A with code a>, <Soil B with code b>


CPT interpretation
-------------------------
This package won't interpret CPTs. This will follow in the GEOLib+ package.
There is a :class:`geolib.soils.layers.CPT` class however, to load from D-Foundations and DSheetPiling input files.

The Soil Class
-------------------------

.. automodule:: geolib.soils.soil
.. autoclass:: geolib.soils.soil_utils.Color
.. autoclass:: geolib.models.dstability.internal.ShearStrengthModelTypePhreaticLevel

.. commented out until unified
.. 1D Profiles and layers
.. ----------------------

.. .. automodule:: geolib.soils.layers
..     :members:
..     :undoc-members:
