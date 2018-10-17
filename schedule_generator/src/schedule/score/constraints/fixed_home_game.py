from schedule.constants import teams

def fixed_home_game(schedule, team_name, gameslot):
	"""
	Enforce that a team has a homegame at the gameslot.
	
	Args:
	  schedule: the schedule object
	  team_name: the name of the team
	  gameslot: the game slot

	Return:
	  0 if the team has a home game at the gameslot, 1 otherwise
	"""
	
	return 0 if schedule.hometeam_gameslot[teams[team_name]][gameslot] == 1 else 1
