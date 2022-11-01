import random
from Player import Player

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
        print(action.cards)
        return action
