import cPickle

class HighScore():
	def __init__(self, score=0, name=""):
		self.score = score
		self.name = name
	
	def __cmp__(self, other):
		if self.score > other.score:
			return -1
		elif self.score < other.score:
			return 1
		else:
			return 0
			
class HighScoreTable():
	def __init__(self, list=[]):
		self.scores = sorted(list)
		while len(self.scores) < 10:
			self.scores.append(HighScore())
	
	def addScore(self, score):
		self.scores.append(score)
		self.scores.sort()
		if len(self.scores) > 10:
			self.scores.pop()
		
		hsfile = open('highScores.dat', 'w')
		pickler = cPickle.Pickler(hsfile)
		table = self
		cPickle.dump(table, hsfile)
		
	def __str__(self):
		ret = ""
		for i in self.scores:
			ret += i.name + ": " + str(i.score) + "\n"
		return ret
		