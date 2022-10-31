from Hand import Hand
from Card import Card
from HandTypes import HandTypes

class PlayableHand(Hand):
    """
    A class representing a playable hand of cards.
    In other words, a PlayableHand consists of 1 to 5 cards that can be played
    during a turn of Fighting the Landlord.
    It is implemented as a subclass of Hand, with additional methods ensuring
    that the hand is valid and comparing the hand to another possible hand.

    PlayableHand.isValidHand(cards) should be called BEFORE creating a PlayableHand
    with a given hand of cards.
    """

    def __init__(self, cards):
        super().__init__(cards)
        assert PlayableHand.isValidHand(self.cards)
        self.type = self._setType()

    
    @staticmethod
    def isValidHand(cards):
        """
        This is a static method for determining whether or not a given list of
        Card objects makes up a valid hand.
        A hand is valid if it is a set of 1, 2, 3, 4, or 5 cards.
        A valid 1 card hand is any card.
        A valid 2 card hand is 2 of a kind (2 jokers is a valid hand).
        A valid 3 card hand is 3 of a kind.
        A valid 4 card hand is at least 3 of the same valued card.
        A 5 card hand is valid if it is equivalent to a  in poker.
        For a 5 card hand, 2's and jokers are not allowed.
        """
        return (self._isSingle() or self._isDouble() or self._isTriple() or
                self._isQuad() or self._isSequence() or self._isBomb() or self._isRocket())

    def _setType(self):
        """
        Returns a HandTypes value based on self.cards().
        Used to set self.type to the correct value.
        """

        if self._isRocket():
            return HandTypes.ROCKET
        if self._isBomb():
            return HandTypes.BOMB
        if self._isSequence():
            return HandTypes.SEQUENCE
        if self._isQuad():
            return HandTypes.QUAD
        if self._isTriple():
            return HandTypes.TRIPLE
        if self._isDouble():
            return HandTypes.DOUBLE
        if self._isSingle():
            return HandTypes.SINGLE
        
        assert False # this should never be reached


    def _isRocket(self):
        """
        Returns True if this PlayableHand is a rocket (2 Jokers).
        This is a helper method for canPlay, and should never be called on its own.
        """
        # math :)
        return len(self.cards) == 2 and self.cards[0].value + self.cards[1].value == 33
    
    def _isBomb(self):
        """
        Returns True if this PlayableHand is a bomb (4 of a kind).
        This is a helper method for canPlay, and should never be called on its own.
        """

        return (len(self.cards) == 4 and
                [c.value for c in self.cards].count(self.cards[0].value) == 4)
    
    def _isSequence(self):
        """
        Returns True if this PlayableHand is a valid sequence.
        """
        vals = [card.value for card in self.cards]
        vals.sort()
        return (len(self.cards == 5) and self.cards[4].value < 15 and
        vals == range(min(vals), max(vals) + 1))

    def _isQuad(self):
        """
        Returns True if this PlayableHand is a valid 4-card (non-bomb) hand.
        """
        return (len(cards) == 4 and (cards.count(cards[0].value) >= 3 or 
                cards.count(cards[1].value) >= 3))

    def _isTriple(self):
        """
        Returns True if this PlayableHand is a valid triple.
        """
        return len(cards) == 3 and cards.count(cards[0].value) == 3

    def _isDouble(self):
        """
        Returns True if this PlayableHand is a valid pair (double).
        """
        return len(cards) == 2 and cards.count(cards[0].value) == 2

    def _isSingle(self):
        """
        Returns True if this PlayableHand is a valid single card.
        """
        return len(cards) == 1

    def _compareOnes(self, other):
        """
        Assumes that this hand and other contain only one card, and returns True
        if this card is greater in value than other's card.
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """
        return self.cards[0].value > other.cards[0].value

    def _comparePairs(self, other):
        """
        Assumes that this hand and other contain only two cards, and returns True
        if this hand's pair is greater in value than other's pair.
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """
        # Since we assumed self and other are valid hands, they must be 2 of a kind.
        # So, we can just check a single card from each again.
        return self._compareOnes(other)

    def _compareTriples(self, other):
        """
        Assumes that this hand and other contain only three cards, and returns True
        if this hand's cards are greater in value than other's cards.
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """
        # Since we assumed self and other are valid hands, they must be 3 of a kind.
        # So, we can just check a single card from each again.
        return self._compareOnes(other)
    
    def _compareFours(self, other):
        """
        Assumes that this hand and other contain only four cards, and returns True
        if this hand's cards are greater in value than other's cards.
        This method also assumes that neither hand is a bomb (4 of a kind).
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """
        # We compare the 3 of a kinds first, then the kickers.
        if (self.cards[0].value == self.cards[1].value or
            self.cards[0].value == self.cards[2].value):
            s_three = self.cards[0].value
        else:
            s_three = self.cards[1].value
        
        if (other.cards[0].value == other.cards[1].value or
            other.cards[0].value == other.cards[2].value):
            o_three = other.cards[0].value
        else:
            o_three = other.cards[1].value
        
        # can't have 3334 and 3335 because only 4 3s in a deck
        if s_three > o_three:
            return True
        
        return False

    def _compareSequences(self, other):
        """
        Assumes that this hand and other are sequences, and returns True
        if this hand's cards are greater in value than other's cards.
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """

        return (max(self.cards, key=lambda c: c.value).value >
        max(other.cards, key=lambda c: c.value).value)
    
    def _compareBombs(self, other):
        """
        Assumes that this hand and other contain only three cards, and returns True
        if this hand's cards are greater in value than other's cards.
        This is a helper method for canPlay, and should never be called on its own.
        PARAMS:
        other       PlayableHand
        """
        # Since we assumed self and other are valid hands, they must be 3 of a kind.
        # So, we can just check a single card from each again.
        return self._compareOnes(other)

    def canPlay(self, other):
        """
        Returns True if this hand can be played above the other hand in a game
        of Fighting the Landlord.
        Note that 2*JK > 4 of a kind > anything else
        PARAMS:
        other       PlayableHand
        """

        assert isinstance(other, self.__class__)

        if self.type == HandTypes.ROCKET:
            return True
        if self.type == HandTypes.BOMB and not (other.type == HandTypes.ROCKET or
        other.type == HandTypes.BOMB):
            return True
        if self.type == HandTypes.BOMB and other.type == HandTypes.BOMB:
            return self._compareBombs(other)
        if self.type != other.type:
            return False
        if self.type == HandTypes.SEQUENCE:
            return self._compareSequences(other)
        if self.type == HandTypes.QUAD:
            return self._compareFours(other)
        if self.type == HandTypes.TRIPLE:
            return self._compareTriples(other)
        if self.type == HandTypes.DOUBLE:
            return self._comparePairs(other)
        if self.type == HandTypes.SINGLE:
            return self._compareOnes(other)
        
        print("this isnt supposed to occur [in canPlay()]")
        return False # if for some reason something is bad just print and return false