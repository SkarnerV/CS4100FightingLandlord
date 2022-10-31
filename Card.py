from Suits import Suits

class Card:
    """
    A class for representing a single card.
    A card can have any suit in a normal deck of cards (heart, diamond, club, spade).
    The minimum value of the card is 3 (representing a 3), and the maximum is 17 (red joker).
    PARAMS:
    suit        Suits
    value       int
    """

    # static variable to easily map card value to card
    valueMap = {3 : "3", 4 : "4", 5 : "5", 6 : "6", 7 : "7", 8 : "8", 9 : "9",10 : "10", 
                11 : "J", 12 : "Q", 13 : "K", 14 : "A", 15 : "2", 16 : "JK", 17 : "JK"}

    def __init__(self, suit: Suits, value: int):
        # may require edge cases for dealing with whatever suit we want the jokers to be
        assert suit in Suits
        assert value >= 3 and value <= 17
        self.suit = suit
        self.value = value

    def getValueAsString(self):
        """
        Gets the String representation of a card's value
        3 --> "3"
        10 --> "10"
        11 --> "J"
        14 --> "A"
        15 --> "2"
        16,17 --> "JK"
        """
        return Card.valueMap[self.value]
        

    def __eq__(self, other):
        # override of equality method
        if isinstance(other, self.__class__):
            return self.suit == other.suit and self.value == other.value
    
    def __hash__(self):
        # override of hashing method
        return hash(("suit", self.suit, "value", self.value))
