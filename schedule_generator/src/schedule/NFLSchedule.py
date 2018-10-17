import numpy as np
from random import shuffle, randint
from schedule.score.score_calculator import get_score
from schedule.constants import teams, matchup_team, NUM_MATCHUPS, NUM_TEAMS, NUM_GAMESLOTS

class NFLSchedule:
	"""
	"""

	def __init__(self):
		"""
		Initializes an NFLSchedule object for storing matchups and associate game slots.
		"""
		
		# matchup x gameslot array
		self.matchup_gameslot = np.arange(NUM_MATCHUPS, dtype=np.uint32)
		
		# score, initially set to None and only calculate when it is called for
		#  this is because there can, most likely, be shuffling. therefore,
		#  the score should only be calculated when the user calls get_score(),
		#  assuming the user has set the schedule and is ready for the score.
		self._score = None
	
	
	def __eq__(self, other):
		"""
		Test if this NFLSchedule is equal to another NFLSchedule.

		Args:
		  other: the other NFLSchedule

		Return:
		  True if this schedule is equal to the other schedule, false othewise.
		"""
		if isinstance(other, NFLSchedule):
			return (self.matchup_gameslot == other.matchup_gameslot).all()
		else:
			return False
	
	
	def get_matchups(self):
		"""
		Gets the matchups.
		
		Return:
		  The matchups.
		"""
		return np.copy(self.matchup_gameslot)
		
	
	def set_matchups(self, matchups):
		"""
		Set the matchups for this schedule.
		
		Args:
		  matchups: a list of matchups, where index i represents the gameslot for matchup i.
		"""
		
		# set matchup array
		self.matchup_gameslot = np.array(matchups, dtype=np.uint32)
		
		# reset the score
		self._score = None
	
	
	@classmethod
	def reproduce(cls, s1, s2):
		"""
		Reproduces two schedules, in the genetic algorithm sense.
		
		Args:
		  s1: the first schedule
		  s2: the second schedule
		  
		Return:
		  A child schedule.
		"""
		
		# create a child schedule
		child = NFLSchedule()
		
		# matchup index to split between parents
		i = randint(1, NUM_MATCHUPS-1)
	
		# split the parent matchup gameslot matrix
		child.matchup_gameslot[:i] = np.copy(s1.matchup_gameslot)[:i]
		child.matchup_gameslot[i:] = np.copy(s2.matchup_gameslot)[i:]
		
		# maintain one game per game slot
		unique_values, unique_indexes = np.unique(child.matchup_gameslot, return_index=True)
		missing_values = np.setdiff1d(np.arange(NUM_GAMESLOTS), unique_values)
		missing_indexes = np.setdiff1d(np.arange(NUM_GAMESLOTS), unique_indexes)
		shuffle(missing_values)
		child.matchup_gameslot[missing_indexes] = missing_values
		
		# return the child
		return child
	
	
	def _set_home_away_matrix(self):
		"""
		Sets the home and away matrix inferred from the current matchup to gs assignment. 
		"""
		
		# reset, or initialize, the matrices
		self.hometeam_gameslot = np.zeros((NUM_TEAMS, NUM_GAMESLOTS))
		self.awayteam_gameslot = np.zeros((NUM_TEAMS, NUM_GAMESLOTS))
		
		# for each matchup, find the gameslot index, and
		#  set the home/away team index to this game slot
		for matchup_index in range(NUM_MATCHUPS):
		
			# get the game slot index where the matchup is scheduled
			gameslot_index = self.matchup_gameslot[matchup_index]
			
			# get the index of the home and away team
			home_index = matchup_team[matchup_index][0]
			away_index = matchup_team[matchup_index][1]
			
			# set the home/away team to gameslot matrix
			self.hometeam_gameslot[home_index, gameslot_index] = 1
			self.awayteam_gameslot[away_index, gameslot_index] = 1
	
	
	def shuffle(self, iterations):
		"""
		Randomly swaps matchups.
		
		Args:
		  iterations: the number of swaps to make
		"""
		
		# swap the matchups
		for i in range(iterations):
			m1 = randint(0, NUM_MATCHUPS-1)
			m2 = randint(0, NUM_MATCHUPS-1)
			self.matchup_gameslot[[m1,m2]] = self.matchup_gameslot[[m2,m1]]
		
		# need to recalculate score if shuffled at least once
		if iterations > 0:
			self._score = None
		
	
	def swap(self, i, j):
		"""
		Swap two matchups.
		
		Args:
		  i: the first matchup index
		  j: the second matchup index
		"""
		
		# swap the matchups
		self.matchup_gameslot[[i,j]] = self.matchup_gameslot[[j,i]]
		
		# need to recalculate score
		self._score = None
	
	
	def copy(self):
		"""
		Creates a copy of this schedule.
		
		Return:
		  The copied schedule
		"""
		
		# create a copy
		copy = NFLSchedule()
		
		# copy the schedule
		copy.matchup_gameslot = np.copy(self.matchup_gameslot)
		
		# copy over the error, incase it was already calculated
		copy._score = self._score
		
		# return the copy
		return copy

	
	def get_score(self):
		"""
		Calculates the score for this matchup assignment. If the score is less than 0,
		  the constraints are not yet satisfied. Once the score is greater than 0, the
		  schedule is playable based on the constraints and the score is a heuristic
		  representing the quality of the schedule.
		
		Return:
		  The score for this assignment.
		"""
		
		# only calculate it once, when it is asked for
		if self._score == None:
		
			# set the home/away team to gameslot matrix
			self._set_home_away_matrix()
			
			# calculate the score
			self._score = get_score(self)
			
		# return the score
		return self._score
	
	
	def constraints_satisfied(self):
		"""
		Return whether or not the constraints are satisfied.
		
		Return:
		  True if the constraints are satisfied, false otherwise.
		"""
		
		# get the score / compute if needed
		score = self.get_score()
		
		# if score is non negative, all constraints are satisfied
		return score >= 0
	
	
