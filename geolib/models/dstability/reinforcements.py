"""
This module handles the three types of reinforcements in DStability.
"""

from pydantic import BaseModel


class DStabilityReinforcement(BaseModel):
    """Base Class for Reinforcements."""

    label: str


class Nail(DStabilityReinforcement):
    """Inherits :class:`~geolib.models.dstability.reinforcements.DStabilityReinforcement`."""

    length: float


class ForbiddenLine(DStabilityReinforcement):
    """Inherits :class:`~geolib.models.dstability.reinforcements.DStabilityReinforcement`. Needs to be further defined."""

    pass


class GeoTextile(DStabilityReinforcement):
    """Inherits :class:`~geolib.models.dstability.reinforcements.DStabilityReinforcement`."""

    effective_tensile_strength: float
    reduction_area: float
