from Hand import Hand
from Card import Card

class PlayableHand(Hand):
    """
    A class representing a playable hand of cards.
    In other words, a PlayableHand consists of 1 to 5 cards that can be played
    during a turn of Fighting the Landlord.
    It is implemented as a subclass of Hand, with additional methods ensuring
    that the hand is valid and comparing the hand to another possible hand.

    isValidHand() should be called BEFORE creating a PlayableHand
    with a given hand of cards.
    """

    def __init__(self, cards):
        super().__init__(cards)
        assert self.isValidHand()
        self.type = self._setType()

    def isValidHand():
        """
        This is a method for determining whether or not a given list of
        Card objects makes up a valid hand.
        A hand is valid if it is a set of 1, 2, 3, 4, or 5 cards.
        A valid 1 card hand is any card.
        A valid 2 card hand is 2 of a kind (2 jokers is a valid hand).
        A valid 3 card hand is 3 of a kind.
        A valid 4 card hand is at least 3 of the same valued card.
        A 5 card hand is valid if it is equivalent to a straight in poker.
        For a 5 card hand, 2's and jokers are not allowed.
        """

        # it looks ugly, but raw Boolean logic should be faster than if/else blocks
        vals = [card.value for card in cards]
        vals.sort()
        return (len(cards) == 1 or 
                (len(cards) == 2 and (cards.count(cards[0].value) == 2
                    or (16 in cards and 17 in cards))) or
                (len(cards) == 3 and cards.count(cards[0].value) == 3) or
                (len(cards) == 4 and (cards.count(cards[0].value) >= 3 or 
                cards.count(cards[1].value) >= 3)) or
                (len(cards == 5) and cards[4].value < 15 and vals == range(min(vals), max(vals) + 1)))

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
        
        if s_three > o_three:
            return True
        if s_three < o_three:
            return False
        
        s = sum(c.value for c in self.cards)
        o = sum(c.value for c in other.cards)
        return (s - 3 * s_three > o - 3 * o_three)

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
        if self._isRocket():
            return True
        if self._isBomb() and not (other._isRocket() or other._isBomb()):
            return True
        if self._isBomb() and other._isBomb():
            return self._compareBombs(other)
        if len(self.cards) != len(other.cards):
            return False
        if len(self.cards == 4):
            return self._compareFours(other)
        if len(self.cards == 3):
            return self._compareTriples(other)
        if len(self.cards == 2):
            return self._comparePairs(other)
        if len(self.cards == 1):
            return self._compareOnes(other)
