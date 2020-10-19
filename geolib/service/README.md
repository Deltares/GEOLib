# GEOLib calculation webservice

This webservice, when correctly configured, enables users to use it as a remote
endpoint for their calculations. They don't need the consoles or licenses installed
locally.

You should install GEOLib with pip install geolib[server]. That enables you to run:

```bash
uvicorn main:app --reload
```

For hosting a more production ready environment, such as services, see the documentation at https://www.uvicorn.org/deployment/. 
Note that not all options work on the Windows platform, but Circus will.