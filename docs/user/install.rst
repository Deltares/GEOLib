.. _install:

Installation
========================

This part of the documentation covers the installation of GEOLib.
The first step to using any software package is getting it properly installed.

GEOLib installation
-------------------

GEOLib releases are available from PyPI::

    $ pip install d-geolib

To install the latest GEOLib simply the following command::

    $ pip install git+git@github.com:Deltares/GEOLib.git

Note that both locations are private and require authentication.

GEOLib service
--------------

If you also want to host your own calculation service, you should also
install some extra packages::

    $ pip install 'geolib-0.1.0-py3-none-any.whl[server]'


Packages used
-------------

This package, unlike GEOLib+, tries to limit the number of
*heavy* depedencies. The main packages used are:

- Poetry_ for package management (replacing setuptools) see also `PEP 518 <https://www.python.org/dev/peps/pep-0518/>`_.
- Pydantic_ for validation of types and some parameters (min/max/defaults).

.. _Poetry: https://python-poetry.org/docs/
.. _Pydantic: https://pydantic-docs.helpmanual.io/

You don't need to install anything manually, as the pip installation should take care of it.

Combining GEOLib with pydantic v2
---------------------------------

GEOLib uses pydantic for validation of types and some parameters (min/max/defaults). The 
latest version of pydantic (v2) has some breaking changes. When using pydantic v2, some
extra dependencies are required.To use GEOLib with pydantic v2, you can use the following
command to automatically install the extra dependencies::

    $ pip install d-geolib[pydantic-v2]

When the extra dependencies are not installed, and pydantic v2 is used, an error will be
thrown when trying to import GEOLib. The error message will guide you in installing the
required packages yourself.

Get the Source Code
-------------------

GEOLib is actively developed on Github, where the code is
`always available <https://github.com/Deltares/GEOLib>`_.

You can either clone the public repository::

    $ git clone git@github.com:Deltares/GEOLib.git

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd geolib
    $ pip install poetry
    $ poetry install
