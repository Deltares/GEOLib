.. _setup:

Setup
=====

GEOLib should work out of the box as a Python module. However, it needs 
setting up of a configuration for calculations to work. The configuration
is also used for the metadata used in the model input files, such as your
company name.

You can specify the configuration in two ways. One is to create a geolib.env
file in your working directory. The second is to specify environment variables.

The *geolib.env* file is a simple text file, which can contain any number of parameters, see the two methods below
to see how you can use this file to configure the path to the console applications.

Setting the console paths per application
-----------------------------------------

In the *geolib.env* file, you can set the paths to the console applications, for example::

    DSTABILITY_CONSOLE_PATH="C:\\Program Files (x86)\\Deltares\\D-GEO Suite\\D-Stability 2023.01\\bin\\D-Stability Console.exe"
    DGEOFLOW_CONSOLE_PATH="C:\\Program Files\\Deltares\\D-GEO Suite\\D-Geo Flow 2023.01\\bin\\D-GeoFlow Console.exe"
    DSHEETPILING_CONSOLE_PATH="C:\\Program Files (x86)\\Deltares\\D-Sheet Piling 23.1.1\\DSheetPiling.exe"
    DFOUNDATIONS_CONSOLE_PATH="C:\\Program Files (x86)\\Deltares\\D-Foundations 23.1.1\\DFoundations.exe"
    DSETTLEMENT_CONSOLE_PATH="C:\\Program Files (x86)\\Deltares\\D-Settlement 23.1.1\\DSettlement.exe"

Settings the console path using the common CONSOLE_FOLDER variable
------------------------------------------------------------------

In the *geolib.env* file, you can set the CONSOLE_FOLDER variable to a folder that should contain all console applications in a single location, for example::

    CONSOLE_FOLDER="C:\\Users\\You\\Documents\\GEOLibConsoles"  # path has to exist!

This configuration variable points to the folder in which the consoles are placed (each in its own subfolder).

Note that the *CONSOLE_FOLDER* variable has to point to an existing path,
otherwise GEOLib will not start. The executables are expected in the following locations::

- *CONSOLE_FOLDER*/"DFoundations/DFoundations.exe"
- *CONSOLE_FOLDER*/"DSettlement/DSettlement.exe"
- *CONSOLE_FOLDER*/"DSheetPiling/DSheetPiling.exe"
- *CONSOLE_FOLDER*/"DStabilityConsole/D-Stability Console.exe"
- *CONSOLE_FOLDER*/"DGeoFlowConsole/DGeoFlow Console.exe"

It can also be set by a **CONSOLE_FOLDER** environment variable. The environment variable will
overrule the .env file, which in its turn, overrides the defaults set in Python.

Default settings
----------------

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

    # For ignoring extra fields that could come with newer/older versions
    # of input/output fields. We don't support any other value than "forbid"!
    extra_fields = "forbid"  # can be "ignore", "allow" or "forbid"

Dynamic settings
----------------

If you don't wish to use *geolib.env* files or wish to override them, you can change the final settings
in Python itself, using the *meta* methods on a model. Note that changing the properties for one model changes the global settings, so it applies to all instances of a model.
For example, to override the *console_folder*::

    >>> import geolib as gl
    >>> from pathlib import Path
    >>> dm = gl.models.DSettlementModel()
    >>> dm.get_meta_property("company")
    Deltares
    >>> dm.set_meta_property("console_folder", Path("other_location"))

Logging
-------

GEOLib makes use of the built-in logging library. If you need to control the level of logging, you can do the following::

    >>> import logging
    >>> logging.getLogger("geolib").setLevel(logging.ERROR)

In this example, logging has been set to the ERROR level.
Note that for setting lower levels than the default warning level, you have to configure your own root logger as well.

Consoles
--------

You can download the consoles `here <https://download.deltares.nl/geolib>`_, 
with the given password. You also need to download the license manager
from `here <https://download.deltares.nl/en/license-manager>`_ and install the given license using the "Add License File" program.

Console usage
-------------

If you wish to use these consoles without Python on the command line, 
note that all except for the D-Stability and D-Geo Flow consoles require the "/b" flag, i.e.::

    $ DFoundations/DFoundations.exe /b "folder_or_file"

Note that you can only execute these files from the commandline, double clicking on them in Explorer won't work.

Version differences
-------------------

Each D-Serie / D-GEO Suite release can slightly change the structure of the input files. New fields are added and some fields are changed or deleted.

GEOLib only supports the files used by the D-Serie / D-GEO Suite consoles and thus the consoles specific version number.
At the moment that version number is:

* D-Settlement **23.2**
* D-Foundations **23.1**
* D-SheetPiling **24.1**
* D-Stability **2024.01**
* D-Geo Flow **2024.01**

Loading files generated by either older or newer versions isn't guaranteed to work and will likely result in an error message such as ValidationError(extra fields not permitted).
You could disable this by changing the extra_fields setting described above, but we don't support this.

You can however easily fix this by resaving the file with the correct version of the console or GUI:

* Open one file at a time with the correct D-Serie / D-GEO Suite GUI version and save it again.
* Run the correct D-Serie / D-GEO Suite console on a file or complete folder of files. This will generate output files, but also save overwrite the input files in the correct version format.
