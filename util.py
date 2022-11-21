from collections import Counter

from HandTypes import HandTypes


def useStrategy(currState):
    actionOptions = currState.getActions()

    # pass only if no other option
    if len(actionOptions) == 1:
        return actionOptions[0]

    # find the lowest value card available in actionOptions
    lowestCardVal = 20  # initialize to higher than any card value
    bestAction = None
    for action in actionOptions:
        # ignore PASS - better to play some cards
        if not action.type == HandTypes.PASS:
            # get cards in action and find the lowest value card
            cardValuesForAction = action.getCardsValue()
            lowestCardValForAction = min(cardValuesForAction)

            if lowestCardValForAction < lowestCardVal:
                # can get rid of a lower value card -- update!
                lowestCardVal = lowestCardValForAction
                bestAction = action

            elif lowestCardValForAction == lowestCardVal:
                # lowest value card it gets rid of is the same
                # still may be a better action if it gets rid of more this low value card
                currentBestCounter = Counter(bestAction.getCardsValue())
                actionCounter = Counter(cardValuesForAction)

                if actionCounter[lowestCardVal] > currentBestCounter[lowestCardVal]:
                    # gets rid of more of the lowest value card
                    # (ex: will choose a double 3 over a single 3)
                    bestAction = action

                elif actionCounter[lowestCardVal] == currentBestCounter[lowestCardVal]:
                    if action.getLength() > bestAction.getLength():
                        # gets rid of the same number of low value cards but overall more cards
                        # (ex: will choose a sequence starting with 3 over a single 3)
                        bestAction = action

                    elif action.getLength() == bestAction.getLength():
                        if sum(cardValuesForAction) > sum(bestAction.getCardsValue()):
                            # gets rid of the same number of cards but with overall lower value
                            # (ex: will choose triple 4s + kicker 3 over triple 5s + kicker 3)
                            bestAction = action

    return bestAction


def landlordNumCards(state):
    """
    Returns the number of cards that the landlord has in the given state
    Feature for an evaluation function
    """
    landlord = state.players[0]
    return landlord.hand.getLength()


def peasant1NumCards(state):
    """
    Returns the number of cards that the peasant1 has in the given state
    Feature for an evaluation function
    """
    peasant1 = state.players[1]
    return peasant1.hand.getLength()


def peasant2NumCards(state):
    """
    Returns the number of cards that the peasant2 has in the given state
    Feature for an evaluation function
    """
    peasant2 = state.players[2]
    return peasant2.hand.getLength()

def landlordBestSingleCombos(state):
    """
    Returns the value of the best card that the landlord has for each hand type
    Feature for an evaluation function
    Combined to save computation from getPlayableHands
    """
    landlord = state.players[0]
    landlordCards = landlord.hand
    playableHands = landlordCards.getPlayableHands()
    doubleCardValues = list(filter(lambda h: h.cards[0].value if h.handtype == HandTypes.DOUBLE or h.handtype == HandTypes.ROCKET else 0, playableHands))
    tripleCardValues = list(filter(lambda h: h.cards[0].value if h.handtype == HandTypes.TRIPLE else 0, playableHands))
    sequenceCardValues = list(filter(lambda h: h.cards[0].value if h.handtype == HandTypes.SEQUENCE else 0, playableHands))
    return (max(doubleCardValues, default=0), max(tripleCardValues, default=0), max(sequenceCardValues, default=0))

def landlordBestSingleCard(state):
    """
    Returns the value of the best card that the landlord has
    Feature for an evaluation function
    """
    landlord = state.players[0]
    landlordCards = landlord.hand
    landlordCardValues = landlordCards.getCardsValue()
    return max(landlordCardValues, default=0)

def landlordWorstSingleCard(state):
    """
    Returns the value of the worst card that the landlord has
    Feature for an evaluation function
    """
    landlord = state.players[0]
    landlordCards = landlord.hand
    landlordCardValues = landlordCards.getCardsValue()
    return min(landlordCardValues, default=20)

def landlordBestDouble(state):
    """
    Returns the value of the best card that the landlord has that can be played as a double
    Feature for an evaluation function
    """
    return playerBestDouble(state, 0)

def playerBestDouble(state, playerIndex):
    """
     Returns the value of the best card that the player at the given index has that can be played as a double
     Feature for an evaluation function
     """
    player = state.players[playerIndex]
    playerCards = player.hand
    playableHands = playerCards.getPlayableHands()
    doubleCardValues = list(
        map(lambda h: True if h.type == HandTypes.DOUBLE or h.type == HandTypes.ROCKET else 0, playableHands))
    return max(doubleCardValues, default=0)
def landlordBestTriple(state):
    """
    Returns the value of the best card that the landlord has that can be played as a triple
    Feature for an evaluation function
    """
    return playerBestTriple(state, 0)

def playerBestTriple(state, playerIndex):
    """
    Returns the value of the best card that the player at the given index has that can be played as a triple
    Feature for an evaluation function
    """
    player = state.players[playerIndex]
    playerCards = player.hand
    playableHands = playerCards.getPlayableHands()
    tripleCardValues = list(map(lambda h: h.cards[0].value if h.type == HandTypes.TRIPLE else 0, playableHands))
    return max(tripleCardValues, default=0)

def landlordBestSequence(state):
    """
    Returns the value of the best card that the landlord has that can be played as a sequence
    Feature for an evaluation function
    """
    return playerBestSequence(state, 0)

def playerBestSequence(state, playerIndex):
    """
    Returns the value of the best card that the player at the given index has that can be played as a sequence
    Feature for an evaluation function
    """
    player = state.players[playerIndex]
    playerCards = player.hand
    playableHands = playerCards.getPlayableHands()
    sequenceCardValues = list(map(lambda h: h.cards[0].value if h.type == HandTypes.SEQUENCE else 0, playableHands))
    return max(sequenceCardValues, default=0)

def newRoundLandlordTurn(state):
    """
    Returns 1 if it is the landlord's turn next with no current round, 0 otherwise
    """
    return 1 if (state.toMove() == 0 and len(state.current) == 0) else 0
