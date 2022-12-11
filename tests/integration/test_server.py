import pytest
import server
from tests.conftest import client
from tests.unit.test_server import TestFixture
from urllib.parse import quote


class TestServer(TestFixture):
    def test_request_index(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_request_showSummary(self, client, mocker, clubs):
        mocker.patch("server.clubs", clubs)
        response = client.post('/showSummary',
                               data=dict(email="admin@irontemple.com", ))
        assert response.status_code == 200
        assert b"Iron Temple" in response.data

    def test_request_book(self, client, mocker, clubs, competitions):
        mocker.patch("server.competitions", competitions)
        url = quote("/book/" + competitions[2].get('name') + '/' + clubs[2].get('name'))
        response = client.get(url)
        assert response.status_code == 200
        assert b"Places available: 55" in response.data

    def test_request_purchasePlaces(self, client, mocker, clubs, competitions):
        response = client.post('/purchasePlaces',
                               data=dict(
                                   competition=competitions[2],
                                   club=clubs[2],
                                   places=2,
                               ))
        assert response.status_code == 200

    def test_request_club_points(self, client, mocker, clubs):
        mocker.patch("server.clubs", clubs)
        response = client.get("/club-points")
        assert response.status_code == 200
        assert b"She Lifts<br>\n            Number of Points: 12" in response.data
        assert clubs[2]['points'] == '12'
