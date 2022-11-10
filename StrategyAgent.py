from collections import Counter

from Agent import Agent
from HandTypes import HandTypes


class StrategyAgent(Agent):
    """
    Represents a game playing agent that always follows gets rid of as many low value cards as possible

    Description of logic:
        - only passes if no other playable hand options
        - first priority is getting rid of the lowest value card (will choose a single 3 over a double 4)
        - next tries to get rid of as many lowest value cards as possible (will choose a double 3 over a single 3)
        - next tries getting rid of more cards (will choose a sequence starting with 3 over a single 3)
        - lastly tries to get rid of other low value cards (will choose triple 4s + kicker 3 over triple 5s + kicker 3)
    """

    def __init__(self, name, hand, role):
        super().__init__(name, hand, role)

    def makeMove(self, currState):
        """
        Selects a random legal move
        """
        actionOptions = currState.getActions()

        # pass only if no other option
        if len(actionOptions) == 1:
            return actionOptions[0]

        # find the lowest value card available in actionOptions
        lowestCardVal = 20 # initialize to higher than any card value
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




