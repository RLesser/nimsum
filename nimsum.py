#!/usr/bin/python

'''
Rules of Nim Sum

Set of objects, of a set amount of colors

2 player game

players take turns taking as many objects as they want all of one color

goal is to be the last one to pick up

'''

import random
import players
from game import Game

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
			p = players.HumanPlayer(playersAdded)
			playerList.append(p)
		elif playerType == 'random':
			p = players.RandomBot(playersAdded)
			playerList.append(p)
		elif playerType == 'smartv1':
			p = players.SmartBotV1(playersAdded)
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


