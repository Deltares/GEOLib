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
such as json [#f1]_ could theoretically be produced too and are expected to be used
in eventual webservices.

All other functionality, such as conversion from common formats, any calculations
such as interpolation or interpretations will not be part of this package and instead
be implemented in the GEOLib+ package.

Architecture
------------

All exposed models are subclassed from a :class:`~geolib.models.base_model.BaseModel` that
defines the generic functions, such as parsing, metadata, executing etc. The individual
subclasses then define model specific functions, such as :meth:`~geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel.add_sheet`.



.. rubric:: Footnotes

.. [#f1] Although these would be technically invalid as JSON doesn't support NaNs.
