"""
A file for running a tournament, pitting differently weighted evaluation functions aganst each other to determine which performs best against the strategy agent.
"""

from game import Game
from game import runGames
from random import random
from TournamentExpectimaxAgent import TournamentExpectimaxAgent

# import sys

# from Agent import RandomAgent
# from Deck import Deck
# from Hand import Hand
# from GameState import GameState
# from MCTSAgent import MCTSAgent
# from Player import Player
# from ExpectimaxAgentOne import ExpectimaxAgentOne
# from ExpectimaxAgentTwo import ExpectimaxAgentTwo
# from Agent import StrategyAgent

# TODO: create agents w/ diff random sets of weights

listOfFeatures = ['p1NumCards', 'p2NumCards', 'lNumCards', 'lBestSingle', 'lWorstSingle', 'lBestDouble', 'lBestTriple', 'lBestSequence', 'lTurnNewRound']

# list of 2^n agents to be used. we will remove losers until there is one winner left
agents = []
for i in range(8):
    newWeights = {}
    for feature in listOfFeatures:
        newWeights[feature] = random() * 10
    # append agent with these weights to Agents

# store losers and how many games they won
losers = [] # in order of [2nd, 3-4, 3-4, 5-8, 5-8, 5-8, 5-8, ...]
# populate agents

N = len(agents)
winsOfWinner = 0
while N > 1:
    size = len(agents)
    # play agents i and i+1 against the strategy agent. winner moves on
    # (iterate over list in reverse to avoid skipping entries)
    for i in range(size-1, 0, -2):
        (_, _, i_wins) = runGames('strategyagent', 'agent_i', 'agent_i', 100)
        (_, _, i_minus_1_wins) = runGames('strategyagent', 'agent_i-1', 'agent_i-1', 100)
        if i_wins >= i_minus_1_wins:
            losers.insert(0, (i_minus_1_wins, agents.pop(i-1)))
            winsOfWinner = i_wins
        else:
            losers.insert(0, (i_wins, agents.pop(i-1)))
            winsOfWinner = i_minus_1_wins
    # reset value of N for next round of bracket
    N = len(agents)

# we now have our winner, so get its feature weights
assert len(agents) == 1
print("Wins: {}".format(winsOfWinner))
print("Features:")
print(agents[0].features) # cant throw an error bc only using tourney agents