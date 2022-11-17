from Hand import Hand
from Player import Player
from PlayableHand import PlayableHand


class GameState:

    def __init__(self, discarded: Hand, players: list[Player], current: list[PlayableHand], currentPlayerIndex = 0,lastPlayerIndex = 0):
        self.discarded = discarded 
        self.players = players
        self.current = current # list of playablehands
        self.lastPlayerIndex = lastPlayerIndex # last player who puts down non empty Hand, 
        self.currentPlayerIndex = currentPlayerIndex # current player index to make an action

    # determine the next player to make action: using currentPlayerIndex
    def toMove(self):

        return self.currentPlayerIndex # for the next move +1 on the index of current player
   
    # helper function that is used to avoid duplicate
    # @return: the next player given current index
    def nextPlayer(self,index:int):
        if index == len(self.players)-1:
                return 0
        else:
            return index+1 

    # hand is sorted
    # hand would be able to check types and weight
    # hand: list of hand or list
    # get all possible actions for current player
    # @return: list of PlayableHand that represent all possible actions that current player could take
    def getActions(self):
        # current hand for current player
        currentHand = self.players[self.toMove()].hand
        # initialize actions
        actions = []

        # if this is a new round
        if len(self.current) == 0:
            actions.extend(currentHand.getPlayableHands())
        
        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = self.current[len(self.current)-1]# the last playablehand for current round
            actions.extend(currentHand.getPlayableHands(currentCombo))
            

        return actions
        
    # check if the game over
    # @return: winner index or -1 if the game has not ended yet
    def isTerminal(self):
        for i in range(len(self.players)):
            # print(len(self.players[i].hand.cards))
            if len(self.players[i].hand.cards) == 0:
                return i
        return -1
    
    # check role
    def getUtility(self):

        for i in self.players:
            if len(i.hand.cards) == 0:
                if i.role == 'LANDLORD':
                    return +100
                else: 
                    return -100
        landlordNumCards = self.players[0].hand.getLength()
        peasant1NumCards = self.players[1].hand.getLength()
        peasant2NumCards = self.players[2].hand.getLength()

        return min(peasant1NumCards,peasant2NumCards) - landlordNumCards

    

    # move the game to the next stage by placing a hand/pass in a round
    # @return: a new game state after placing a hand
    def generateSuccessor(self,hand: PlayableHand):

        # copy the current player
        newPlayers = []
        for i in self.players:
          newPlayers.append(i.copy())
        #current player
        currentPlayerIndex = self.toMove()
        # copy the current deck
        newRound = []
        for i in self.current:
            newRound.append(i.copy())
        # copy of the discarded deck
        newDiscarded = self.discarded.copy()
        # if everyone passes in this round: current play is empty and this round started wit next player 
        # clear the current deck 
        if len(hand.cards) == 0 and self.lastPlayerIndex == self.nextPlayer(currentPlayerIndex):
            # return the new state with current cleared
            return GameState(newDiscarded, newPlayers, [], self.nextPlayer(self.currentPlayerIndex), self.lastPlayerIndex)

        # player passed, but round not over
        elif len(hand.cards) == 0:
            return GameState(newDiscarded, newPlayers, newRound, self.nextPlayer(self.currentPlayerIndex),
                             self.lastPlayerIndex)

        # player did not pass: update current and discard piles and continue round
        else:
            # modify the current player's card: filter the hand that current player plays this round
            newPlayers[currentPlayerIndex].hand.cards = [card for card in self.players[currentPlayerIndex].hand.cards if card not in hand.cards]
            # append hand to cuurent deck: put played hand to current round
            newRound.append(hand)
            # *push the played hand to discarded list
            newDiscarded.cards.extend(hand.cards)
            # return a new start regarding to the changes to the fields
            return GameState(newDiscarded, newPlayers, newRound, self.nextPlayer(self.currentPlayerIndex), currentPlayerIndex)
        


    def toString(self):
        """
        Returns a simple string representation of the current game state, including the top card of the
        current round and the number of cards in each player's hand
        """
        # Display what card is on top of the pile for this round
        currentHandStr = ''

        # cards are in current - show top hand
        if len(self.current) > 0:
            lastHandPlayed = self.current[len(self.current)-1]
            currentHandStr = lastHandPlayed.toString()

        gameStateStr = self.players[self.lastPlayerIndex].name + " Last Played: " + currentHandStr

        # Display the number of cards each player has
        for player in self.players:
            playerStr = f'{player.name} has {player.hand.getLength()} cards'
            gameStateStr += "\n" + playerStr

        return gameStateStr