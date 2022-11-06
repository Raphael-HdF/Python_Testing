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
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("We can't find the email address")
        return render_template('index.html')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][
        0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
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
