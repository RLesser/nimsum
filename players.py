import random

class Player(object):
	"""docstring for Player"""
	def __init__(self, playerNumber):
		super(Player, self).__init__()
		self.playerNumber = playerNumber
		self.setName()

	def setName(self):
		pass

	def takeAmount(self, colorDict, playerList, printMode):
		pass


class HumanPlayer(Player):
	"""docstring for HumanPlayer"""
	# figure out why this argument cant be in the super class
	def __init__(self, playerNumber):
		super(HumanPlayer, self).__init__(playerNumber)


	def setName(self):
		self.name = raw_input("Enter player name: ")


	def takeAmount(self, colorDict, playerList, printMode):
		color = raw_input("[" + self.name + "] Enter color to be picked: ")
		amount = int(raw_input("Enter amount to take of that color: "))
		return color, amount


class RandomBot(Player):
	"""docstring for RandomBot"""
	def __init__(self, playerNumber):
		super(RandomBot, self).__init__(playerNumber)


	def setName(self):
		self.name = "RandomBot-" + str(self.playerNumber)
		
	def takeAmount(self, colorDict, playerList, printMode):
		self.printMode = printMode
		return self.randomChoice(colorDict)
		

	def randomChoice(self, colorDict):
		remainingColors = [color for color in colorDict if colorDict[color] > 0]
		chosenColor = remainingColors[random.randint(0,len(remainingColors)-1)]
		chosenAmount = random.randint(1,colorDict[chosenColor])
		if self.printMode:
			print "[RandomBot-" + str(self.playerNumber) + "]",
			print " Enter color to be picked: ", chosenColor
			print "Enter amount to take of that color: ", chosenAmount
		return chosenColor, chosenAmount


class SmartBotV1(RandomBot):
	"""docstring for SmartBotV1"""
	def __init__(self, playerNumber):
		super(SmartBotV1, self).__init__(playerNumber)


	def setName(self):
		self.name = "SmartBotV1-" + str(self.playerNumber)


	def takeAmount(self, colorDict, playerList, printMode):
		self.printMode = printMode

		# Rule 1: If only one pile remaining, take all of that pile
		remainingColors = [color for color in colorDict if colorDict[color] > 0]
		if len(remainingColors) == 1:
			return remainingColors[0], colorDict[remainingColors[0]]
		
		return self.randomChoice(colorDict)
