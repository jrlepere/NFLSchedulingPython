"""
Deletes schedules from the database if the score is less than 0 (in violation) or
 if there exists an identical schedules. That is, if there is a schedule with the
 same permuation of sunday games for each week.
"""

import pymysql
import argparse
from schedule.NFLSchedule import NFLSchedule

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
			if schedule.get_score() < 0 or schedule in schedules:
				cursor.execute('DELETE FROM schedules WHERE schedule="%s" AND year="%s"' % (matchup[0], matchup[1]))
			else:
				schedules.append(schedule)
		conn.commit()
finally:
	conn.close()
	
