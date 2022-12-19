import sys
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs

def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return competitions_started(listOfCompetitions)

def first(elements):
    """Returns the first element of a given iterable.
    If the element is empty, it returns the empty element.
    If not itable it raise an exception.
    """
    try:
        return next(iter(elements))
    except TypeError as e:
        raise TypeError(e)
    except StopIteration:
        return elements

def filter_list_of_dict(list_of_dict, **kwargs):
    """Filter list of dictionaries based on the given kwargs arguments"""
    return [n for n in list_of_dict
            if all(n.get(k) == v for k, v in kwargs.items())]

def get_from_list_of_dict(list_of_dict, **kwargs):
    """Get the first element of a list of dictionaries filtered by kwargs arguments."""
    return first(filter_list_of_dict(list_of_dict, **kwargs))

def competitions_started(competitions):
    now = datetime.now()
    for comp in competitions:
        date_to_check = datetime.strptime(comp['date'], '%Y-%m-%d %H:%M:%S')
        comp['started'] = True if date_to_check < now else False
    return competitions

app = Flask(__name__)
app.config.from_pyfile('config.py')

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = get_from_list_of_dict(clubs, **request.form)
    if not club:
        flash("We can't find the email address")
        return render_template('index.html')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = get_from_list_of_dict(clubs, **{'name': club})
    foundCompetition = get_from_list_of_dict(competitions, **{'name': competition})
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = get_from_list_of_dict(competitions,
                                        name=request.form['competition'])
    club = get_from_list_of_dict(clubs, name=request.form['club'])
    placesRequired = int(request.form['places'])

    if placesRequired > 12:
        flash(f"You can't book more than 12 places.")
        return render_template('booking.html', club=club,
                               competition=competition)

    if placesRequired > int(club['points']):
        flash(f"You don't have enough points to get this number of places."
              f"\nYou only have {club['points']} points")
        return render_template('booking.html', club=club,
                               competition=competition)
    if competition['started']:
        flash("You can't book a past competition")
        return render_template('welcome.html', club=club, competitions=competitions)

    club['points'] = str(int(club['points']) - placesRequired)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/club-points')
def club_points():
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

def main(argv=[]):
    kwargs = dict()
    if "debug" in argv:
        app.config["debug"] = True

    return app


if __name__ == "__main__":
    app = main(sys.argv[1:])
    app.run()
