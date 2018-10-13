from src.genetic_algorithm import genetic_algorithm
from src.NFLSchedule import NFLSchedule
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
parser.add_argument('-s',
            dest='seed',
            required=False,
            type=bool,
            help='True for highest scoring seed, False for random seed')
args = parser.parse_args()

# connection information
host='nflschedules.cd7ko38smnnq.us-west-1.rds.amazonaws.com'
port=3306
dbname='nflschedules'
user='nflschedules'
password=args.password

if __name__ == '__main__':

	# base schedule so only one read
	base = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
	# shuffles to make for each individual in the initial population
	init_shuffles = 256
	
	# set the base matchups to one from the database
	if args.seed is not None:
		# TODO fetch highest score
		try:
			# connect to the database
			conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
			with conn.cursor() as cursor:
				# get all matchups from the database, select one at random and set to the base
				cursor.execute('SELECT * FROM schedules')
				all_matchups = cursor.fetchall()
				matchup = all_matchups[randint(0,len(all_matchups)-1)][0]
				base.set_matchups([int(i) for i in matchup.split(',')])
				init_shuffles = 0
		finally:
			conn.close()
	
	# get schedules
	schedules = genetic_algorithm(base, pop_size=128, num_elitist=16, num_results=1000, init_shuffles=init_shuffles)
	
	# try and write to database
	try:
		
		# connect to the database
		conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
		
		# sql command
		sql = 'INSERT INTO schedules (schedule, year, score) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE score=%s'
		
		# write each schedule to database
		for schedule in schedules:
			with conn.cursor() as cursor:
				cursor.execute(sql, (",".join(map(str,schedule.get_matchups().tolist())), '2018', '100', '100'))
	
		# commit
		conn.commit()
	
	# save the results to a csv if there was an error
	except:
		
		# result filename
		result_filename = './results/results.csv'

		# write the results
		with open(result_filename, 'a+') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for schedule in schedules:
				writer.writerow(schedule.get_matchups())
	
	finally:
		
		# close the connection
		conn.close()
	
