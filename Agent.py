import random
from Player import Player
from util import useStrategy


class Agent(Player):
    """
    Represents a game playing agent for a game of Fighting the Landlord.
    Agent is a subclass of Player, as anything a player does an agent should be able to do.
    """

    def __init__(self, name, hand, role):
        super().__init__(name, hand, role)

    def makeMove(self, currState):
        """
        Uses some type of calculation to make valid move and update state
        """


class RandomAgent(Agent):
    """
    Represents a game playing agent that randomly chooses a legal action on its turn
    """

    def __init__(self, name, hand, role):
        super().__init__(name, hand, role)

    def makeMove(self, currState):
        """
        Selects a random legal move
        """
        actionOptions = currState.getActions()
        action = random.choice(actionOptions)
        return action
    
    def copy(self):
        return RandomAgent(self.name,self.hand.copy(),self.role)


class StrategyAgent(Agent):
    """
    Represents a game playing agent that always follows gets rid of as many low value cards as possible

    Description of logic:
        - only passes if no other playable hand options
        - first priority is getting rid of the lowest value card (will choose a single 3 over a double 4)
        - next tries to get rid of as many lowest value cards as possible (will choose a double 3 over a single 3)
        - next tries getting rid of more cards (will choose a sequence starting with 3 over a single 3)
        - lastly tries to get rid of other low value cards (will choose triple 4s + kicker 3 over triple 5s + kicker 3)
    """

    def __init__(self, name, hand, role):
        super().__init__(name, hand, role)

    def makeMove(self, currState):
        return useStrategy(currState)

    def copy(self):
        return StrategyAgent(self.name, self.hand.copy(), self.role)

