GEOLib
=============================

GEOLib is a Python package to generate, execute and parse several D-Serie numerical models.

Requirements
------------

To install the required dependencies to run GEOLib code, run:

.. code-block:: bash

    $ pip install -r requirements

Or, when having poetry installed (you should):

.. code-block:: bash

    $ poetry install


Testing
-------

In order to run the testcode, from the root of the repository, run:

.. code-block:: bash

    $ pytest

or, in case of using Poetry

.. code-block:: bash

    $ poetry run pytest


Documentation
-------------

In order to run the documentation, from the root of the repository, run:

.. code-block:: bash

    $ cd docs
    $ sphinx-build . build -b html -c .


The documentation is now in the `build` subfolder, where you can open 
the `index.html` in your browser.
