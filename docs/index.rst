.. geolib documentation master file, created by
   sphinx-quickstart on Mon Mar  2 15:19:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GEOLib's documentation!
==================================

GEOLib is a Python package to generate input, execute and parse output for several D-Serie numerical models.
Release v\ |version|.

-------------------

**Behold, the power of GEOLib**::

    >>> import geolib as gl
    >>> from pathlib import Path
    >>> m = gl.DSettlementModel()
    >>> m.parse(Path("test.sli"))
    >>> m.execute()
    >>> m.output.dict()
    {'verticals_count': 1, 'vertical': [{'id': 1, 'x': 0.0, 'z': 0.0, 'time__settlement_per_load': {'timesettlementperload': [[0.0, 0.0, 0.0], ...


The User Guide
--------------

This part of the documentation, which is mostly prose, begins with some
background information about GEOLib, then focuses on step-by-step
instructions for getting the most out of GEOLib.

.. toctree::
   :maxdepth: 3

   user/intro
   user/install
   user/setup
   user/server

The Tutorials
-------------

This part of the documentation, which is all prose, gives some examples
of using GEOLib.

.. toctree::
   :maxdepth: 3

   community/tutorial


The API Documentation / Guide
-----------------------------

If you are looking for information on a specific function, class, or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 3

   dev/api


The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you. It includes in depth guide how to go about extending GEOLib.

.. toctree::
   :maxdepth: 3

   dev/extend
   dev/todo


There are no more guides. You are now guideless.
Good luck.

Changelog
---------

.. toctree::
   :maxdepth: 3

   changelog
