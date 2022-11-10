from Agent import Agent

class ExpectimaxAgent(Agent):

    def __init__(self, name, hand, role, depth = 2):
        super().__init__(name, hand, role)
        self.depth = depth

    def makeMove(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        v = float('-inf')
        action = None
        # alpha = float('-inf')
        # beta = float('inf')
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
        v = 0
        for i in state.getActions():
            if state.toMove() == 2:
                expect = self.max_value(state.generateSuccessor(i),depth+1)
            else: 
                expect = self.min_value(state.generateSuccessor(i),depth)
            v = expect + v
            # if v < alpha:
            #     return v
            # beta = min(beta,v)
        # if len(state.getActions()) == 0:
        #     return 0
        return v/len(state.getActions())

    def evaluationFunction(self,state):
        return state.getUtility()
    
    def copy(self):
        return ExpectimaxAgent(self.name,self.hand.copy(),self.role,self.depth)