from Hand import Hand
from PlayableHand import PlayableHand
from GameState import GameState

class Player:
    """
    This class represents a player of a game of Fighting the Landlord.
    A player is either a PEASANT or a LANDLORD, and has a Hand.
    The role of a Player is to play a move.
    
    PARAMS:
    hand        Hand
    role        "PEASANT" or "LANDLORD"
    """

    def __init__(self, hand, role):
        assert role == "PEASANT" or role == "LANDLORD"
        self.hand = hand
        self.role = role
    
    def makeMove(self, currState):
        """
        Uses user input to make a valid move and update state
        """