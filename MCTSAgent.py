import random
from math import ceil
from operator import itemgetter

from GameState import GameState
from Agent import Agent, StrategyAgent
from Hand import Hand


class MCTSAgent(Agent):
    """
    Represents an agent that selects the move with the greatest success rate if
    we select a move and then finish the game using random agents.
    """

    def __init__(self, name, hand, role, trialsPerMove = 500):
        super().__init__(name, hand, role)
        self.trialsPerMove = trialsPerMove

    def makeMove(self, currState):
        possibleActions = currState.getActions()
        successRates = []
        trialsPerAction = ceil(self.trialsPerMove / len(possibleActions))

        for action in possibleActions:
            numWins = 0
            for i in range(trialsPerAction):
                nextState = currState.generateSuccessor(action)
                if (self.simulateGame(nextState) > 0):
                    numWins += 1
            successRates.append((action, numWins))

        return max(successRates, key=itemgetter(1))[0]




    def copy(self):
        return MCTSAgent(self.name, self.hand.copy(), self.role, self.trialsPerMove)



    def simulateGame(self, nextState):
        remainingCards = []
        remainingCards.extend(nextState.players[1].hand.cards)
        remainingCards.extend(nextState.players[2].hand.cards)
        random.shuffle(remainingCards)
        numPeasant1Cards = nextState.players[1].hand.getLength()


        landlordSimulation = StrategyAgent(None, nextState.players[0].hand.copy(), "LANDLORD")

        peasant1Cards = remainingCards[:numPeasant1Cards]
        peasant1Cards.sort(key=lambda c: c.value)
        peasant1Simulation = StrategyAgent(None, Hand(peasant1Cards), "PEASANT")

        peasant2Cards = remainingCards[numPeasant1Cards:]
        peasant2Cards.sort(key=lambda c: c.value)
        peasant2Simulation = StrategyAgent(None, Hand(peasant2Cards), "PEASANT")

        nextPlayers = [landlordSimulation, peasant1Simulation, peasant2Simulation]
        newRound = list(map(lambda hand: hand.copy(), nextState.current))
        simulatedState = GameState(nextState.discarded.copy(), nextPlayers, newRound, nextState.currentPlayerIndex,
                  nextState.lastPlayerIndex)

        while simulatedState.isTerminal() == -1:
            # Fetch next agent
            agentIndex = simulatedState.toMove()
            agent = simulatedState.players[agentIndex]

            # Prompt agent for action - will be a Hand of cards
            action = agent.makeMove(simulatedState)

            # Execute action
            simulatedState = simulatedState.generateSuccessor(action)

        return simulatedState.getUtility()

