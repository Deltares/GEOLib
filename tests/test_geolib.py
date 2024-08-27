import pytest

from geolib import __version__

from .context import geolib

version = "2.4.1"


@pytest.mark.systemtest
def test_version():
    assert __version__ == version
