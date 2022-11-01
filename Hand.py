from Card import Card
from HandTypes import HandTypes
from PlayableHand import PlayableHand


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

    def print(self):
        print(self.cards)
    
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

    def getPlayableHands(self, currHand=None):
        """
        Get all playable hands of a certain type that can be created with this hand's cards.
        Returns a list of PlayableHand objects of the given type.
        PARAMS:

        currHand        PlayableHand
        """
        # removes duplicates
        cards = list(set(self.cards))
        cards.sort(key=lambda c: c.value)
        ret = []
        # add all types of hands to ret
        ret.extend([PlayableHand([card]) for card in cards])

        for i in range(len(cards) - 1):
            if cards[i].value == cards[i + 1].value:
                ret.append(PlayableHand(cards[i:i+2]))
        
        for i in range(len(cards) - 2):
            if cards[i].value == cards[i + 1].value and cards[i + 1].value == cards[i + 2].value:
                ret.append(PlayableHand(cards[i:i+3]))
        
        for i in range(len(cards) - 2):
            if cards[i].value == cards[i + 1].value and cards[i + 1].value == cards[i + 2].value:
                for j in range(len(cards)):
                    if cards[j].value != cards[i]:
                        ret.append(PlayableHand([cards[i], cards[i + 1], cards[i + 2], cards[j]]))
        
        for i in range(len(cards) - 4):
            if [c.value for c in cards[i:i+5]] == list(range(cards[i].value, cards[i + 4].value)):
                ret.append(cards[i:i+5])
        
        for i in range(len(cards) - 3):
            if cards[i].value == cards[i + 1].value and cards[i + 1].value == cards[i + 2].value and cards[i + 2].value == cards[i + 3].value:
                ret.append(PlayableHand(cards[i:i+4]))
        
        if sum(c.value for c in cards[-2:]) == 33:
            ret.append(PlayableHand(cards[-2:]))
        
        if currHand is None:
            ret = [[]] + ret # pass
            return ret
        
        # print('RET: {}'.format(ret))
        ret = list(filter(lambda hand: True if hand == [] else hand.type == HandTypes.BOMB or hand.type == HandTypes.ROCKET or hand.type == currHand.type, ret))
        ret = [[]] + ret # pass
        return ret

    def toString(self):
        return ' '.join(map(lambda x: x.toString(), self.cards))