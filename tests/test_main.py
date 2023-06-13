import pytest
from fastapi.testclient import TestClient
from fastapp.main import fastapi_app


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


@pytest.mark.parametrize("version", ("v1",))
def test_post_sample(client, version):
    # arrange
    path = f"/{version}/sample/sample"

    # action
    response = client.post(path, json={"input": "Test"})

    # assert
    assert response.status_code == 200
    assert response.json() == {"output": "Hello Test"}
