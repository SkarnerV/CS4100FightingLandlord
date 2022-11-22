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

    def __init__(self, name, hand, role, trialsPerMove = 300):
        super().__init__(name, hand, role)
        self.trialsPerMove = trialsPerMove

    def makeMove(self, currState):
        possibleActions = self.getBetterActions(currState)
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
        peasant1Simulation = StrategyAgent(None, Hand(remainingCards[:numPeasant1Cards]), "PEASANT")
        peasant2Simulation = StrategyAgent(None, Hand(remainingCards[numPeasant1Cards:]), "PEASANT")
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

    def getBetterActions(self, state):
        # current hand for current player
        currentHand = self.hand
        # initialize actions
        actions = []

        # if this is a new round
        if len(state.current) == 0:
            actions.extend(currentHand.getBetterPlayableHands())

        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = state.current[len(state.current) - 1]  # the last playablehand for current round
            actions.extend(currentHand.getBetterPlayableHands(currentCombo))

        return actions