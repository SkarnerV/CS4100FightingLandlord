from Card import Card
from HandTypes import HandTypes

class Hand:
    """
    A class for representing a hand of cards.
    A hand of cards is a list of valid Card objects.
    PARAMS:
    cards       List[Card]
    """
    
    def __init__(self, cards: list[Card]):
        # cards is allowed to be empty during construction
        self.cards = cards
    
    def addCard(self, card: Card):
        """
        Adds the given card to this hand's list of cards.
        If the hand already contains this card, does nothing.
        """
        if card not in self.cards:
            self.cards.append(card)
    
    def removeCard(self, card):
        """
        Removes the given card from this hand's list of cards.
        If the hand does not contain the specified card, does nothing.
        """
        if card in self.cards:
            self.cards.remove(card)
    
    def getPlayableHands(self, type):
        """
        Get all playable hands of a certain type that can be created with this hand's cards.
        Returns a list of PlayableHand objects of the given type.
        PARAMS:
        type        HandTypes
        """
        # removes duplicates
        self.cards = list(set(self.cards))
        self.cards.sort(key=lambda c: c.value)
        if type == HandTypes.SINGLE:
            return [PlayableHand([card]) for card in self.cards]
        
        if type == Handtypes.DOUBLE:
            ret = []
            for i in range(len(self.cards) - 1):
                if self.cards[i].value == self.cards[i + 1].value:
                    ret.append(PlayableHand(self.cards[i:i+2]))
            return ret

        if type == HandTypes.TRIPLE:
            ret = []
            for i in range(len(self.cards) - 2):
                if self.cards[i].value == self.cards[i + 1].value and self.cards[i + 1].value == self.cards[i + 2].value:
                    ret.append(PlayableHand(self.cards[i:i+3]))
            return ret
        
        if type == HandTypes.QUAD:
            ret = 0
            for i in range(len(self.cards) - 2):
                if self.cards[i].value == self.cards[i + 1].value and self.cards[i + 1].value == self.cards[i + 2].value:
                    for j in range(len(self.cards)):
                        if self.cards[j].value != self.cards[i]:
                            ret.append(PlayableHand([self.cards[i], self.cards[i + 1], self.cards[i + 2], self.cards[j]]))
            return ret
        
        # This will NOT RETURN DUPLICATE STRAIGHTS. This is because suits are irrelevant, so
        # two straights that are the same except for suits are identical hands, so playing either
        # will make no difference. However, since cards are removed after playing them, if you do
        # have duplicate straights, you will still be able to play both of them at some point.
        if type == handTypes.STRAIGHT:

            ret = []
            for i in range(len(self.cards) - 4):
                if [c.value for c in self.cards[i:i+5]] == list(range(self.cards[i].value, self.cards)):
                    ret.append(self.cards[i:i+5])
            return ret

        if type == HandTypes.BOMB:
            ret = []
            for i in range(len(self.cards) - 3):
                if self.cards[i].value == self.cards[i + 1].value and self.cards[i + 1].value == self.cards[i + 2].value and self.cards[i + 2].value == self.cards[i + 3].value:
                    ret.append(PlayableHand(self.cards[i:i+4]))
            return ret
        
        if type == HandTypes.ROCKET:
            if self.cards[-1].value == 17 and self.cards[-2].value == 16:
                return [PlayableHand(self.cards[-2:])]