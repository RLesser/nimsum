import players

class Game(object):
	"""docstring for Game"""
	def __init__(self, colorDict, playerList):
		super(Game, self).__init__()
		self.colorDict = colorDict
		self.playerList = playerList
		self.round = 1

	def playGame(self, printMode = True):
		outcome = None
		self.printMode = printMode
		while outcome == None:
			outcome = self.playRound()
		return outcome


	def playRound(self):
		for p in self.playerList:
			if self.printMode:
				self.printGameInfo()
			while True:
				color, amount = p.takeAmount(self.colorDict, 
											 self.playerList, 
											 self.printMode)
				try:
					self.removeColorAmount(color, amount)
				except Exception as e:
					print e
					if e == ValueError:
						print "Tried to remove too many colors!"
					if e == KeyError:
						print "Invalid color!"
				else:
					break
			if sum([self.colorDict[color] for color in self.colorDict]) == 0:
				return self.endGame(p.name, p.playerNumber)
		self.round += 1

	def printGameInfo(self):
		for color in self.colorDict:
			print color, self.colorDict[color]

	def removeColorAmount(self, color, amount):
		if self.colorDict[color] < amount:
			raise ValueError
		self.colorDict[color] -= amount 

	def endGame(self, winnerName, playerNumber):
		if self.printMode:
			print winnerName, "is the winner!"
		return playerNumber
