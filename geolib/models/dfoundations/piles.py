"""Pile Library for D-Foundations.

.. todo::
    Fill Pile Library, we wait for third-party code.
"""

from pydantic import BaseModel as DataModel


class Pile(DataModel):
    """Base Class for Piles."""


class HShapedPile(Pile):
    """Inherits :class:`~geolib.models.dfoundations.piles.Pile`."""


class DrivenBasePile(Pile):
    """Inherits :class:`~geolib.models.dfoundations.piles.Pile`."""


class HollowPile(Pile):
    """Inherits :class:`~geolib.models.dfoundations.piles.Pile`."""
