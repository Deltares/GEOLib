from geolib import DFoundationsModel
from geolib.service.main import app
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
import pytest
from tests.utils import only_teamcity

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.acceptance
@only_teamcity
def test_post_calculate():
    model = DFoundationsModel()

    response = client.post(
        "/calculate", json={"model": model.json()}, auth=HTTPBasicAuth("test", "test")
    )
    assert response.status_code == 500
    assert "status_code" in response.text
