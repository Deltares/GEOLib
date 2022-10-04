import pytest

from geolib import __version__

from .context import geolib

version = "0.1.9"


@pytest.mark.systemtest
def test_version():
    assert __version__ == version
