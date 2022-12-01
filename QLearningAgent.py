import random
import time

import util
from Agent import StrategyAgent, Agent
from Counter import Counter
from FeatureExtractor import FeatureExtractor
from GameState import GameState
from Hand import Hand
from PlayableHand import PlayableHand


class QLearningAgent(Agent):
    def __init__(self, weights, hand, name="Landlord", role="LANDLORD", epsilon=0.5, alpha=0.5, discount=0.9):
        super().__init__(name, hand, role)
        self.featExtractor = FeatureExtractor()
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(discount)
        self.name = name
        self.hand = hand
        self.role = role

        if weights is None:
            # randomly assign initial weights
            featureNames = self.featExtractor.getFeatureNames()
            weights = Counter()
            for feat in featureNames:
                weights[feat] = random.randrange(-10, 10)

        self.weights = weights

    def makeMove(self, currState):
        # Pick Action
        actionOptions = currState.getActions()
        action = PlayableHand([])
        if util.flipCoin(self.epsilon):
            # take a random action
            if len(actionOptions) > 0:
                action = random.choice(actionOptions)
        else:
            # follow the best policy
            action = self.computeActionFromQValues(currState)

        return action


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        possibleActions = state.getActions()
        qValuesForState = []
        for action in possibleActions:
            qValue = self.getQValue(state, action)
            qValuesForState.append(qValue)

        return max(qValuesForState, default=0.0)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        possibleActions = state.getActions()
        # store all actions with the max Q-value for this state so that
        # ties can be broken randomly
        bestActions = []
        maxQValue = self.computeValueFromQValues(state)

        for action in possibleActions:
            qValue = self.getQValue(state, action)
            if qValue == maxQValue:
                bestActions.append(action)

        if len(bestActions) == 0:
            return PlayableHand([])
        else:
            return random.choice(bestActions)


    def getWeights(self):
        return self.weights


    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        features = self.featExtractor.getFeatures(state, action)
        weights = self.getWeights()
        qValue = weights * features
        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        currentQValue = self.getQValue(state, action)
        nextQValue = self.computeValueFromQValues(nextState)

        features = self.featExtractor.getFeatures(state, action)
        for fKey, fVal in features.items():
            difference = reward + self.discount * nextQValue - currentQValue
            self.weights[fKey] += self.alpha * difference * fVal

        self.weights.normalize()





    def observeTransition(self, state, action, nextState):
        """
                Called by environment to inform agent that a transition has
                been observed. This will result in a call to self.update
                on the same arguments

                NOTE: Do *not* override or call this function
        """
        reward = self.getTransitionReward(state, action)
        self.update(state, action, nextState, reward)



    def getTransitionReward(self, state, action):
        """
        Let the reward for taking an action in a particular state be the winrate obtained after taking this
        action and then playing out 1000 games with StrategyAgents as the playout strategy
        (see MCTSAgent)
        """
        numWins = 0
        for i in range(100):
            nextState = state.generateSuccessor(action)
            if (self.simulateGame(nextState) > 0):
                numWins += 1
        return numWins / 100

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


    def copy(self):
        return QLearningAgent(self.weights.copy(), self.hand.copy(), self.name, self.role, self.epsilon, self.alpha, self.discount)

