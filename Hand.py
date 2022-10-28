from Card import Card

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