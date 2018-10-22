from schedule.constants import matchup_team, gameslot_week, NUM_TEAMS, NUM_WEEKS, international_gameslots
import numpy as np

def no_bye_after_international(schedule):
	"""
	Counts the number of times a team playing in an international game does not
	 have a bye the following week.
	
	Args:
	  schedule: the schedule
	
	Return:
	  The number of times a team does not have a bye following an international game.
	"""
	
	# team x week matrix
	team_week = (np.matmul(schedule.hometeam_gameslot, gameslot_week) +
				 np.matmul(schedule.awayteam_gameslot, gameslot_week))
	
	# count of time international teams don't have a bye the following week
	count = 0
	
	for gs in international_gameslots:
		teams = matchup_team[schedule.gameslot_matchup[gs]]
		week_num = np.argwhere(gameslot_week[gs])[0][0]
		if week_num < NUM_WEEKS - 1:
			if team_week[teams[0]][week_num+1] != 0:
				count += 1
			if team_week[teams[1]][week_num+1] != 0:
				count += 1
	
	return count
