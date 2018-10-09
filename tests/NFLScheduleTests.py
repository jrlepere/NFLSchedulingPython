from tests.context import src
from src.NFLSchedule import NFLSchedule

def test_NFLScheduleEquality():
	"""
	Test NFLSchedule == NFLSchedule.
	"""
	
	# init
	s1 = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	s2 = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
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
	s = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
	# test error is 0
	assert s.get_error() == 0


def test_swap():
	"""
	Test swap function.
	"""
	
	# init
	s1 = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	s2 = NFLSchedule.init('./resources/nfl-matchups_2018.csv')
	
	# test swap same
	s1.swap(0,1)
	s2.swap(1,0)
	assert s1 == s2
	
	# test swap not equal
	s1.swap(10,20)
	assert s1 != s2

