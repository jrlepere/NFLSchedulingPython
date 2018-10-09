import numpy as np
from random import random, randint, uniform, shuffle
from src.NFLSchedule import NFLSchedule
from math import sqrt

def genetic_algorithm(base, pop_size=128, elitist=16):
	
	# gets the reproduction probability for the current population
	def get_reproduction_probability(population):
		a = []
		for i in range(len(population)):
			if i == 0:
				a.append(1)
			else:
				if population[i].get_error() == population[i-1].get_error():
					a.append(a[-1])
				else:
					a.append(a[-1]+1)
		a = [a[-1]/i for i in a]
		sum_a = sum(a)
		return [i/sum_a for i in a]
	
	# reproduction probability
	def get_parent_index(a):
		x = uniform(0, 1)
		for i in range(pop_size):
			x -= a[i]
			if x < 0:
				return i
		return 0
	
	# initial random population
	population = [base.copy() for _ in range(pop_size)]
	for individual in population:
		individual.shuffle(256)
	population = sorted(population, key=lambda x: x.get_error())
	reproduction_probability = get_reproduction_probability(population)
	
	while True:
	
		# minimum error
		m = population[0].get_error()
		if m == 0:
			break
			
		# new population, elitist
		new_population = []
		for individual in population:
			if individual.get_error() == m:
				if individual not in new_population:
					new_population.append(individual)
					if len(new_population) == elitist:
						break
			else:
				break
		print('%3d - %3d - %3d'%(m, population[-1].get_error(), len(new_population)))
		
		# populate next generation
		for _ in range(pop_size-len(new_population)):
			
			# asexual reproduction
			child = population[get_parent_index(reproduction_probability)].copy()
			
			# mutation
			r = random()
			if r < 0.9:
				child.shuffle(1)
			elif r < 0.99:
				child.shuffle(2)
			else:
				child.shuffle(3)
				
			# populate
			new_population.append(child)
		
		# shuffle the population so we do not retain the same elitists
		shuffle(new_population)
		
		# set new population and sort by error
		population = new_population
		population = sorted(population, key=lambda x: x.get_error())
		reproduction_probability = get_reproduction_probability(population)
				


		
