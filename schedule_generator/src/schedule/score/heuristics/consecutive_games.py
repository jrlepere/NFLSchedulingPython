from schedule.constants import gameslot_week, NUM_TEAMS, NUM_WEEKS
import numpy as np

def consecutive_road_games(schedule):
	"""
	Count the total number of times a team has 3 or more consecutive road games.
	
	Args:
	  schedule: the schedule
	
	Return:
	  The total number of times a teams has 3 or more consecutive road games
	"""
	
	# get away team by week matrix
	awayteam_week = np.matmul(schedule.awayteam_gameslot, gameslot_week)
	
	# count number of times a team has 3 consecutive road games
	count = 0
	for team in range(NUM_TEAMS):
		for week in range(NUM_WEEKS-2):
			if (awayteam_week[team][week] == 1 and
				awayteam_week[team][week+1] == 1 and
				awayteam_week[team][week+2] == 1):
				count += 1
				
	return count
	
