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



    def getSingle(self):
        collection = []
        for i in self.cards:
            collection.push([i])
        return collection

    def getDouble(self):
        collection = []
        for i in range(0,len(self.cards)-1):
            if self.cards[i].value == self.cards[i+1].value:
                collection.push([self.cards[i],self.cards[i+1]])
        return collection

    def getTriple(self):
        collection = []
        for i in range(0,len(self.cards)-2):
            if self.cards[i].value == self.cards[i+1].value and self.cards[i+1].value == self.cards[i+2].value:
                collection.push([self.cards[i],self.cards[i+1],self.cards[i+2]])
        return collection


    def getQuad(self):
        collection = []
        for i in range(0,len(self.cards)-2):
            if self.cards[i].value == self.cards[i+1].value and self.cards[i+1].value == self.cards[i+2].value:
                for c in self.cards:
                    if c != self.cards[i].value and i.suit != 'BJ' and i.suit != 'RJ':
                        collection.push([self.cards[i],self.cards[i+1],self.cards[i+2],c])
        return collection

    def getBomb(self):
        collection = []
        for i in range(0,len(self.cards)-3):
            if self.cards[i].value == self.cards[i+1].value and self.cards[i+1].value == self.cards[i+2].value and self.cards[i+2].value == self.cards[i+3].value:
                collection.push([self.cards[i],self.cards[i+1],self.cards[i+2],self.cards[i+3]])
        return collection
    
    def getRocket(self):
        collection = []
        if self.cards[len(self.cards-1)].suit == 'RJ' and self.cards[len(self.cards-2)].suit == 'BJ':
                collection.push([self.cards[len(self.cards-2)],self.cards[len(self.cards-1)]])
        return collection
        
    def getSequence(self):
        collection = []
        noDuplicate = list(set(self.cards))
        for i in range(0,len(noDuplicate)-4):
            if noDuplicate[i].value == noDuplicate[i+1].value+1 and noDuplicate[i+1].value == noDuplicate[i+2].value+1 and noDuplicate[i+2].value == noDuplicate[i+3].value+1 and noDuplicate[i+3].value == noDuplicate[i+4].value+1:
                if noDuplicate[i+4].suit != 'RJ' and noDuplicate[i+4].suit != 'BJ' and noDuplicate[i+4].value != 15:
                    collection.push([noDuplicate[i],noDuplicate[i+1],noDuplicate[i+2],noDuplicate[i+3],noDuplicate[i+4]])
        return collection
        

    

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
        ret.append([]) # PASS
        # add all types of hands to ret
        ret.append([PlayableHand([card]) for card in cards])

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
            if [c.value for c in cards[i:i+5]] == list(range(cards[i].value, cards)):
                ret.append(cards[i:i+5])
        
        for i in range(len(cards) - 3):
            if cards[i].value == cards[i + 1].value and cards[i + 1].value == cards[i + 2].value and cards[i + 2].value == cards[i + 3].value:
                ret.append(PlayableHand(cards[i:i+4]))
        
        if sum(c.value for c in cards[-2:]) == 33:
            ret.append(PlayableHand(cards[-2:]))
        
        if currHand is None:
            return ret
        
        return list(filter(lambda hand: hand.type == HandTypes.BOMB or hand.type == HandTypes.ROCKET or hand.type == currHand.type, ret))

