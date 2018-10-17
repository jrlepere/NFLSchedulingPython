from schedule.constants import gameslot_week, NUM_WEEKS, num_games_per_week
import numpy as np

def shared_stadium(schedule, team1, team2):
	"""
	Constraint that two teams cannot have home games in the same week.

	Args:
	  schedule: the schedule object
	  team1: the index of the first team
	  team2: the index of the second team

	Return:
	  The number of violations.
	"""
	
	# compute hometeam by week matrix
	hometeam_week = np.matmul(schedule.hometeam_gameslot, gameslot_week)
	
	# extract home games per week for each team
	hometeam_week_team1 = hometeam_week[team1]
	hometeam_week_team2 = hometeam_week[team2]
	
	# element wise multiplication, if 1 then home game in same week
	home_same_week = hometeam_week_team1 * hometeam_week_team2

	# validate distance between games, ie if team plays home Thursday or Monday, it is okay
	#  for both teams to play home games in the same week
	gs_count = 0
	for week_num in range(NUM_WEEKS-1): # skip week 17, as all teams play on Sunday
		
		# thursday check
		if schedule.hometeam_gameslot[team1][gs_count] or schedule.hometeam_gameslot[team2][gs_count]:
			home_same_week[week_num] = 0
		
		# increment number of games
		gs_count += num_games_per_week[week_num]
		
		# monday check
		if schedule.hometeam_gameslot[team1][gs_count-1] or schedule.hometeam_gameslot[team2][gs_count-1]:
			home_same_week[week_num] = 0
	
	# return total violations
	return np.sum(home_same_week)
