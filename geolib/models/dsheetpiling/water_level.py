from geolib.models import BaseDataClass

from .internal import WaterLevel as InternalWaterLevel
from .settings import DistributionType


class WaterLevel(BaseDataClass):
    name: str
    level: float
    distribution_type: DistributionType = DistributionType.NONE
    standard_deviation: float = 0.0
    rep_low_passive_CROW: float = 0.0
    delta_h_deci_low_passive_CROW: float = 0.0
    rep_high_passive_CROW: float = 0.0
    delta_h_deci_high_passive_CROW: float = 0.0
    average_low_passive_CROW: float = 0.0
    rep_high_active_CROW: float = 0.0
    delta_h_deci_high_active_CROW: float = 0.0
    average_high_active_CROW: float = 0.0

    def to_internal(self) -> InternalWaterLevel:
        return InternalWaterLevel(**self.model_dump(exclude_none=True))
