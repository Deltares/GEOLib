.. _install:

Installation
========================

.. image:: https://farm5.staticflickr.com/4230/35550376215_da1bf77a8c_k_d.jpg


This part of the documentation covers the installation of Geolib.
The first step to using any software package is getting it properly installed.

Geolib installation
-------------------------

To install Geolib, simply run these simple commands in your terminal of choice::

    $ pip install git+git@bitbucket.org:DeltaresGEO/geolib.git


Get the Source Code
-------------------

Requests is actively developed on BitBucket, where the code is
`always available <https://bitbucket.org/DeltaresGEO/geolib/src>`_.

You can either clone the public repository::

    $ git clone git@bitbucket.org:DeltaresGEO/geolib.git

Once you have a copy of the source, you can embed it in your own Python
package, or install it into your site-packages easily::

    $ cd geolib
    $ pip install poetry
    $ poetry install .
