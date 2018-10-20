from solver.genetic_algorithm import genetic_algorithm
from schedule.NFLSchedule import NFLSchedule
import csv
import pymysql
import argparse
from random import randint

# argument parser for password
parser = argparse.ArgumentParser(description='Supply the password.')
parser.add_argument('-p',
            dest='password',
            required=True,
            type=str,
            help='the rds password')
args = parser.parse_args()

# connection information
host='nflschedules.cd7ko38smnnq.us-west-1.rds.amazonaws.com'
port=3306
dbname='nflschedules'
user='nflschedules'
password=args.password

sql = 'INSERT INTO schedules (schedule, year, score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE score=%s'

try:
	conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
	with conn.cursor() as cursor:
		cursor.execute('SELECT * FROM schedules')
		all_matchups = list(cursor.fetchall())
		base = NFLSchedule()
		schedules = []
		for matchup in all_matchups:
			schedule = NFLSchedule()
			schedule.set_matchups([int(i) for i in matchup[0].split(',')])
			with conn.cursor() as cursor:
				cursor.execute(sql, (",".join(map(str,schedule.get_matchups().tolist())), '2018', schedule.get_score(), schedule.get_score()))
		conn.commit()
finally:
	conn.close()
	
