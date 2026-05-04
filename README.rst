GEOLib
=============================

GEOLib is a Python package to generate, execute and parse several D-Serie and D-GEO Suite numerical models.

Installation
------------

Install GEOLib with:

.. code-block:: bash

    $ pip install d-geolib

Configure your environment using the instructions on our `Setup <https://deltares.github.io/GEOLib/latest/user/setup.html>`_ page.
You may get the console executables from the Deltares download portal, or in the case of the D-GEO Suite, you may copy the contents of the installation 'bin' directory to your console folder.

Running the source code
-----------------------

If you want to make changes to GEOLib you can run the source code from GitHub directly on your local machine, 
please follow the instructions below on how to set up your development environment using Pixi.

You do not need to follow these instructions if you want to use the GEOLib package in your project.

Requirements
------------

To install the required dependencies to run GEOLib code, use `Pixi <https://pixi.sh>`_:

.. code-block:: bash

    $ pixi install

This will create a reproducible development environment with all dependencies.


Testing & Development
---------------------

Make sure all dependencies are installed:

.. code-block:: bash

    $ pixi install

In order to run the testcode, from the root of the repository, run:

.. code-block:: bash

    $ pixi run pytest

Running mypy for type checking:

.. code-block:: bash

    $ pixi run mypy --config-file pyproject.toml geolib

Running standard linters:

.. code-block:: bash

    $ pixi run isort .
    $ pixi run black .


Documentation
-------------

In order to build the documentation, from the root of the repository, run:

.. code-block:: bash

    $ cd docs
    $ pixi run sphinx . build -b html -c .


The documentation is now in the `build` subfolder, where you can open 
the `index.html` in your browser.

Build wheel
-----------

To build a distributable wheel package using hatchling:

.. code-block:: bash

    $ pip install build
    $ python -m build

The distributable packages are now built in the `dist` subfolder.

Update lock files
-----------------------

To update dependencies and lock files, use Pixi for local development:

.. code-block:: bash

    $ pixi install

CI uses uv for multi-version testing and will regenerate `uv.lock` automatically.

Code linter
-----------------------

In order to run code cleanup/linter use the following commands:

.. code-block:: bash

    $ pixi run isort .
    $ pixi run black .