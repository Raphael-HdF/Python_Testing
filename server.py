import sys
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from models import ListOfClubs, ListOfCompetitions


def loadClubs():
    with open('clubs.json') as c:
        list_of_clubs = ListOfClubs(json.load(c)['clubs'])
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
        list_of_competitions = ListOfCompetitions(json.load(comps)['competitions'])
        return list_of_competitions


app = Flask(__name__)
app.config.from_pyfile('config.py')

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = clubs.filter_clubs(**request.form)[0]
    except IndexError:
        flash("We can't find the email address")
        return render_template('index.html')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = clubs.get_club(name=club)
    found_competition = competitions.get_competition(name=competition)
    if found_club and found_competition:
        return render_template('booking.html', club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = competitions.get_competition(**request.form)
    club = clubs.get_club(**request.form)
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


def main(argv):
    kwargs = dict()
    if "debug" in argv:
        kwargs['debug'] = True
    app.run(**kwargs)


if __name__ == "__main__":
    main(sys.argv[1:])
