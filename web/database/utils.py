import pymysql

# connection information
host='nflschedules.cd7ko38smnnq.us-west-1.rds.amazonaws.com'
port=3306
dbname='nflschedules'
user='nflschedules'


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
			schedules = cursor.fetchall()[:num_schedules]
		
	finally:
		conn.close()
		
	# return schedule count
	return schedules
