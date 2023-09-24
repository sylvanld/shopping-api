from fastapi.testclient import TestClient


def test_openapi_exposed(test_client: TestClient):
    response = test_client.get("/openapi.json")
    assert response.status_code == 200

    openapi_specs = response.json()
    assert openapi_specs.get("openapi").startswith("3.")
