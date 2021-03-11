"""
All D-Serie models store some metadata in the input files. These include
projectnames, dates and times, remarks etc. All of these options are
available via the `Metadata` class.

The `Metadata` class can also hold other properties for your project
such as an compute endpoint.

.. todo::
    Make a mapping between the possible metadata options and names for each model.

"""
from datetime import datetime
from pathlib import Path

from pydantic import AnyHttpUrl, BaseSettings, DirectoryPath

from geolib import __version__ as version

CONSOLE_RUN_BATCH_FLAG = "/b"


class MetaData(BaseSettings):
    """Holds all metadata found in the header of model files.

    Could be specified by default or in advance to make
    model generation easier.

    Also can read these settings automatically from a
    'geolib.env' file in the working directory, or give
    as '_env_file' parameter.
    """

    company: str = ""
    analyst: str = ""
    startdate: datetime = datetime.now()
    project: str = ""
    remarks: str = f"Created by GEOLib {version}"

    # For remote execution
    endpoint: AnyHttpUrl = "http://localhost:8000/"
    gl_username: str = "test"
    gl_password: str = "test"

    # For calculations
    console_folder: DirectoryPath = Path(".")
    timeout: int = 10 * 60  # in seconds, so 10 minutes

    # For multiple calculations
    calculation_folder: Path = Path("tests/test_output/calculations")
    nprocesses: int = 1

    # For ignoring extra fields that could come with newer/older versions
    # of input/output fields. We don't support any other value than "forbid"!
    extra_fields = "forbid"  # can be "ignore", "allow" or "forbid"

    class Config:
        env_file = "geolib.env"
