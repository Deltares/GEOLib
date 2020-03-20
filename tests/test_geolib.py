from geolib import __version__

from .context import geolib
import pytest


def test_version():
    assert __version__ == "0.1.0"
