import secrets
import shutil
from pathlib import Path
from typing import Union
import uuid

# TODO Make sure that fastapi is installed
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

from geolib import models
from geolib.errors import CalculationError
from geolib.models import BaseModel

from .settings import Settings

settings = Settings()
app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.username)
    correct_password = secrets.compare_digest(credentials.password, settings.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


umodels = Union[
    models.DFoundationsModel,
    models.DSheetPilingModel,
    models.DStabilityModel,
    models.DSettlementModel,
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


def cleanup(path: Path):
    print(f"Cleaning up {path}")
    shutil.rmtree(path)


@app.post("/calculate")
async def calculate(
    model: umodels,
    background_tasks: BackgroundTasks,
    # _: str = Depends(get_current_username),
) -> Union[umodels, CalculationError]:
    unique_id = str(uuid.uuid4())
    unique_folder = Path(settings.calculation_folder / unique_id).absolute()
    unique_folder.mkdir(parents=True, exist_ok=True)
    ext = model.parser_provider_type().input_parsers[0].suffix_list[0]
    model.serialize(unique_folder / f"{unique_id}{ext}")

    try:
        output = model.execute()
    except CalculationError as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=e.__dict__
        )
    else:
        return output
    finally:
        background_tasks.add_task(cleanup, unique_folder)
