import pymysql
from random import shuffle, randint
from utils.filters.matchup_filter import MatchupFilter


# connection information
host='localhost'
port=3306
dbname='nflschedules'
user='root'

# map from matchup index to home and away team
matchup_team = []
with open('/home/ubuntu/web/resources/nfl-matchups_2018.csv', 'r') as f:
	next(f)
	for line in f:
		matchup_team.append([
			line.split(',')[0].strip(),
			line.split(',')[1].strip()
		])

# header information
num_games_per_week = [16, 16, 16, 15, 15, 15, 14, 14, 13, 14, 13, 15, 16, 16, 16, 16, 16]
thanksgiving_gameslots = [161,162,163]
thanksgiving_week = 11


def get_num_schedules():
	"""
	Get the number of schedules in the database.
	  
	Return:
	  The number of schedules in the database.
	"""

	# schedule count
	schedule_count = None
	
	try:
		# try and get the number of rows in the database
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
			cursor.execute('SELECT COUNT(*) FROM schedules')
			schedule_count = cursor.fetchall()[0][0]
		
	finally:
		conn.close()
		
	# return schedule count
	return schedule_count


def get_matchups(gameslots):
	"""
	Get a list of all unique matchups for a certain gameslot.
	
	Args:
	  gameslots: a list of gameslots
	
	Return:
	  A list of [[[home, away], ...], [[home, away], ...], ...] for each unique matchup for each gameslots.
	"""
	
	# a list of unique schedules
	schedules = [[] for _ in range(len(gameslots))]
	
	try:
		# try and get the schedules
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
		
			# fetch the schedules
			cursor.execute('SELECT * FROM schedules ORDER BY score DESC')
			all_schedules = list(cursor.fetchall())
			
			# for each schedule, decode and add to result if the schedule
			#  passes all of the filters
			for schedule in all_schedules:
				
				# strip and split the string as stored in the database
				matchups_gameslot = schedule[0].strip().split(',')
				
				# find the matchup at gameslot i
				for i in range(len(matchups_gameslot)):
					for j in range(len(gameslots)):
						gs = gameslots[j]
						if int(matchups_gameslot[i]) == gs:
							if matchup_team[i] not in schedules[j]:
								schedules[j].append(matchup_team[i][:])
							break
	
	finally:
		conn.close()
		
	# return schedules
	return schedules


def get_schedules(num_schedules=None, opener=['All'], tgm1=['All'], tgm2=['All'], tgm3=['All']):
	"""
	Get the schedules from the database.
	
	Args:
	  num_schedules: the number of schedules to return, None for all.
	  opener: the opponent for the Super Bowl champion home opener game
	  
	Return:
	  A list of decoded schedules of the form:
	   schedules: {week_number: [[home,away], [home,away], ...]}
	   year: the schedule year
	   score: the schedule score
	"""

	# a list of schedules
	schedules = []
	
	# filters
	filters = []
	if opener != ['All']:
		filters.append(MatchupFilter(matchup=opener, gameslot=0, matchup_team=matchup_team))
	if tgm1 != ['All']:
		filters.append(MatchupFilter(matchup=tgm1, gameslot=thanksgiving_gameslots[0], matchup_team=matchup_team))
	if tgm2 != ['All']:
		filters.append(MatchupFilter(matchup=tgm2, gameslot=thanksgiving_gameslots[1], matchup_team=matchup_team))
	if tgm3 != ['All']:
		filters.append(MatchupFilter(matchup=tgm3, gameslot=thanksgiving_gameslots[2], matchup_team=matchup_team))
	
	try:
		# try and get the schedules
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
		
			# fetch the schedules
			cursor.execute('SELECT * FROM schedules ORDER BY score DESC')
			all_schedules = list(cursor.fetchall())
			
			# for each schedule, decode and add to result if the schedule
			#  passes all of the filters
			for schedule in all_schedules:
			
				# mapping from gameslot to matchup
				gameslot_matchups = dict()
				
				# strip and split the string as stored in the database
				matchups_gameslot = schedule[0].strip().split(',')
				
				# update gameslot matchups for each gameslot to [home, away] team
				for i in range(len(matchups_gameslot)):
					gameslot_matchups[int(matchups_gameslot[i])] = i
				
				# test filters
				acceptable = True
				for f in filters:
					if not f.filter(gameslot_matchups):
						acceptable = False
					if not acceptable:
						break
				
				# add decoded schedule, up to number of schedules
				if acceptable:
					schedules.append({
						'schedule': decode_matchups(gameslot_matchups),
						'year': schedule[1],
						'score': "%.3f" % schedule[2]
					})
					if len(schedules) == num_schedules:
						break
		
	finally:
		conn.close()
		
	# return schedules
	return schedules
	

def decode_matchups(gameslot_matchups):
	"""
	Decode the gameslot matchup indexes to gameslot matchup team names and day of week
	
	Args:
	  gameslot_matchups: a dictionary of gameslot index to matchup index.
	
	Return:
	  A schedule in the form: {week_number: [[home,away,day], [home,away,day], ...]}
	"""
	
	# update gameslot matchups for each gameslot to [home, away] team
	for i in range(len(gameslot_matchups)):
		gameslot_matchups[i] = matchup_team[gameslot_matchups[i]][:]
	
	# order the schedules by gameslot
	schedule_gameslot_matchups = [gameslot_matchups[i] for i in sorted(gameslot_matchups)]
	
	# week to schedule mapping
	week_schedule = dict()
	count = 0
	for week_num in range(len(num_games_per_week)):
		num_games = num_games_per_week[week_num]
		week = schedule_gameslot_matchups[count:count+num_games]
		if week_num != len(num_games_per_week) - 1:
			if week_num != thanksgiving_week:
				s = 1
				week[0].append('THURSDAY NIGHT')
			else:
				s = 3
				week[0].append('THANKSGIVING')
				week[1].append('THANKSGIVING')
				week[2].append('THANKSGIVING')
			for i in range(s, len(week)-2):
				week[i].append("SUNDAY")
			week[-2].append('SUNDAY NIGHT')
			week[-1].append('MONDAY NIGHT')
		else:
			for i in range(len(week)):
				week[i].append("SUNDAY")
		week_schedule[week_num+1] = week
		count += num_games
	
	# return the decoded schedules
	return week_schedule

	
