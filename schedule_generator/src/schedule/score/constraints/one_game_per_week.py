from schedule.constants import gameslot_week, NUM_TEAMS
import numpy as np

def one_game_per_week(schedule):
	"""
	Gets the number of violations for the constraint that each team can
	have only one game per week and one bye week.
	
	Args:
	  schedule: the schedule object
	
	Return:
	  The number of violations for the constraint.
	"""
	
	return np.sum(
				np.where(
					np.matmul(schedule.hometeam_gameslot, gameslot_week) +
					np.matmul(schedule.awayteam_gameslot, gameslot_week)
					!= 1, 1, 0
				)
			) - NUM_TEAMS

