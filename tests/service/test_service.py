from pathlib import Path, PosixPath, WindowsPath

import pydantic.json
import pytest
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from geolib import BaseModelList, DFoundationsModel, DSettlementModel
from geolib.service.main import app
from tests.utils import TestUtils, only_teamcity

pydantic.json.ENCODERS_BY_TYPE[Path] = str
pydantic.json.ENCODERS_BY_TYPE[PosixPath] = str
pydantic.json.ENCODERS_BY_TYPE[WindowsPath] = str

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate_empty_model_fails():
    model = DFoundationsModel()

    response = client.post(
        "/calculate/dfoundationsmodel",
        data=model.json(),
        auth=HTTPBasicAuth("test", "test"),
    )
    assert response.status_code == 500
    assert "message" in response.text


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate():
    model = DSettlementModel()
    input_folder = Path(TestUtils.get_local_test_data_dir("dsettlement"))
    benchmark_fn = input_folder / "bm1-1.sli"
    model.parse(benchmark_fn)

    response = client.post(
        "/calculate/dsettlementmodel",
        data=model.json(),
        auth=HTTPBasicAuth("test", "test"),
    )

    assert response.status_code == 200
    assert DSettlementModel(**response.json())


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate_many():
    # Setup models
    a = DSettlementModel()
    b = DSettlementModel()
    input_folder = Path(TestUtils.get_local_test_data_dir("dsettlement"))
    benchmark_fn = input_folder / "bm1-1.sli"

    ml = BaseModelList(models=[a, b])
    for i, model in enumerate(ml.models):
        model.parse(benchmark_fn)
    ml.models.append(DSettlementModel(filename=Path("c.sli")))

    response = client.post(
        "/calculate/dsettlementmodels",
        data="[" + ",".join((model.json() for model in ml.models)) + "]",
        auth=HTTPBasicAuth("test", "test"),
    )
    assert response.status_code == 200
    assert "models" in response.json()
    assert "errors" in response.json()

    # Empty model yields errors
    assert len(response.json()["errors"]) == 1
    assert "c.sli" in response.json()["errors"][-1]


@pytest.mark.unittest
def test_auth():
    response = client.post(
        "/calculate/dsettlementmodels",
        json=[],
        auth=HTTPBasicAuth("test", "test"),
    )
    assert response.status_code == 422
    assert "ensure this value has at least 1 items" in response.text
