from flask import Flask, render_template, request
from utils.utils import get_num_schedules, get_schedules, get_matchups, thanksgiving_gameslots
import argparse


# create flask app object
app = Flask(__name__)


def matchup_encode(matchup):
	"""
	Matchup encoding.
	
	Args:
	  matchup: the matchup [hometeam, awayteam]
	
	Return:
	  The encoded matchup
	"""
	return matchup[0] + ',' + matchup[1]


def matchup_decode(matchup):
	"""
	Matchup decoding.
	
	Args:
	  matchup: the encoded matchup
	
	Return:
	  The decoded matchup [hometeam, awayteam]
	"""
	return matchup.split(',')


def matchup_display(matchup):
	"""
	Format to display a matchup.
	
	Args:
	  matchup: the matchup [hometeam, awayteam]
	
	Return:
	  Formatted string to display
	"""
	return matchup[0].split(' ')[-1] + " vs " + matchup[1].split(' ')[-1]


# get all matchups for specific gameslots
matchups = get_matchups([0] + thanksgiving_gameslots)

# unique openers
openers = [['All', 'All']] + [[matchup_encode(matchup), matchup_display(matchup)] for matchup in matchups[0]]

# unique thanksgiving games
thanksgiving_matchups = [{'n':i, 'matchups':[['All', 'All']] + [[matchup_encode(matchup), matchup_display(matchup)] for matchup in matchups[i]]} for i in range(1, len(thanksgiving_gameslots) + 1)]


@app.route('/')
def home():
	
	# get arguments
	opener = request.args.get('opener') if request.args.get('opener') is not None else 'All'
	tgm1 = request.args.get('tgm1') if request.args.get('tgm1') is not None else 'All'
	tgm2 = request.args.get('tgm2') if request.args.get('tgm2') is not None else 'All'
	tgm3 = request.args.get('tgm3') if request.args.get('tgm3') is not None else 'All'
	
	# get a list of schedules
	schedules = get_schedules(num_schedules=50,
							  opener=matchup_decode(opener),
							  tgm1=matchup_decode(tgm1),
							  tgm2=matchup_decode(tgm2),
							  tgm3=matchup_decode(tgm3))
	
	# get the number of schedules in the database
	total_schedules = get_num_schedules()
	
	# render template
	return render_template('home.html',
							total_schedules=total_schedules,
							schedules=schedules,
							num_schedules=len(schedules),
							openers=openers,
							thanksgiving_matchups=thanksgiving_matchups)

@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/about')
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run()
