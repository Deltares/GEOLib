from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from geolib import BaseModelList, DFoundationsModel, DSettlementModel
from geolib.pydantic import pydanticv1_loaded
from tests.utils import TestUtils, only_teamcity

pytestmark = pytest.mark.skipif(
    pydanticv1_loaded, reason="FastApi uses pydantic v2 when it is available."
)

if not pydanticv1_loaded:
    from geolib.service.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        yield client


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate_empty_model_fails(client: TestClient):
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
def test_post_calculate(client: TestClient):
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
def test_post_calculate_many(client: TestClient):
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
def test_auth(client: TestClient):
    response = client.post(
        "/calculate/dsettlementmodels",
        json=[],
        auth=HTTPBasicAuth("test", "test"),
    )
    assert response.status_code == 422
    assert "at least 1 item" in response.text
