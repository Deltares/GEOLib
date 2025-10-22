from geolib.models import BaseDataClass

from .internal import WaterLevel as InternalWaterLevel
from .settings import DistributionType


class WaterLevel(BaseDataClass):
    name: str
    level: float
    distribution_type: DistributionType = DistributionType.NONE
    standard_deviation: float = 0.0
    delta_h_deci_CROW: float = 0.0

    def to_internal(self) -> InternalWaterLevel:
        return InternalWaterLevel(**self.model_dump(exclude_none=True))
