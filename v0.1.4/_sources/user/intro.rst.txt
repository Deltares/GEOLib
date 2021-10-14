.. _introduction:

Introduction
============

Philosophy
----------

GEOLib is a Python package that wraps four D-Serie models; D-Stability, 
D-Settlement, D-SheetPiling and D-Foundations. It does this on a file 
based level, by producing the required input files and reading the output files, 
calling the numerical model as a subprocess in between.

It is therefore mainly a data transformation package, parsing files 
such as \*.sli (in the case of D-Settlement) to a dict-like format in Python, 
and serialize from this internal format back to \*.sli again. Other formats
such as json [#f1]_ are easily derived and are used in the webservices.

All other functionality, such as conversion from common formats, any calculations
such as interpolation or interpretations will not be part of this package and instead
be implemented in the GEOLib+ package.

Architecture
------------

All exposed models are subclassed from a :class:`~geolib.models.base_model.BaseModel` that
defines the generic functions, such as parsing, metadata, executing etc. The individual
subclasses then define model specific functions, such as :meth:`~geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel.add_head_line`.

Each model has a datastructure attribute that is a close representation of the input (or output) structure.
This structure is automatically type validated and can easily be serialized by using *.dict()* or *.json()*.
While it is possible to edit this datastructure directly, is only meant to be manipulated using the interface 
on the model level, integrity can't otherwise be guaranteed.

Requirements
------------

For translating the requirements on the publicwiki from blocks like [SOIL] to this package
we advise to read the tutorials and make use of the search function. The tutorials
cover all that's needed to create a valid, calculatable model for each supported D-Serie product.
The search function combined with the :ref:`api` documentation covers the remaining parts.


.. rubric:: Footnotes

.. [#f1] Although these would be technically invalid as JSON doesn't support NaNs.
