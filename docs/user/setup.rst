.. _setup:

Setup
=====

GEOLib should work out of the box as a Python module. However, it needs 
setting up of a configuration for calculations to work. The configuration
is also used for the metadata used in the model input files, such as your
company name.

You can specify the configuration in two ways. One is to create a geolib.env
file in your working directory. The second is to specify environment variables.

The *geolib.env* file is a simple text file, which can contain any number of parameters::

    CONSOLE_FOLDER="tests"  # path has to exist!

This configuration variable points to the folder in which the consoles are placed (each in its own subfolder).
It can also be set by a CONSOLE_FOLDER environment variable. The enviroment variable will
overrule the .env file, which in its turn, overrides the defaults set in Python.

The defaults are as follows::

    company: str = ""
    analyst: str = ""
    startdate: datetime = datetime.now()
    project: str = ""
    remarks: str = f"Created by GEOLib {version}"
    console_folder: DirectoryPath = Path(".")

    # Used for remote calculation client side
    endpoint: AnyHttpUrl = "http://localhost:8000/"

    # User for both client/server
    gl_username: str = "test"
    gl_password: str = "test"

    # Used by server
    calculation_folder: Path = Path("tests/test_output/calculations")
    nprocesses: int = 1

Note that the *console_folder* variable has to point to an existing path,
otherwise GEOLib will not start. The executables are expected in the following locations
in the *console_folder*.

- "DFoundationsConsole/DFoundationsConsole.exe"
- "DSettlementConsole/DSettlementConsole.exe"
- "DSheetPilingConsole/DSheetPilingConsole.exe"
- "DStabilityConsole/D-GEO Suite Stability GEOLIB Console.exe"
