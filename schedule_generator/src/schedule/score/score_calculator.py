from schedule.score.constraints.one_game_per_week import one_game_per_week
from schedule.score.constraints.fixed_matchup import fixed_matchup
from schedule.score.constraints.fixed_home_game import fixed_home_game
from schedule.score.constraints.shared_stadium import shared_stadium
from schedule.constants import get_matchup_index, london_games, mexico_games, thanksgiving_gameslots

def get_score(schedule):
	"""
	Calculates the score for the schedule.
	
	Args:
	  schedule: the schedule object
	
	
	Return:
	  The score for the schedule. If the score is negative, then the
	  constraints are not yet satisfied. Otherwise, the score is
	  a heuristic representing the quality of the schedule.
	"""
	
	# get the number of constraint violations
	constraint_violations = get_constraints(schedule)
	
	# if at least one constraint it in violation, return the score
	#  as the negative of the number of violations.
	if constraint_violations > 0:
		return -constraint_violations
	
	# otherwise, return the positive heuristic value
	return get_heuristic(schedule)
	

def get_constraints(schedule):
	"""
	Gets the number of constraints on the schedule.
	
	Args:
	  schedule: the schedule object
	
	Return:
	  The number of constraints the schedule is violating.
	"""
	
	constraint_violations  = one_game_per_week(schedule)
	constraint_violations += fixed_matchup(schedule,
								get_matchup_index("Oakland Raiders", "Seattle Seahawks"),
								london_games[0])
	constraint_violations += fixed_matchup(schedule,
								get_matchup_index("Los Angeles Chargers", "Tennessee Titans"),
								london_games[1])
	constraint_violations += fixed_matchup(schedule,
								get_matchup_index("Jacksonville Jaguars", "Philadelphia Eagles"),
								london_games[2])
	constraint_violations += fixed_matchup(schedule,
								get_matchup_index("Los Angeles Rams", "Kansas City Chiefs"),
								mexico_games[0])
	constraint_violations += fixed_home_game(schedule, "Philadelphia Eagles", 0)
	constraint_violations += fixed_home_game(schedule, "Detroit Lions", thanksgiving_gameslots[0])
	constraint_violations += fixed_home_game(schedule, "Dallas Cowboys", thanksgiving_gameslots[1])
	constraint_violations += shared_stadium(schedule, "New York Jets", "New York Giants")
	
	return constraint_violations
	

def get_heuristic(schedule):
	"""
	Gets a heuristic for the schedule.
	
	Args:
	  schedule: the schedule object
	
	Return:
	  The heuristic calculation for the schedule.
	"""
	
	return 0
