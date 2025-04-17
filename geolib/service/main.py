import secrets
import shutil
import uuid
from pathlib import Path, PosixPath, WindowsPath

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import Field, ValidationError
from pydantic.deprecated import json as pydantic_json
from starlette import status
from starlette.responses import JSONResponse
from typing_extensions import Annotated

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
pydantic_json.ENCODERS_BY_TYPE[Path] = str
pydantic_json.ENCODERS_BY_TYPE[PosixPath] = str
pydantic_json.ENCODERS_BY_TYPE[WindowsPath] = str

settings = MetaData()
app = FastAPI()
security = HTTPBasic()


# Models (types) are defined below, because they are used in the
# signatures of the functions and they differ between Pydantic v1 and v2.
dsettlement_list = Annotated[list[DSettlementModel], Field(min_length=1)]
dfoundation_list = Annotated[list[DFoundationsModel], Field(min_length=1)]
dsheetpile_list = Annotated[list[DSheetPilingModel], Field(min_length=1)]
dstability_list = Annotated[list[DStabilityModel], Field(min_length=1)]


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


@app.get("/", response_model=False)
async def root():
    return {"message": "Hello World"}


def cleanup(path: Path):
    print(f"Cleaning up {path}")
    shutil.rmtree(path)


def execute(model: BaseModel, background_tasks: BackgroundTasks):
    unique_id = str(uuid.uuid4())
    unique_folder = Path(settings.calculation_folder / unique_id).absolute()
    unique_folder.mkdir(parents=True, exist_ok=True)
    ext = model.parser_provider_type().input_parsers[0].suffix_list[0]
    model.serialize(unique_folder / f"{unique_id}{ext}")

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


@app.post("/calculate/dsettlementmodel", response_model=None)
async def calculate_dsettlementmodel(
    model: DSettlementModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DSettlementModel:
    return execute(model, background_tasks)


@app.post("/calculate/dfoundationsmodel", response_model=None)
async def calculate_dfoundationsmodel(
    model: DFoundationsModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DFoundationsModel:
    return execute(model, background_tasks)


@app.post("/calculate/dsheetpilingmodel", response_model=None)
async def calculate_dsheetpilingmodel(
    model: DSheetPilingModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DSheetPilingModel:
    return execute(model, background_tasks)


@app.post("/calculate/dstabilitymodel", response_model=None)
async def calculate_dstabilitymodel(
    model: DStabilityModel,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> DStabilityModel:
    return execute(model, background_tasks)


@app.post("/calculate/dsettlementmodels", response_model=None)
async def calculate_many_dsettlementmodels(
    models: dsettlement_list,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> list[DSettlementModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dfoundationsmodels", response_model=None)
async def calculate_many_dfoundationsmodel(
    models: dfoundation_list,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> list[DFoundationsModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dsheetpilingmodels", response_model=None)
async def calculate_many_dsheetpilingmodel(
    models: dsheetpile_list,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> list[DSheetPilingModel]:
    return execute_many(models, background_tasks)


@app.post("/calculate/dstabilitymodels", response_model=None)
async def calculate_many_dstabilitymodel(
    models: dstability_list,
    background_tasks: BackgroundTasks,
    _: str = Depends(get_current_username),
) -> list[DStabilityModel]:
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
