from pathlib import Path

from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):
    """Holds all metadata found in the header of model files.

    Could be specified by default or in advance to make
    model generation easier.

    Also can read these settings automatically from a 
    'geolib.env' file in the working directory, or give
    as '_env_file' parameter.
    """

    gl_username: str = "test"
    gl_password: str = "test"
    console_folder: DirectoryPath = Path(".")
    calculation_folder: Path = Path("tests/test_output/calculations")
    nprocesses: int = 1

    class Config:
        env_file = "geolib.env"
