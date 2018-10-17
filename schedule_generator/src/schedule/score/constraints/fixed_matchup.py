
def fixed_matchup(schedule, matchup, gameslot):
	"""
	Enforce that a matchup be played at a gameslot.
	
	Args:
	  schedule: the schedule object
	  matchup: the matchup index
	  gameslot: the gameslot index
	
	Return:
	  0 if the matchup is schedule for the gameslot, 1 otherwise.
	"""
	return 0 if schedule.matchup_gameslot[matchup] == gameslot else 1
