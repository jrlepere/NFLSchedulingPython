import pymysql
from random import shuffle, randint


# connection information
host='nflschedules.cd7ko38smnnq.us-west-1.rds.amazonaws.com'
port=3306
dbname='nflschedules'
user='nflschedules'	


# map from mathup index to home and away team
matchup_team = []
with open('./resources/nfl-matchups_2018.csv', 'r') as f:
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


def get_num_schedules(password):
	"""
	Get the number of schedules in the database.
	
	Args:
	  password: the database password.
	  
	Return:
	  The number of schedules in the database.
	"""

	# schedule count
	schedule_count = None
	
	try:
		# try and get the number of rows in the database
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
			schedule_count = cursor.execute('SELECT * FROM schedules')
		
	finally:
		conn.close()
		
	# return schedule count
	return schedule_count


def get_schedules(password, num_schedules=None, order='random'):
	"""
	Get the schedules from the database.
	
	Args:
	  password: the database password.
	  num_schedules: the number of schedules to return, None for all.
	  order: 'random'
	  
	Return:
	  A list of decoded schedules of the form:
	   schedules: {week_number: [[home,away], [home,away], ...]}
	   year: the schedule year
	   score: the schedule score
	"""

	# a list of schedules
	schedules = None
	
	try:
		# try and get the schedules
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
		
			# fetch the schedules
			cursor.execute('SELECT * FROM schedules') # TODO always return by score
			schedules = list(cursor.fetchall())
			
			# shuffle if random
			if order == 'random':
				shuffle(schedules)
			
			# slice number of schedules
			if num_schedules is not None:
				schedules = schedules[:num_schedules]
		
	finally:
		conn.close()
		
	# return schedule count
	return decode_schedules(schedules)
	

def decode_schedules(schedules):
	"""
	Decode the schedules from the database.
	
	Args:
	  schedules: a list of schedule rows from the database, where each entry is
	    matchup to gameslot list, year, score
	
	Return:
	  A list of decoded schedules of the form:
	   schedules: {week_number: [[home,away], [home,away], ...]}
	   year: the schedule year
	   score: the schedule score
	"""
	
	# list of decoded schedules
	decoded_schedules = []
	
	# for each schedule, create a ductionary of
	for schedule in schedules:
		
		# year and score
		year = schedule[1]
		score = schedule[2]
	
		# mapping from gameslot to matchup
		gameslot_matchups = dict()
		
		# strip and split the string as store in the database
		matchups_gameslot = schedule[0].strip().split(',')
		
		# update gameslot matchups for each gameslot to [home, away] team
		for i in range(len(matchups_gameslot)):
			gameslot_matchups[int(matchups_gameslot[i])] = matchup_team[i][:]
		
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
		
		# add the decoded schedule
		decoded_schedules.append({
			'schedule': week_schedule,
			'year': year,
			'score': score
		})
	
	# return the decoded schedules
	return decoded_schedules


def get_gameslot_headers():
	"""
	Get the game slot header information
	
	Args:
	  password: the database password.
	
	Returns:
	  Gameslot header information for each game slot
	"""
	
	gameslot_header = []
	
	for week_num in range(len(num_games_per_week)):
		gameslot_header.append('Week %d - TH' % (week_num+1))
		for _ in range(num_games_per_week[week_num]-3):
			gameslot_header.append('Week %d - S' % (week_num+1))
		gameslot_header.append('Week %d - SN' % (week_num+1))
		gameslot_header.append('Week %d - MN' % (week_num+1))
	
	return gameslot_header
	
