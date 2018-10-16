from tests.context import src
from src.NFLSchedule import NFLSchedule

# base object so only one read of file
base = NFLSchedule.init('./resources/nfl-matchups_2018.csv')

# known acceptable matchup to gameslot allocation
known_acceptable_matchup = [98,99,238,174,102,251,66,241,69,42,218,159,
	88,245,150,101,169,229,185,195,171,204,79,205,31,15,226,
	39,187,198,228,18,223,184,83,14,59,21,122,10,34,206,73,24,
	46,38,201,149,43,37,28,178,52,70,74,16,200,254,151,168,104,57,
	61,91,113,40,164,26,48,49,215,114,75,72,126,199,143,77,44,27,250,
	249,22,3,87,179,50,108,5,203,177,144,139,219,146,227,55,230,217,116,
	148,170,63,221,130,84,210,214,172,153,133,243,134,211,197,152,248,173,
	56,239,7,208,193,115,13,186,103,2,60,190,82,196,123,162,47,32,165,212,242,
	30,23,176,107,225,234,147,0,247,213,119,183,155,76,4,207,160,17,138,120,
	86,220,161,53,80,233,105,121,142,194,135,45,141,94,235,154,106,112,145,246,
	128,95,64,11,1,209,117,8,6,132,240,12,216,35,51,124,81,62,192,253,166,36,232,
	157,65,67,244,167,163,9,33,92,78,137,189,90,96,125,100,181,188,109,29,54,129,
	136,231,222,58,85,202,71,68,156,237,111,158,255,140,224,20,25,89,252,175,19,191,
	93,97,41,110,127,236,118,182,131,180]


def test_NFLScheduleEquality():
	"""
	Test NFLSchedule == NFLSchedule.
	"""
	
	# init
	s1 = base.copy()
	s2 = base.copy()
	
	# test equality
	assert s1 == s2
	
	# test not equal after shuffle
	s2.shuffle(5)
	assert s1 != s2


def test_NFLScheduleAcceptable():
	"""
	Test an acceptable NFL schedule. Since the order of our file is the actual schedule, it must be acceptable.
	"""
	
	# init actual schedule
	s = base.copy()
	assert s.constraints_satisfied()
	
	# known correct
	s.set_matchups(known_acceptable_matchup)
	assert s.constraints_satisfied()


def test_swap():
	"""
	Test swap function.
	"""
	
	# init
	s1 = base.copy()
	s2 = base.copy()
	
	# test swap same
	s1.swap(0,1)
	s2.swap(1,0)
	assert s1 == s2
	
	# test swap not equal
	s1.swap(10,20)
	assert s1 != s2


def test_same_home_team_week():
	"""
	Test the same_home_team_week constraint
	"""

	# init actual schedule
	s = base.copy()
	s._set_home_away_matrix()
	# week 15 Jets are on a Saturday and Giants are on Sunday
	#  which we do not account for in the algorithm,
	#  so 1 violation is expected
	assert s._home_game_same_week(s.teams['New York Giants'], s.teams['New York Jets']) == 1


