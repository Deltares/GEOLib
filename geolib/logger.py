import logging
from logging import NullHandler

logger = logging.getLogger("geolib")
# Set default logging handler to avoid "No handler found" warnings.
logger.addHandler(NullHandler())
