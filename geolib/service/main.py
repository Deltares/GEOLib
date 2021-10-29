import secrets
import shutil
import uuid
from pathlib import Path, PosixPath, WindowsPath
from typing import Dict, List, Type, Union

import pydantic.json
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import ValidationError, conlist
from starlette import status
from starlette.responses import JSONResponse

from geolib.errors import CalculationError
from geolib.models import (
    BaseModel,
    BaseModelList,
    DFoundationsModel,
    DSettlementModel,
    DSheetPilingModel,
    DStabilityModel,
)
from geolib.models.meta import MetaData

# Fixes for custom serialization
pydantic.json.ENCODERS_BY_TYPE[Path] = str
pydantic.json.ENCODERS_BY_TYPE[PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[WindowsPath] = str

settings = MetaData()
app = FastAPI()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.gl_username)
    correct_password = secrets.compare_digest(credentials.password, settings.gl_password)
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


def cleanup(path: Path):
    print(f"Cleaning up {path}")
    shutil.rmtree(path)


def execute(model, background_tasks: BackgroundTasks):
    unique_id = str(uuid.uuid4())
    unique_folder = Path(settings.calculation_folder / unique_id).absolute()
    unique_folder.mkdir(parents=True, exist_ok=True)
    ext = model.parser_provider_type().input_parsers[0].suffix_list[0]
    model.serialize(unique_folder / f"{unique_id}{ext}")

    # Override console folder from client
    model.meta.console_folder = settings.console_folder

    try:
        output = model.execute()
    except (CalculationError, ValidationError) as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e), "traceback": unique_id},
        )
    else:
        return output
    finally:
        background_tasks.add_task(cleanup, unique_folder)


@app.post("/calculate/dsettlementmodel")
async def calculate_dsettlementmodel(
    model: DSettlementModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DSettlementModel:
    return execute(model, background_tasks)


@app.post("/calculate/dfoundationsmodel")
async def calculate_dfoundationsmodel(
    model: DFoundationsModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DFoundationsModel:
    return execute(model, background_tasks)


@app.post("/calculate/dsheetpilingmodel")
async def calculate_dsheetpilingmodel(
    model: DSheetPilingModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DSheetPilingModel:
    return execute(model, background_tasks)


@app.post("/calculate/dstabilitymodel")
async def calculate_dstabilitymodel(
    model: DStabilityModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DStabilityModel:
    return execute(model, background_tasks)


@app.post("/calculate/dsettlementmodels")
async def calculate_many_dsettlementmodels(
    models: conlist(DSettlementModel, min_items=1),
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> List[DSettlementModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dfoundationsmodels")
async def calculate_many_dfoundationsmodel(
    models: conlist(DFoundationsModel, min_items=1),
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> List[DFoundationsModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dsheetpilingmodels")
async def calculate_many_dsheetpilingmodel(
    models: conlist(DSheetPilingModel, min_items=1),
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> List[DSheetPilingModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dstabilitymodels")
async def calculate_many_dstabilitymodel(
    models: conlist(DStabilityModel, min_items=1),
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> List[DStabilityModel]:
    return execute_many(models, background_tasks)


def execute_many(
    models: BaseModelList, background_tasks: BackgroundTasks
) -> BaseModelList:
    unique_id = str(uuid.uuid4())
    unique_folder = Path(settings.calculation_folder / unique_id).absolute()
    unique_folder.mkdir(parents=True, exist_ok=True)

    bm = BaseModelList(models=models)

    try:
        output = bm.execute(unique_folder, nprocesses=settings.nprocesses)
    except (CalculationError, ValidationError) as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e), "traceback": unique_id},
        )
    else:
        return output
    finally:
        background_tasks.add_task(cleanup, unique_folder)
