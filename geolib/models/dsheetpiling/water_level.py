from typing import Optional
from pydantic import BaseModel as DataModel
from .settings import DistributionType
from .internal import WaterLevel as InternalWaterLevel


class WaterLevel(DataModel):
    name: str
    level: float
    distribution_type: Optional[DistributionType] = None
    standard_deviation: Optional[float] = None

    def to_internal(self) -> InternalWaterLevel:
        return InternalWaterLevel(**self.dict(exclude_none=True))
