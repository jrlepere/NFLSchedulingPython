import numpy as np
from random import random, randint, uniform, shuffle
from src.NFLSchedule import NFLSchedule
from math import sqrt

def genetic_algorithm(base, pop_size=128, num_elitist=16, num_results=100):
	"""
	Try and find num_results unique playable schedules using the genetic algorithm.
	
	Args:
	  base: a base schedule to copy from
	  pop_size: the size of the population
	  num_elitist: the number of unique elitist to retain for each generation
	  num_results: the number of unique schedules to return
	
	Return:
	  A list of playable schedules.
	"""
	
	# gets the reproduction probability for the current population
	def get_reproduction_probability(population):
	
		# probability result
		a = []
		
		# for each population index
		for i in range(len(population)):
			if i == 0:
				# rank of 1 for the first individual
				a.append(1)
			else:
				if population[i].get_score() == population[i-1].get_score():
					# score if the same as the previous, give the same rank
					a.append(a[-1])
				else:
					# add increment rank
					a.append(a[-1]+1)
					
		# invert the rankings with respect to the maximum
		a = [a[-1]/i for i in a]
		
		# return as probability
		sum_a = sum(a)
		return [i/sum_a for i in a]
	
	# gets parent index from reproduction probability
	def get_parent_index(a):
		x = random()
		for i in range(pop_size):
			x -= a[i]
			if x < 0:
				return i
		return 0
	
	# initial random population
	population = [base.copy() for _ in range(pop_size)]
	for individual in population:
		individual.shuffle(256)
	population = sorted(population, key=lambda x: x.get_score(), reverse=True)
	reproduction_probability = get_reproduction_probability(population)
	
	# results
	res = []
	
	# populate results
	while len(res) < num_results:
		
		# get the maximum score
		m = population[0].get_score()
		
		# new population, elitist
		new_population = []
		for individual in population:
			if individual.get_score() == m:
				if individual not in new_population:
					new_population.append(individual)
					if len(new_population) == num_elitist:
						break
			else:
				break
		print('%3d - %3d - %3d'%(m, population[-1].get_score(), len(new_population)))
		
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
		population = sorted(population, key=lambda x: x.get_score(), reverse=True)
		reproduction_probability = get_reproduction_probability(population)
		
		# add to results if constraints satisfied
		for individual in population:
			if not individual.constraints_satisfied():
				break
			if individual not in res:
				res.append(individual)
	
	# return the results
	return res
