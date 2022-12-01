from Agent import Agent
from Deck import Deck
from util import useStrategy
from PlayableHand import *
class ExpectimaxAgentOne(Agent):

    def __init__(self, name, hand, role, depth = 4):
        super().__init__(name, hand, role)
        self.depth = depth
 
    def makeMove(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction
        """
        v = float('-inf')
        action = None
        # alpha = float('-inf')
        # beta = float('inf')
        if len(gameState.current) == 0:
            return useStrategy(gameState)
        for i in gameState.getActions():
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
        for i in state.getActions():
            v = max(v,self.min_value(state.generateSuccessor(i),depth))
            # if v > beta:
            #     return v
            # alpha = max(alpha,v)
        return v

    def min_value(self,state,depth):
        if state.isTerminal() > -1:
            return self.evaluationFunction(state)
        v = 999999999
        predictedActions = state.getActions()
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

    def evaluationFunction(self,state):
        return state.getUtility()
    
    def copy(self):
        return ExpectimaxAgentOne(self.name,self.hand.copy(),self.role,self.depth)

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

    