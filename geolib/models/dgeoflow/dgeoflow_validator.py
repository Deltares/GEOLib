import logging

from geolib.models.validators import BaseValidator

logger = logging.getLogger(__name__)


class DGeoFlowValidator(BaseValidator):
    """Validator for DGeoFlow structure.

    Has access to self.ds from parent class.
    Will run all is_valid_ functions to check for validity."""
