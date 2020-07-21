from typing import Optional
from pydantic import BaseModel as DataModel
from .settings import DistributionType
from .internal import WaterLevel as InternalWaterLevel


class WaterLevel(DataModel):
    name: str
    level: float
    distribution_type: DistributionType = DistributionType.NONE
    standard_deviation: float = 0.0

    def to_internal(self) -> InternalWaterLevel:
        return InternalWaterLevel(**self.dict(exclude_none=True))
