import pytest
from fastapi.testclient import TestClient

from fast_zero import app


@pytest.fixture()
def client():
    return TestClient(app)
