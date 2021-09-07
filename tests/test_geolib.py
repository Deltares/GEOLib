import pytest

from geolib import __version__

from .context import geolib


@pytest.mark.systemtest
def test_version():
    assert __version__ == "0.1.6"
