from src.genetic_algorithm import genetic_algorithm
from src.NFLSchedule import NFLSchedule
		
if __name__ == '__main__':

	# base schedule so only one read
	base = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
	
	genetic_algorithm(base)
