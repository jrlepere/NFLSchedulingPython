
class OpenerFilter:

	def __init__(self, opener, matchup_team):
	
		self.opener = opener
		self.matchup_team = matchup_team

	def filter(self, gameslot_matchups):	
		return self.matchup_team[gameslot_matchups[0]][1] == self.opener
