import numpy as np
from random import random, randint
from NFLSchedule import NFLSchedule

def genetic_algorithm():

	# population size
	pop_size = 128

	a = np.arange(pop_size)[::-1]
	a =  a / np.sum(a)
	def get_parent_index():
		x = random()
		for i in range(pop_size):
			x -= a[i]
			if x < 0:
				return i
		return 0

	# base schedule so only one read
	base = NFLSchedule.init('nfl-matchups_2018.csv')
	
	# current random population
	population = [base.copy() for _ in range(pop_size)]
	for individual in population:
		individual.shuffle(100)
	population = sorted(population, key=lambda x: x.get_error())
	count = 0
	
	while True:
		m = min([i.get_error() for i in population])
		if m == 0:
			break
		else:
			print('%d - %d  %d'%(m, max([i.get_error() for i in population]), count))
		# new population
		new_population = [population[0]]
		
		for _ in range(pop_size-len(new_population)):
			parent1 = population[get_parent_index()]
			parent2 = population[get_parent_index()]
			child = NFLSchedule.reproduce(parent1, parent2)
			if random() < 0.5:
				child.shuffle(1)
			new_population.append(child)
		population = new_population
		population = sorted(population, key=lambda x: x.get_error())
				
		
if __name__ == '__main__':
	genetic_algorithm()

		
