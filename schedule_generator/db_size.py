import pymysql
import argparse

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
	# print the number of rows in the database
	conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
	with conn.cursor() as cursor:
		print(cursor.execute('SELECT * FROM schedules'))
	
finally:
	conn.close()
	
