import numpy as np
from random import shuffle, randint
from schedule.score.score_calculator import get_score
from schedule.constants import teams, matchup_team, NUM_MATCHUPS, NUM_TEAMS, NUM_GAMESLOTS, NUM_WEEKS, num_games_per_week, thanksgiving_gameslots

class NFLSchedule:
	"""
	"""

	def __init__(self):
		"""
		Initializes an NFLSchedule object for storing matchups and associate game slots.
		"""
		
		# matchup x gameslot array
		self.matchup_gameslot = np.arange(NUM_MATCHUPS, dtype=np.uint32)
		
		# gameslot to matchup
		self.gameslot_matchup = [0 for _ in range(NUM_GAMESLOTS)]
		self._set_gameslot_matchup()
		
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
			
			# order of Sunday games does not matter
			gs_count = 0
			for week_num in range(NUM_WEEKS-1): # skip week 17
				
				# Thursday night check
				if gs_count != thanksgiving_gameslots[0]:
					s = gs_count+1
					if self.gameslot_matchup[gs_count] != other.gameslot_matchup[gs_count]:
						return False
				else:
					s = gs_count+3
					if (self.gameslot_matchup[gs_count] != other.gameslot_matchup[gs_count]) or (self.gameslot_matchup[gs_count+1] != other.gameslot_matchup[gs_count+1]) or (self.gameslot_matchup[gs_count+2] != other.gameslot_matchup[gs_count+2]):
						return False
				# increment gameslot counter
				gs_count += num_games_per_week[week_num]
				
				# Sunday day check
				if not (sorted(self.gameslot_matchup[s:gs_count-2]) == sorted(other.gameslot_matchup[s:gs_count-2])):
					return False
				
				# Sunday night check
				if self.gameslot_matchup[gs_count-2] != other.gameslot_matchup[gs_count-2]:
					return False
				
				# Monday night check
				if self.gameslot_matchup[gs_count-1] != other.gameslot_matchup[gs_count-1]:
					return False
				
			return True
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
		
		# reset gameslot to matchup
		self._set_gameslot_matchup()
		
		# reset the score
		self._score = None
	
	
	def _set_gameslot_matchup(self):
		"""
		Sets the gameslot to matchup array for efficient equality check.
		"""
		for i in range(NUM_MATCHUPS):
			self.gameslot_matchup[self.matchup_gameslot[i]] = i
	
	
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
		
		# reset gameslot to matchup
		child._set_gameslot_matchup()
		
		# reset the score
		child._score = None
		
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
			g1 = self.matchup_gameslot[m1]
			g2 = self.matchup_gameslot[m2]
			self.matchup_gameslot[[m1,m2]] = self.matchup_gameslot[[m2,m1]]
			self.gameslot_matchup[g2] = m1
			self.gameslot_matchup[g1] = m2
		
		if iterations > 0:
			# reset the score
			self._score = None
		
	
	def swap(self, m1, m2):
		"""
		Swap two matchups.
		
		Args:
		  m1: the first matchup index
		  m2: the second matchup index
		"""
		
		# swapped gameslots
		g1 = self.matchup_gameslot[m1]
		g2 = self.matchup_gameslot[m2]
		
		# swap the matchups
		self.matchup_gameslot[[m1,m2]] = self.matchup_gameslot[[m2,m1]]
		
		# reset gameslot to matchup
		self.gameslot_matchup[g2] = m1
		self.gameslot_matchup[g1] = m2
		
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
		
		# reset gameslot to matchup
		copy.gameslot_matchup = self.gameslot_matchup[:]
		
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
	
	
