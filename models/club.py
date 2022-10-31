class ListOfClubs:
    def __init__(self, clubs=[]):
        self.clubs = [Club(**club) for club in clubs]

    def __iter__(self):
        return iter(self.clubs)

    def __next__(self):
        return next(self.clubs)

    def filter_clubs(self, **kwargs):
        return [n for n in self.clubs
                if all(getattr(n, k) == v for k, v in kwargs.items())]

    def get_club(self, **kwargs):
        clubs = self.filter_clubs(**kwargs)
        return clubs[0] if clubs else None


class Club:
    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def __repr__(self):
        return self.name
