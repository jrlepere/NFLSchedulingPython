import numpy as np

def get_schedule_info(filepath):
	"""
	Gets the team and matchup information from a file in the form:
	  home, away (header)
	  hometeam name, awayteam name
	  hometeam name, awayteam name
	  ...
	
	Args:
	  filepath: the path to the file
	
	Return:
	  team: dictionary of team name to team index
	  matchups: [[hometeam index, awayteam index],
	  			 [hometeam index, awayteam index],
	  			 ...]
	"""
	
	# map from team name to team index
	teams = dict()
	with open(filepath, 'r') as f:
		next(f)
		for line in f:
			if line.split(',')[0].strip() not in teams:
				teams[line.split(',')[0].strip()] = len(teams)
			if line.split(',')[1].strip() not in teams:
				teams[line.split(',')[1].strip()] = len(teams)		
	
	# map from mathup index to home/away team index
	matchup_team = []
	with open(filepath, 'r') as f:
		next(f)
		for line in f:
			matchup_team.append([
				teams[line.split(',')[0].strip()],
				teams[line.split(',')[1].strip()]
			])
	
	# return information
	return teams, matchup_team

teams, matchup_team = get_schedule_info('../resources/nfl-matchups_2018.csv')

def get_matchup_index(hometeam, awayteam):
	"""
	Get the index of the matchup between the hometeam and awayteam

	Args:
	  hometeam: the index of the home team
	  awaytaem: the index of the away team

	Return:
	  The index of the matchup.
	"""

	# find the matchup
	for i in range(len(matchup_team)):
		if matchup_team[i][0] == hometeam and matchup_team[i][1] == awayteam:
			return i

	# not found
	raise Exception("matchup not found for %s, %s" % (hometeam, awayteam))

num_games_per_week = [16, 16, 16, 15, 15, 15, 14, 14, 13, 14, 13, 15, 16, 16, 16, 16, 16]
thanksgiving_gameslots = [161,162,163]
NUM_WEEKS = len(num_games_per_week)
london_games = [79, 94, 108]
mexico_games = [160]

# number of matchups, gameslots and teams
NUM_GAMESLOTS = len(matchup_team)
NUM_MATCHUPS = len(matchup_team)
NUM_TEAMS = len(teams)

# week gameslot matrix
week_gameslot = []
count = 0
for n in num_games_per_week:
	week_games = [0 for _ in range(256)]
	week_games[count:count+n] = [1 for _ in range(n)]
	count += n
	week_gameslot.append(week_games)
gameslot_week = np.array(week_gameslot, dtype=np.uint32).T

# TEAMS
RAIDERS = teams["Oakland Raiders"]
SEAHAWKS = teams["Seattle Seahawks"]
CHARGERS = teams["Los Angeles Chargers"]
TITANS = teams["Tennessee Titans"]
JAGUARS = teams["Jacksonville Jaguars"]
EAGLES = teams["Philadelphia Eagles"]
RAMS = teams["Los Angeles Rams"]
CHIEFS = teams["Kansas City Chiefs"]
LIONS = teams["Detroit Lions"]
COWBOYS = teams["Dallas Cowboys"]
JETS = teams["New York Jets"]
GIANTS = teams["New York Giants"]

# MATCHUPS
RAIDERS_SEAHAWKS = get_matchup_index(RAIDERS, SEAHAWKS)
CHARGERS_TITANS = get_matchup_index(CHARGERS, TITANS)
JAGUARS_EAGLES = get_matchup_index(JAGUARS, EAGLES)
RAMS_CHIEFS = get_matchup_index(RAMS, CHIEFS)

