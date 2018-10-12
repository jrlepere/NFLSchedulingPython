import pymysql


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


def get_schedules(password, num_schedules=None):
	"""
	Get the schedules from the database.
	
	Args:
	  password: the database password.
	  num_schedules: the number of schedules to return, None for all.
	  
	Return:
	  The number of schedules in the database.
	"""

	# a list of schedules
	schedules = None
	
	try:
		# try and get the schedules
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		with conn.cursor() as cursor:
			cursor.execute('SELECT * FROM schedules')
			schedules = cursor.fetchall()
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
	  The decoded schedules.
	"""
	
	decoded_schedules = []
	
	for schedule in schedules:
		gameslot_matchups = dict()
		matchups_gameslot = schedule[0].strip().split(',')
		for i in range(len(matchups_gameslot)):
			gameslot_matchups[matchups_gameslot[i]] = matchup_team[i]
		decoded_schedules.append({
			'schedule': [gameslot_matchups[i] for i in sorted(gameslot_matchups)],
			'year': schedule[1],
			'score': schedule[2]
		})
	
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
	
