from random import choice, randint
from locust import HttpUser, task, between
from urllib.parse import quote

from server import loadClubs, loadCompetitions


class PerformanceTest(HttpUser):
    wait_time = between(1, 5)
    clubs = loadClubs()
    competitions = loadCompetitions()

    def on_start(self):
        club = choice(self.clubs)
        self.client.post("/showSummary", data=dict(email=club.get('email')))

    def on_stop(self):
        self.client.get("/logout")

    @task()
    def purchasePlaces(self):
        club = choice(self.clubs)
        competition = choice(self.competitions)
        self.client.post('/purchasePlaces',
                         data=dict(
                             competition=competition.get('name'),
                             club=club.get('name'),
                             places=randint(1, 15),
                         ))

    @task()
    def book(self):
        club = choice(self.clubs)
        competition = choice(self.competitions)
        url = quote("/book/" + competition.get('name') + '/' + club.get('name'))
        self.client.get(url)

    @task()
    def index(self):
        self.client.get("/")

    @task()
    def club_points(self):
        self.client.get("/club_points")
