"""
A file for running a tournament, pitting differently weighted evaluation functions aganst each other to determine which performs best against the strategy agent.
"""

from game import Game
from game import runGames
from random import random
from TournamentExpectimaxAgent import TournamentExpectimaxAgent

listOfFeatures = ['p1NumCards', 'p2NumCards', 'lNumCards', 'lBestSingle', 'lWorstSingle', 'lBestDouble', 'lBestTriple', 'lBestSequence', 'lTurnNewRound']

# list of 2^n agents to be used. we will remove losers until there is one winner left
agentWeights = []
for i in range(8):
    weights = {}
    for feature in listOfFeatures:
        weights[feature] = random() * 10
    agentWeights.append(weights)

# store losers and how many games they won
losers = [] # in order of [2nd, 3-4, 3-4, 5-8, 5-8, 5-8, 5-8, ...]

N = len(agentWeights)
winsOfWinner = 0
while N > 1:
    size = len(agentWeights)
    # play agents i and i+1 against the strategy agent. winner moves on
    # (iterate over list in reverse to avoid skipping entries)
    for i in range(size-1, 0, -2):
        (_, _, i_wins) = runGames('strategyagent', 'tournamentagent', 'tournamentagent', 100, agentWeights[i])
        (_, _, i_minus_1_wins) = runGames('strategyagent', 'tournamentagent', 'tournamentagent', 100, agentWeights[i - 1])
        if i_wins >= i_minus_1_wins:
            losers.insert(0, (i_minus_1_wins, agentWeights.pop(i-1)))
            winsOfWinner = i_wins
        else:
            losers.insert(0, (i_wins, agentWeights.pop(i-1)))
            winsOfWinner = i_minus_1_wins
    # reset value of N for next round of bracket
    N = len(agentWeights)

# we now have our winner, so get its feature weights
assert len(agentWeights) == 1
print("Wins: {}".format(winsOfWinner))
print("Features:")
print(agentWeights) # cant throw an error bc only using tourney agents