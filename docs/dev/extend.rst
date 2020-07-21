.. _extend:

Contributing
============

This part of the documentation covers the main components of GEOLib, including
the external packages used with an explanation, so users know how to extend the
GEOLib package.

Structure
---------

The structure of the GEOLib package follows common patterns:
    - `docs` for the documentation
    - `geolib` for the source of the package
    - `tests` for all test related code

The structure of the geolib folder itself is still in flux, but the overall
structure is as follows:

    - `geometry` for generic geometry classes and related functions
    - `soils` for generic soils and related functions
    - `models` for (abstract) base classes related to models and all related classes such as parsers, serializers and validators
    - `models/model` for the implementation of above

Naming of files should be readable, in such a way that if you're looking for a class
you should be able to find the relevant Python file from browsing the directory tree alone.

Testing
-------

When developing a new feature it's a good practice to start with a simple test script
that documents how you should use the new feature. The test will fail in the beginning
because nothing is implemented or linked yet, but should be fixed in the end. This is
also the simplest way of navigating a large complex package, instead of trying to get 
everything running in a separate script.

The test package we're using is pytest: https://docs.pytest.org/en/latest/. You can find
the tests in the `tests` folder. For each model there's a subfolder. When you need data,
such as input files in your tests, you can put these in the `test_data` subfolder. These
files are checked in using Git LFS.

When testing user facing functions (the public API) that take simple types such as strings
or integers, it's good to also use Hypothesis: https://hypothesis.readthedocs.io/en/latest/quickstart.html
in your tests. Instead of testing with one string of your own making, hypothesis will
generate many strings, including empty ones for you.


Documenting
-----------

We use Sphinx and thus reStructuredText `.rst` files to write our documentation. It is good to read the basics about
reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html.

**Always** write docstrings for your classes, methods or functions. These docstrings are used
automatically in the documentation. Many IDEs support generating a docstring on the fly.
We use the Google style of docstrings:

.. code-block:: python

    def func(arg1: int, arg2: str) -> bool:
        """Summary line.

        Extended description of function.

        Args:
            arg1: Description of arg1
            arg2: Description of arg2

        Returns:
            Description of return value

        """
        return True

You can find the Sphinx documentation about this style here: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

To document usages or examples, the docstring of a class is often not the right place. You can
place these examples at the top of the module, like this for the `dstability_model.py`.

.. code-block:: python

    """

    Usage::

        >>> dstab = DStabilityModel.parse("test.stix")
        >>> dstab.execute()
        >>> dstab.output
        <dict>

    """
    import abc

This will automatically show up in the documentation if the whole module is imported in the `docs`.


Inheritance
-----------

GEOLib makes extensive use of inheritance. In the `geolib/models` folder there are several
Python files that provide `BaseModel`\s, `BaseParser`\s, etc. This enables common behaviour and
greatly reduces the amount of duplicate code, but can be confusing at first. An example, not
all methods are defined on their children; you can `execute` a `DSettlementModel`, but the
execute method is only defined on the `BaseModel` and is thus the same of all derived Models.

We often inherit `BaseModel` (many times renamed as `DataClass` to distinguish it from our own
`BaseModel`) from Pydantic: https://pydantic-docs.helpmanual.io/
Pydantic combines the power of dataclasses (new in Python 3.7) with type hints and gives us way
less boilerplate and free validation on instantiation:

.. code-block:: python

    from datetime import datetime
    from typing import List, Optional
    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name = 'John Doe'
        signup_ts: Optional[datetime] = None
        friends: List[int] = []

Note how in the above example we need no `__init__` method like a dataclass. We can define
types and defaults for fields. We can even constrain fields (specifying a range of valid options
for a field) using only types: https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
Construction can be from dict and json, and vica versa. This is what we use for the internal dataclasses for each model.

Type hinting
------------

GEOLib uses type hinting in all its classes and functions. This is partly used for automatic validation
on initialization for classes by `pydantic`, but it's meant for overall readability.
Annotating your code with type hints reduces the amount of bugs by improving readability
and enabling the use of static code checkers such as `mypy`, which we also use.

If the type of variables in a function is unclear in the current context we
advise to also add type hints. An example:

.. code-block:: python

    def some_function(a: int) -> int:
        b: int = result_with_unknown_type_from_other_function()
        return a * b




Adding requirements
-------------------

New requirements can be added using Poetry: https://python-poetry.org/docs/
For example, adding a new package:

.. code-block:: bash

    $ poetry add new_package

It's good to keep the `requirements.txt` up to date, so afterwards run:

.. code-block:: bash

    $ poetry export --without-hashes -f requirements.txt > requirements.txt
