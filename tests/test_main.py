import pytest
from fastapi.testclient import TestClient
from function.core.config import settings
from function.function_app import fastapi_app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(fastapi_app)


@pytest.mark.parametrize("version", ("v1",))
def test_get_heartbeat(client, version):
    # arrange
    path = f"/{version}/health/heartbeat"

    # action
    response = client.get(path)

    # assert
    assert response.status_code == 200
    assert response.json() == {"isAlive": True}
