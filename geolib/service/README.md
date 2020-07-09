# GEOLib calculation webservice

This webservice, when correctly configured, enables users to use it as a remote
endpoint for their calculations. They don't need the consoles or licenses installed
locally.

You should install GEOLib with pip install geolib[server]. That enables you to run:

```bash
uvicorn main:app --reload
```

For a more production ready environment see the documentation at https://fastapi.tiangolo.com/deployment/#alternatively-deploy-fastapi-without-docker, specifically https://www.uvicorn.org/#running-with-gunicorn.
