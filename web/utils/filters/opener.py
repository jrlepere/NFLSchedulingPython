

class OpenerFilter:

	def __init__(self, opener):
	
		self.opener = opener

	def filter(self, schedule):	
		return schedule['schedule'][1][0][1] == self.opener
