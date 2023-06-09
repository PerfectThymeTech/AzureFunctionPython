import pytest
from fastapi.testclient import TestClient
from core.config import settings
from main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize("version", ("v1",))
def test_get_heartbeat(client, version):
    # arrange
    path = f"/corrector/{version}/heartbeat"

    # action
    response = client.get(path)

    # assert
    assert response.status_code == 200
    assert response.json() == {"isAlive": True}
