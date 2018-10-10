from src.genetic_algorithm import genetic_algorithm
from src.NFLSchedule import NFLSchedule
import csv

if __name__ == '__main__':

	# base schedule so only one read
	base = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
	# get schedules
	schedules = genetic_algorithm(base, pop_size=128, num_elitist=16, num_results=1000)
	
	# result filename
	result_filename = './results/results.csv'
	
	# write the results
	with open(result_filename, 'a+') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for s in schedules:
			writer.writerow(s.get_matchups())
	
