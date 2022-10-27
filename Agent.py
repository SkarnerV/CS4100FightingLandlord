from Player import Player

class Agent(Player):
    """
    Represents a game playing agent for a game of Fighting the Landlord.
    Agent is a subclass of Player, as anything a player does an agent should be able to do.
    """

    def __init__(self, hand, role):
        super()

    def makeMove(self, currState):
        """
        Uses some type of calculation to make valid move and update state
        """