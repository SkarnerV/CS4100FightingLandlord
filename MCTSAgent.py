from operator import itemgetter

from GameState import GameState
from Agent import Agent


class MCTSAgent(Agent):
    """
    Represents an agent that selects the move with the greatest success rate if
    we select a move and then finish the game using random agents.
    """

    def __init__(self, name, hand, role, trialsPerMove = 50):
        super().__init__(name, hand, role)
        self.trialsPerMove = trialsPerMove

    def makeMove(self, currState):
        possibleActions = self.getBetterActions(currState)
        successRates = []

        for action in possibleActions:
            numWins = 0
            for i in range(self.trialsPerMove):
                nextState = currState.generateSuccessor(action)
                if (self.simulateGame(nextState) > 0):
                    numWins += 1
            successRates.append((action, numWins))

        return max(successRates, key=itemgetter(1))[0]




    def copy(self):
        return MCTSAgent(self.name, self.hand.copy(), self.role, self.trialsPerMove)



    def simulateGame(self, nextState):
        randomPlayers = list(map(lambda p: p.convertToRandomAgent(), nextState.players))
        newRound = list(map(lambda hand: hand.copy(), nextState.current))
        simulatedState = GameState(nextState.discarded.copy(), randomPlayers, newRound, nextState.currentPlayerIndex,
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