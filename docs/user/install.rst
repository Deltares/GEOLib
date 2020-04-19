.. _install:

Installation
========================

This part of the documentation covers the installation of GEOLib.
The first step to using any software package is getting it properly installed.

GEOLib installation
-------------------------

To install GEOLib, simply the following command::

    $ pip install git+git@bitbucket.org:DeltaresGEO/geolib.git

At a later stage, released versions will be available from the repository as .whl installs.

Requirements
------------

This package, unlike GEOLib+, tries to limit the number of
*heavy* depedencies. The main packages used are:

- Poetry_ for package management (replacing setuptools) see also `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_.
- Pydantic_ for validation of types and some parameters (min/max/defaults)

.. _Poetry: https://python-poetry.org/docs/
.. _Pydantic: https://pydantic-docs.helpmanual.io/

Get the Source Code
-------------------

GEOLib is actively developed on BitBucket, where the code is
`always available <https://bitbucket.org/DeltaresGEO/geolib/src>`_.

You can either clone the public repository::

    $ git clone git@bitbucket.org:DeltaresGEO/geolib.git

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd geolib
    $ pip install poetry
    $ poetry install
