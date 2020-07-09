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
from geolib import __version__ as version
from pydantic import BaseSettings, AnyHttpUrl, DirectoryPath
from pathlib import Path

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

    endpoint: AnyHttpUrl = "http://localhost:8000/"  # For remote execution
    console_folder: DirectoryPath = Path(".")

    class Config:
        env_file = "geolib.env"
