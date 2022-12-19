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

    def test_request_showSummary_not_found(self, client, mocker, clubs):
        mocker.patch("server.clubs", clubs)
        response = client.post('/showSummary',
                               data=dict(email="test@test.com", ),
                               follow_redirects=True)
        assert response.status_code == 200
        assert b"We can&#39;t find the email address" in response.data

    def test_request_book(self, client, mocker, clubs, competitions):
        mocker.patch("server.competitions", competitions)
        url = quote("/book/" + competitions[2].get('name') + '/' + clubs[2].get('name'))
        response = client.get(url)
        assert response.status_code == 200
        assert b"Places available: 55" in response.data

    def test_request_book_fail(self, client, mocker, clubs, competitions):
        mocker.patch("server.competitions", competitions)
        url = quote("/book/" + 'erreur' + '/' + clubs[2].get('name'))
        response = client.get(url)
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data

    def test_request_purchasePlaces(self, client, mocker, clubs, competitions_started):
        mocker.patch("server.clubs", clubs)
        mocker.patch("server.competitions", competitions_started)
        competition = competitions_started[2].get('name')
        club = clubs[1].get('name')
        response = client.post('/purchasePlaces',
                               data=dict(
                                   competition=competition,
                                   club=club,
                                   places=2,
                               ))
        assert response.status_code == 200
        # Message confirming the booking
        assert b'Great-booking complete!' in response.data
        # Message giving the resulting points
        assert b'Number of Places: 53' in response.data
        # Message giving the points remaining
        assert b'Points available: 2' in response.data

    def test_request_purchasePlaces_cant_book_more_than_twelve(self, client, mocker,
                                                               clubs,
                                                               competitions_started):
        mocker.patch("server.clubs", clubs)
        mocker.patch("server.competitions", competitions_started)
        competition = competitions_started[2].get('name')
        club = clubs[1].get('name')
        response = client.post('/purchasePlaces',
                               data=dict(
                                   competition=competition,
                                   club=club,
                                   places=14,
                               ))
        assert response.status_code == 200
        # Message blocking
        assert b"You can&#39;t book more than 12 places." in response.data

    def test_request_purchasePlaces_not_enough_points(self, client, mocker, clubs,
                                                      competitions_started):
        mocker.patch("server.clubs", clubs)
        mocker.patch("server.competitions", competitions_started)
        competition = competitions_started[2].get('name')
        club = clubs[1].get('name')
        response = client.post('/purchasePlaces',
                               data=dict(
                                   competition=competition,
                                   club=club,
                                   places=5,
                               ))
        assert response.status_code == 200
        # Message blocking
        assert b"You don&#39;t have enough points to get this number of places." in response.data
        # Message giving the points remaining
        assert b'You only have 4 points' in response.data

    def test_request_purchasePlaces_competiton_started(self, client, mocker, clubs,
                                                       competitions_started):
        mocker.patch("server.clubs", clubs)
        mocker.patch("server.competitions", competitions_started)
        competition = competitions_started[0].get('name')
        club = clubs[1].get('name')
        response = client.post('/purchasePlaces',
                               data=dict(
                                   competition=competition,
                                   club=club,
                                   places=2,
                               ))
        assert response.status_code == 200
        # Message blocking on past competition
        assert b"You can&#39;t book a past competition" in response.data

    def test_request_club_points(self, client, mocker, clubs):
        mocker.patch("server.clubs", clubs)
        response = client.get("/club-points")
        assert response.status_code == 200
        assert b"She Lifts<br>\n            Number of Points: 12" in response.data
        assert clubs[2]['points'] == '12'

    def test_request_logout(self, client):
        response = client.get("/logout",
                              follow_redirects=True)
        assert response.status_code == 200
        assert b"Welcome to the GUDLFT Registration Portal!" in response.data

    def test_main(self, client):
        app = server.main(['debug'])
        assert app.config['debug'] == True
