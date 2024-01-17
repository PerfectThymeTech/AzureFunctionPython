import pytest
from fastapi.testclient import TestClient
from fastapp.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize("version", ("v1",))
def test_get_heartbeat(client, version):
    # arrange
    path = f"/{version}/health/heartbeat"
    headers = {
        "x-ms-auth-internal-token": "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="
    }

    # action
    response = client.get(path, headers=headers)

    # assert
    assert response.status_code == 200
    assert response.json() == {"isAlive": True}


@pytest.mark.parametrize("version", ("v1",))
def test_post_sample(client, version):
    # arrange
    path = f"/{version}/sample/sample"

    # action
    response = client.post(path, json={"input": "Test"})

    # assert
    assert response.status_code == 200
    assert response.json() == {"output": "Hello Test"}
