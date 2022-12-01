import util
from Agent import Agent
from Deck import Deck
from util import useStrategy
from PlayableHand import *

class TournamentExpectimaxAgent(Agent):

    def __init__(self, name, hand, role, features, depth = 3):
        super().__init__(name, hand, role)
        self.depth = depth
        # dict of feature weights
        self.features = features
 
    def makeMove(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        v = float('-inf')
        action = None
        # alpha = float('-inf')
        # beta = float('inf')
        actions = self.getBetterActions(gameState)
        # for i in actions:
        #     print(i.toString())
        for i in actions:
            current = self.min_value(gameState.generateSuccessor(i),0)
            if current > v:
                action = i
                v = current
            # if current > beta:
            #     return action
            # alpha = max(alpha,current)
        return action

    
    def max_value(self,state,depth):
        # print('depth ',depth)
        if state.isTerminal() > -1 or depth+1 == self.depth:
           return self.evaluationFunction(state)
      
        v = float('-inf')
        for i in self.getBetterActions(state):
            v = max(v,self.min_value(state.generateSuccessor(i),depth))
            # if v > beta:
            #     return v
            # alpha = max(alpha,v)
        return v

    def min_value(self,state,depth):
        if state.isTerminal() > -1:
            return self.evaluationFunction(state)
        v = 999999999
        predictedActions = self.getBetterActions(state)
        for i in predictedActions:
            if state.toMove() == 2:
                expect = self.max_value(state.generateSuccessor(i),depth+1)
            else: 
                expect = self.min_value(state.generateSuccessor(i),depth)
            if expect < v:
                v = expect
            # if v < alpha:
            #     return v
            # beta = min(beta,v)
        # if len(state.getActions()) == 0:
        #     return 0
        return v

    def evaluationFunction(self, state):
        # we now have a map of features to weights that we can use
        # NOTE: this is now a weighted sum, so for items to be negative, their weights must be negative
        if state.isTerminal() > -1:
            return state.getUtility()
        else:
            return util.peasant1NumCards(state) * self.features['p1NumCards'] + util.peasant2NumCards(state) * self.features['p2NumCards'] + util.landlordNumCards(state) * self.features['lNumCards']\
                   + util.landlordBestSingleCard(state) * self.features['lBestSingle'] + util.landlordWorstSingleCard(state) * self.features['lWorstSingle'] + util.landlordBestDouble(state) * self.features['lBestDouble']\
                   + util.landlordBestTriple(state) * self.features['lBestTriple'] + util.landlordBestSequence(state) * self.features['lBestSequence'] + util.newRoundLandlordTurn(state) * self.features['lTurnNewRound']

    def predictActions(self, state):
        newDeck = Deck()
        for i in self.hand.cards:
            newDeck.removeCard(i)
        for i in state.discarded.cards:
            newDeck.removeCard(i)
        
        actions = [] # list of playablehand
        if len(state.current) == 0:
            actions.extend(newDeck.getPlayableHands())
        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = state.current[-1]# the last playablehand for current round
            actions.extend(newDeck.getPlayableHands(currentCombo))
        
        return actions

      # hand is sorted
    # hand would be able to check types and weight
    # hand: list of hand or list
    # get all possible actions for current player
    # @return: list of PlayableHand that represent all possible actions that current player could take
    def getBetterActions(self,state):
        # current hand for current player
        currentHand = self.hand
        # initialize actions
        actions = []

        # if this is a new round
        if len(state.current) == 0:
            actions.extend(currentHand.getBetterPlayableHands())
        
        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = state.current[len(state.current)-1]# the last playablehand for current round
            actions.extend(currentHand.getBetterPlayableHands(currentCombo))
            

        return actions