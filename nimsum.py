#!/usr/bin/python

'''
Rules of Nim Sum

Set of objects, of a set amount of colors

2 player game

players take turns taking as many objects as they want all of one color

goal is to be the last one to pick up

'''

import random

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
				color, amount = p.takeAmount(self.colorDict, self.playerList, self.printMode)
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
	


def retrieveColorDict(autoRandom = False):
	colorDict = {}
	while True:
		if autoRandom:
			retrievalMethod = 'random'
		else:
			retrievalMethod = raw_input('Enter game info retrieval method' + 
										'[input/file/random]: ')

		if retrievalMethod == 'input':
			done = False
			while not done:
				color = raw_input("Enter color (or 'exit' to end list): ")
				if color == 'exit':
					done = True
				else:
					amount = int(raw_input("Enter amount for " + color + ": "))
					colorDict[color] = amount
			break

		if retrievalMethod == 'file':
			filename = raw_input('Enter filename: ')
			with open(filename, 'rb') as f:
				for line in f.readlines():
					color = line.split(',')[0].strip()
					amount = int(line.split(',')[1].strip())
					colorDict[color] = amount
			break

		if retrievalMethod == 'random':
			allColors = ['blue', 'red', 'yellow', 'green', 'purple', 'orange']
			colors = allColors[0:random.randint(3,6)]
			for color in colors:
				amount = random.randint(3,10)
				colorDict[color] = amount
			break
		print "Invalid method"
	return colorDict


def main():
	playerNum = int(raw_input("Enter number of players: "))
	playerList = []
	playersAdded = 0
	humanInvolved = False
	while playersAdded < playerNum:
		playersAdded += 1
		playerType = raw_input("Enter player type [human/random/smartv1]: ")
		if playerType == 'human':
			humanInvolved = True
			p = HumanPlayer(playersAdded)
			playerList.append(p)
		elif playerType == 'random':
			p = RandomBot(playersAdded)
			playerList.append(p)
		elif playerType == 'smartv1':
			p = SmartBotV1(playersAdded)
			playerList.append(p)
		else:
			playersAdded -= 1
			print "Incorrect player type"

	if not humanInvolved:
		sim = ('y' == raw_input("No humans are playing. Running simulation? (y/n) "))
		if sim:
			trailCount = int(raw_input("Enter number of trials: "))
			winnerCounts = [0 for x in playerList]
			count = 0
			while count < trailCount:
				colorDict = retrieveColorDict(autoRandom = True)
				G = Game(colorDict, playerList)
				winnerCounts[G.playGame(printMode = False)-1] += 1
				count += 1

			print winnerCounts
	else:
		colorDict = retrieveColorDict()
		G = Game(colorDict, playerList)
		G.playGame()


if __name__ == '__main__':
	main()	


