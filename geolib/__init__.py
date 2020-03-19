"""
GEOLIB Library
"""

__version__ = "0.1.0"

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

from . import utils

logging.getLogger(__name__).addHandler(NullHandler())
