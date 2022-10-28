import random

from Card import Card
from Suits import Suits


class Deck:
    """
    Represents a full deck of 54 cards (2-Ace one of each suit, black joker, and red joker)
    Used to shuffle and deal cards out to players at the start of a new game
    """

    def __init__(self):
        fullDeck = []
        for suit in Suits:
            # corresponds to values on non-joker cards
            for value in range(3, 16):
                fullDeck.append(Card(suit, value))
        # add jokers TODO what suits should jokers be?
        fullDeck.append(Card(None, 16))
        fullDeck.append(Card(None, 17))
        random.shuffle(fullDeck)

        self.cards = fullDeck

    def deal(self, numCards: int):
        """
        Returns the first numCards cards and removes them from the deck
        Modifies deck to ensure that the same card aren't dealt to two different players
        """
        assert numCards <= len(self.cards), f'Not enough cards in the deck to return {numCards}'
        dealtCards = self.cards[:numCards]
        self.cards = self.cards[numCards:]

        return dealtCards
