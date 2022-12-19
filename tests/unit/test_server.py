import datetime as dt
import pytest

from server import *


class TestFixture:
    @pytest.fixture
    def clubs(self):
        return [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "15"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
            }
        ]

    @pytest.fixture
    def competitions(self):
        now = dt.datetime.now()
        return [
            {
                "name": "Spring Festival",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-30), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-15), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "13"
            },
            {
                "name": "La compete",
                "date": dt.datetime.strftime(now + dt.timedelta(days=30), '%Y-%m-%d '
                                                                          '%H:%M:%S'),
                "numberOfPlaces": "55"
            }
        ]

    @pytest.fixture
    def competitions_started(self):
        now = dt.datetime.now()
        return [
            {
                "name": "Spring Festival",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-30), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "25",
                "started": True
            },
            {
                "name": "Fall Classic",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-15), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "13",
                "started": True
            },
            {
                "name": "La compete",
                "date": dt.datetime.strftime(now + dt.timedelta(days=30), '%Y-%m-%d '
                                                                          '%H:%M:%S'),
                "numberOfPlaces": "55",
                "started": False
            }
        ]


class TestGroup(TestFixture):

    @pytest.fixture
    def mocker_open_clubs(self, mocker):
        # Read a mocked /etc/release file
        file = '''{"clubs": [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "15"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
            {"name": "She Lifts",
             "email": "kate@shelifts.co.uk",
             "points": "12"
             }
        ]}'''
        mocked_etc_release_data = mocker.mock_open(read_data=file)
        mocker.patch("builtins.open", mocked_etc_release_data)

    def test_loadClubs(self, mocker_open_clubs):
        expected_value = [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "15"
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            },
            {"name": "She Lifts",
             "email": "kate@shelifts.co.uk",
             "points": "12"
             }
        ]

        assert loadClubs() == expected_value

    def test_filter_list_of_dict(self, clubs):
        expected_value = [
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
            }
        ]
        assert filter_list_of_dict(clubs, points="12") == expected_value

        expected_value = []
        assert filter_list_of_dict(clubs, points="2") == expected_value

    def test_get_from_list_of_dict(self, clubs):
        expected_value = {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
        assert get_from_list_of_dict(clubs,
                                     email="kate@shelifts.co.uk") == expected_value

        expected_value = []
        assert get_from_list_of_dict(clubs,
                                     email="dont_exist@test.fr") == expected_value

    def test_first(self):
        iterable = [1, 2, 3]
        assert first(iterable) == 1

        iterable = []
        assert first(iterable) == []

        iterable = 555
        with pytest.raises(TypeError):
            first(iterable)

    def test_competitions_started(self, competitions):
        now = dt.datetime.now()
        expected_value = [
            {
                "name": "Spring Festival",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-30), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "25",
                "started": True,
            },
            {
                "name": "Fall Classic",
                "date": dt.datetime.strftime(now + dt.timedelta(days=-15), '%Y-%m-%d '
                                                                           '%H:%M:%S'),
                "numberOfPlaces": "13",
                "started": True,
            },
            {
                "name": "La compete",
                "date": dt.datetime.strftime(now + dt.timedelta(days=30), '%Y-%m-%d '
                                                                          '%H:%M:%S'),
                "numberOfPlaces": "55",
                "started": False,
            }
        ]

        assert competitions_started(competitions) == expected_value
