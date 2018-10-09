import numpy as np
from random import shuffle, randint

class NFLSchedule:
	"""
	"""

	# number of games per week
	num_games_per_week = [16, 16, 16, 15, 15, 15, 14, 14, 13, 14, 13, 15, 16, 16, 16, 16, 16]
	thanksgiving_gameslots = [161,162,163]
	NUM_WEEKS = len(num_games_per_week)

	def __init__(self, teams, matchup_team):
		"""
		Initializes an NFLSchedule object for storing matchups and associate game slots.
		
		Args:
		  teams: a dictionary of team name to team index
		  all_matchups: a matrix of all matchup by home/away team index for each matchup
		"""
		
		# store the teams and matchups
		self.teams = teams
		self.matchup_team = matchup_team
		
		# number of matchups, gameslots and teams
		self.NUM_GAMESLOTS = len(self.matchup_team)
		self.NUM_MATCHUPS = len(self.matchup_team)
		self.NUM_TEAMS = len(self.teams)
		
		# matchup x gameslot array
		self.matchup_gameslot = np.arange(self.NUM_MATCHUPS, dtype=np.uint32)
		
		# error, initially set to -1 and only calculate when it is called for
		#  this is because there can, most likely, be shuffling. therefore,
		#  the error should only be calculated when the user calls get_error(),
		#  assuming the user has set the schedule and is ready for the error.
		self._error = -1
	
	
	def __eq__(self, other):
		if isinstance(other, NFLSchedule):
			return (self.matchup_gameslot == other.matchup_gameslot).all()
		else:
			return False
			
	
	@classmethod
	def init(cls, matchups_file):
		"""
		Initializes an NFLSchedule object with matchups from a file.
		
		Args:
		  matchups_file: a file containing each matchup for the upcoming season.
		"""
		
		# map from team name to team index
		teams = dict()
		with open(matchups_file, 'r') as f:
			next(f)
			for line in f:
				if line.split(',')[0].strip() not in teams:
					teams[line.split(',')[0].strip()] = len(teams)
				if line.split(',')[1].strip() not in teams:
					teams[line.split(',')[1].strip()] = len(teams)		
		
		# map from mathup index to home/away team index
		matchup_team = []
		with open(matchups_file, 'r') as f:
			next(f)
			for line in f:
				matchup_team.append([
					teams[line.split(',')[0].strip()],
					teams[line.split(',')[1].strip()]
				])
		
		# return an NFLSchedule object with the team / matchup information
		return NFLSchedule(teams, matchup_team)
	
	
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
		child = NFLSchedule(s1.teams, s1.matchup_team)
		
		# matchup index to split between parents
		i = randint(1, s1.NUM_MATCHUPS-1)
	
		# split the parent matchup gameslot matrix
		child.matchup_gameslot[:i] = np.copy(s1.matchup_gameslot)[:i]
		child.matchup_gameslot[i:] = np.copy(s2.matchup_gameslot)[i:]

		
		# maintain one game per game slot
		unique_values, unique_indexes = np.unique(child.matchup_gameslot, return_index=True)
		missing_values = np.setdiff1d(np.arange(child.NUM_GAMESLOTS), unique_values)
		missing_indexes = np.setdiff1d(np.arange(child.NUM_GAMESLOTS), unique_indexes)
		shuffle(missing_values)
		child.matchup_gameslot[missing_indexes] = missing_values
		
		# return the child
		return child
	
	
	def _set_home_away_matrix(self):
		"""
		Sets the home and away matrix inferred from the current matchup to gs assignment. 
		"""
		
		# reset, or initialize, the matrices
		self.hometeam_gameslot = np.zeros((self.NUM_TEAMS, self.NUM_GAMESLOTS))
		self.awayteam_gameslot = np.zeros((self.NUM_TEAMS, self.NUM_GAMESLOTS))
		
		# for each matchup, find the gameslot index, and
		#  set the home/away team index to this game slot
		for matchup_index in range(self.NUM_MATCHUPS):
		
			# get the game slot index where the matchup is scheduled
			gameslot_index = self.matchup_gameslot[matchup_index]
			
			# get the index of the home and away team
			home_index = self.matchup_team[matchup_index][0]
			away_index = self.matchup_team[matchup_index][1]
			
			# set the home/away team to gameslot matrix
			self.hometeam_gameslot[home_index, gameslot_index] = 1
			self.awayteam_gameslot[away_index, gameslot_index] = 1
	
	
	def shuffle(self, iterations):
		"""
		Randomly swaps matchups.
		
		Args:
		  iterations: the number of swaps to make
		"""
		
		for i in range(iterations):
			m1 = randint(0,self.NUM_MATCHUPS-1)
			m2 = randint(0,self.NUM_MATCHUPS-1)
			
			# swap the matchups
			self.matchup_gameslot[[m1,m2]] = self.matchup_gameslot[[m2,m1]]
		
		if iterations > 0:
			# need to recalculate error if shuffled at least once
			self._error = -1
		
	
	def swap(self, i, j):
		"""
		Swap two matchups.
		
		Args:
		  i: the first matchup index
		  j: the second matchup index
		"""
		
		# swap the matchups
		self.matchup_gameslot[[i,j]] = self.matchup_gameslot[[j,i]]
		
		# need to recalculate error
		self._error = -1
	
	
	def copy(self):
		"""
		Creates a copy of this schedule.
		
		Return:
		  The copied schedule
		"""
		
		# create a copy
		copy = NFLSchedule(self.teams, self.matchup_team)
		
		# copy the schedule
		copy.matchup_gameslot = np.copy(self.matchup_gameslot)
		
		# copy over the error, incase it was already calculated
		copy._error = self._error
		
		# return the copy
		return copy
		
	
	def get_error(self):
		"""
		Calculates the error for this matchup assignment.
		
		Return:
		  The error for this assignment.
		"""
		
		# only calculate it once, when it is asked for
		if self._error == -1:
		
			# set the home/away team to gameslot matrix
			self._set_home_away_matrix()
			
			# one game per team per week
			self._error = self._one_game_per_week()
			
			# Eagles first game of season at home
			self._error += self._specific_home_game(team_index=self.teams['Philadelphia Eagles'], gameslot=0)
			
			# Lions thanksgiving
			self._error += self._specific_home_game(team_index=self.teams['Detroit Lions'], gameslot=NFLSchedule.thanksgiving_gameslots[0])
			
			# Cowboys thanksgiving
			self._error += self._specific_home_game(team_index=self.teams['Dallas Cowboys'], gameslot=NFLSchedule.thanksgiving_gameslots[1])
			
		return self._error
	
	# week gameslot matrix
	week_gameslot = []
	count = 0
	for n in num_games_per_week:
		week_games = [0 for _ in range(256)]
		week_games[count:count+n] = [1 for _ in range(n)]
		count += n
		week_gameslot.append(week_games)
	gameslot_week = np.array(week_gameslot, dtype=np.uint32).T
	def _one_game_per_week(self):
		"""
		Gets the number of violations of the one game per team per week constraint.
		
		Return:
		  The number of violations of the one game per team per week constraint.
		"""
		
		return np.sum(np.where(np.matmul(self.hometeam_gameslot, NFLSchedule.gameslot_week) + np.matmul(self.awayteam_gameslot, NFLSchedule.gameslot_week) != 1, 1, 0)) - self.NUM_TEAMS
	
	
	def _specific_home_game(self, team_index, gameslot):
		"""
		Enforce that the first game of the year is at home for the Super Bowl champs.
		
		Return:
		  1 if the super bowl champ is not starting the season at home.
		"""
		
		return 1 if self.hometeam_gameslot[team_index][gameslot] != 1 else 0
	
