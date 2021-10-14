.. _server:

Server
======

GEOLib comes with a built-in webservice that enables users to use it as a remote
endpoint for their calculations.

You should install GEOLib with `pip install geolib[server]` as described in :ref:`install`. 
That enables you to run::

    $ uvicorn geolib.service.main:app

Now you can use the *execute_remote* methods on the GEOLib models, pointing to this
server. Note that this server needs to be configured correctly as a standalone
GEOLib client first.

For hosting a more production ready environment, such as services, see the documentation at https://www.uvicorn.org/deployment/. 
Note that not all options work on the Windows platform, but Circus will.

Authentication
--------------

The service is protected by basic authentication (i.e. username & password) only.
Since the default is to run uvicorn over unencrypted HTTP, this is **not secure** for 
untrusted networks.

You can configure the username (GL_USERNAME, default is "test") and password 
(GL_PASSWORD, default is "test") using *geolib.env* or environment variables
as described in :ref:`setup`.
