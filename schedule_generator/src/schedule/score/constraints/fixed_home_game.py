
def fixed_home_game(schedule, team, gameslot):
	"""
	Enforce that a team has a homegame at the gameslot.
	
	Args:
	  schedule: the schedule object
	  team: the index of the team
	  gameslot: the game slot

	Return:
	  0 if the team has a home game at the gameslot, 1 otherwise
	"""
	
	return 0 if schedule.hometeam_gameslot[team][gameslot] == 1 else 1
