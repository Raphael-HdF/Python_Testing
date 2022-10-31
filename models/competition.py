class ListOfCompetitions:
    list_name = 'competitions'

    def __init__(self, competitions=[]):
        self.competitions = [Competition(**competition) for competition in competitions]

    def __iter__(self):
        return iter(self.competitions)

    def __next__(self):
        return next(self.competitions)

    def filter_competitions(self, **kwargs):
        return [n for n in self.competitions
                if all(getattr(n, k) == v for k, v in kwargs.items())]

    def get_competition(self, **kwargs):
        competitions = self.filter_competitions(**kwargs)
        return competitions[0] if competitions else None


class Competition:
    def __init__(self, name, date, numberOfPlaces):
        self.name = name
        self.date = date
        self.numberOfPlaces = numberOfPlaces

    def __repr__(self):
        return self.name
