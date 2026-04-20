from pathlib import Path, PosixPath, WindowsPath

import pytest
from fastapi.testclient import TestClient
from geolib.models import BaseModelList, DFoundationsModel, DSettlementModel
from geolib.service.main import app
from pydantic.deprecated import json as pydantic_json
from requests.auth import HTTPBasicAuth

from tests.utils import TestUtils, only_teamcity

pydantic_json.ENCODERS_BY_TYPE[Path] = str
pydantic_json.ENCODERS_BY_TYPE[PosixPath] = str
pydantic_json.ENCODERS_BY_TYPE[WindowsPath] = str

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate_empty_model_fails():
    model = DFoundationsModel()

    payload = model.model_dump(mode="json")

    response = client.post(
        "/calculate/dfoundationsmodel",
        json=payload,
        auth=HTTPBasicAuth("test", "test"),
    )
    assert response.status_code == 500
    assert "message" in response.text


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate():
    model = DSettlementModel()
    input_folder = Path(TestUtils.get_local_test_data_dir("dsettlement/benchmarks"))
    benchmark_fn = input_folder / "bm1-1.sli"
    model.parse(benchmark_fn)

    payload = model.model_dump(mode="json")

    response = client.post(
        "/calculate/dsettlementmodel",
        json=payload,
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
    input_folder = Path(TestUtils.get_local_test_data_dir("dsettlement/benchmarks"))
    benchmark_fn = input_folder / "bm1-1.sli"

    ml = BaseModelList(models=[a, b])
    for i, model in enumerate(ml.models):
        model.parse(benchmark_fn)
    ml.models.append(DSettlementModel(filename=Path("c.sli")))

    payload = [model.model_dump(mode="json") for model in ml.models]

    response = client.post(
        "/calculate/dsettlementmodels",
        json=payload,
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
    assert "List should have at least 1 item after validation" in response.text
