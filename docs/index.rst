.. geolib documentation master file, created by
   sphinx-quickstart on Mon Mar  2 15:19:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to geolib's documentation!
==================================

Geolib is a Python package to generate input, execute and parse output for several D-Serie numerical models.
Release v\ |version|.

-------------------

**Behold, the power of Geolib**::

    >>> import geolib as gl
    >>> m = gl.DSettlement(fn="data/test.sli")
    DSettlement 2D Model with XX options
    >>> m.update_metadata(project="test")
    >>> m.execute()
    Succesfully executed model in 3 seconds
    >>> r.parse_result()
    {"settlements": [1.25, 2.55], "verticals": [1.0, 2.0], ..}


The User Guide
--------------

This part of the documentation, which is mostly prose, begins with some
background information about Geolib, then focuses on step-by-step
instructions for getting the most out of Geolib.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/soils
   user/geometry


The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 3

   dev/todo

There are no more guides. You are now guideless.
Good luck.
