from Counter import Counter
from Hand import Hand
from HandTypes import HandTypes


class FeatureExtractor:

    def getFeatureNames(self):
        return ['landlord-has-most-cards',
                'landlord-has-least-cards',
                'winning-move',
                'passing-near-peasant-win',
                'highest-card-near-peasant-win',
                'lowest-card-in-hand',
                'most-low-cards',
                'action-size',
                'opponent-must-pass',
                'pass']

    def getFeatures(self, state, action):
        """
          Returns a dict from features to values
        """
        features = Counter()
        features['landlord-has-most-cards'] = self.landlordHasMostCards(state, action)
        features['landlord-has-least-cards'] = self.landlordHasLeastCards(state, action)
        features['winning-move'] = self.winningMove(state, action)
        features['passing-near-peasant-win'] = self.badPass(state, action)
        features['highest-card-near-peasant-win'] = self.highestCardNearPeasantWin(state, action)
        features['lowest-card-in-hand'] = self.getsRidOfLowestCard(state, action)
        features['most-low-cards'] = self.getsRidOfMostLowCards(state, action)
        features['action-size'] = self.actionSize(action)
        features['opponent-must-pass'] = self.opponentMustPass(state, action)
        features['pass'] = self.moveIsPass(action)

        features.normalize()
        return features

    def landlordHasMostCards(self, state, action):
        return 1 if (self.landlordNumCards(state, action) > self.peasant1NumCards(state)
        and self.landlordNumCards(state, action) > self.peasant2NumCards(state)) else 0

    def landlordHasLeastCards(self, state, action):
        return 1 if (self.landlordNumCards(state, action) < self.peasant1NumCards(state)
        and self.landlordNumCards(state, action) < self.peasant2NumCards(state)) else 0


    def landlordNumCards(self, state, action):
        """
        Returns the number of cards that the landlord has in the given state
        Feature for an evaluation function
        """
        landlord = state.players[0]
        return landlord.hand.getLength() - action.getLength()

    def peasant1NumCards(self, state):
        """
        Returns the number of cards that the peasant1 has in the given state
        Feature for an evaluation function
        """
        peasant1 = state.players[1]
        return peasant1.hand.getLength()

    def peasant2NumCards(self, state):
        """
        Returns the number of cards that the peasant2 has in the given state
        Feature for an evaluation function
        """
        peasant2 = state.players[2]
        return peasant2.hand.getLength()

    def winningMove(self, state, action):
        if self.landlordNumCards(state, action) == 0:
            return 1
        else:
            return 0

    def badPass(self, state, action):
        if action.type == HandTypes.PASS and (self.peasant1NumCards(state) < 5 or self.peasant2NumCards(state) < 5):
            return 1
        else:
            return 0

    def getsRidOfLowestCard(self, state, action):
        actionValues = action.getCardsValue()
        handValues = state.players[0].hand.getCardsValue()

        if min(handValues, default=0) in actionValues:
            return 1
        else:
            return 0

    def getsRidOfMostLowCards(self, state, action):
        actionValues = action.getCardsValue()
        handValues = state.players[0].hand.getCardsValue()
        minHandValue = min(handValues, default=0)

        if actionValues.count(minHandValue) == handValues.count(minHandValue):
            return 1
        else:
            return 0

    def actionSize(self, action):
        return action.getLength()

    def opponentMustPass(self, state, action):
        possibleOpponentCards = state.players[1].hand.copy().cards
        possibleOpponentCards.extend(state.players[2].hand.copy().cards)
        opponentPlayableHands = Hand(possibleOpponentCards).getPlayableHands()

        if action.type == HandTypes.PASS:
            return 0

        opponentPlayableValues = list(map(
                lambda h: h.cards[0].value if h.type == action.type or h.type == HandTypes.ROCKET else 0,
                opponentPlayableHands))
        return 1 if action.cards[0].value > max(opponentPlayableValues, default=0) else 0


    def highestCardNearPeasantWin(self, state, action):
        if self.peasant1NumCards(state) < 7 or self.peasant2NumCards(state) < 7:
            actionValues = action.getCardsValue()
            handValues = state.players[0].hand.getCardsValue()
            return 1 if max(handValues, default=0) in actionValues else 0
        else:
            return 0

    def moveIsPass(self, action):
        return 1 if action.type == HandTypes.PASS else 0