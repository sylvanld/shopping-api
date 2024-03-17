import pytest
from fastapi.testclient import TestClient

from shopping.api.factory import create_api


@pytest.fixture(scope="function")
def test_client():
    api = create_api({})
    client = TestClient(api)
    return client
