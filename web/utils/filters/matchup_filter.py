
class MatchupFilter:

	def __init__(self, matchup, gameslot, matchup_team):
	
		self.matchup = matchup
		self.gameslot = gameslot
		self.matchup_team = matchup_team

	def filter(self, gameslot_matchups):	
		return self.matchup_team[gameslot_matchups[self.gameslot]] == self.matchup
