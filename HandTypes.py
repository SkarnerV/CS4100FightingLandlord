from enum import Enum

class HandTypes(Enum):
    """
    An enum representing the possible types of hands in Fighting the Landlord.
    Numerical values may be used in comparison.
    """

    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    QUAD = 4
    STRAIGHT = 5
    BOMB = 6
    ROCKET = 7