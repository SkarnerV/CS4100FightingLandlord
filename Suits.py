from enum import Enum

class Suits(Enum):
    """
    An enum representing the possible suits of a card in a normal deck of cards.
    Each value represents its corresponding suit.
    Numerical values are NOT TO BE USED.
    """

    HEART = 1
    DIAMOND = 2
    CLUB = 3
    SPADE = 4