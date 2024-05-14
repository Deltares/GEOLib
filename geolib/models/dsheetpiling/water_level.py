from typing import Optional

from geolib._compat import IS_PYDANTIC_V2
from geolib.models import BaseDataClass

from .internal import WaterLevel as InternalWaterLevel
from .settings import DistributionType


class WaterLevel(BaseDataClass):
    name: str
    level: float
    distribution_type: DistributionType = DistributionType.NONE
    standard_deviation: float = 0.0

    def to_internal(self) -> InternalWaterLevel:
        if IS_PYDANTIC_V2:
            return InternalWaterLevel(**self.model_dump(exclude_none=True))
        else:
            return InternalWaterLevel(**self.dict(exclude_none=True))
