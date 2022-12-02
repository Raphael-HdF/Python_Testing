import pytest
import server
from tests.conftest import client


def test_request_index(client):
    response = client.get("/")
    assert response.status_code == 200
    # assert b"<h2>Hello, World!</h2>" in response.data


