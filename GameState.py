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
    # @return: list of Hands that represent all possible actions that current player could take
    def getActions(self):
        # current hand for current player
        currentHand = self.players[self.toMove()].hand
        # initialize actions
        actions = []

        # if this is a new round
        if(len(self.current) == 0):
            actions.extend(currentHand.getPlayerable())
        
        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = self.current[len(self.current)-1]# the last playablehand for current round
            actions.extend(currentHand.getPlayerable(currentCombo))
            

        return actions
        
    # check if the game over
    # @return: winner index or -1 if the game has not ended yet
    def isTerminal(self):
        for i in self.players:

            if len(i.hand) == 0:
                return i
        return -1
    
    # check role
    def getUtility(self):
        
        for i in self.players:
            if len(i.hand) == 0:
                if i.role == 'LANDLORD':
                    return +100
                else: 
                    return -100
        return 0


    # move the game to the next stage by placing a hand/pass in a round
    # @return: a new game state after placing a hand
    def generateSuccessor(self,hand):

        # copy the current player
        newPlayers = self.players.copy()
        #current player
        currentPlayerIndex = self.toMove()
        # copy the current deck
        newRound = PlayableHand(self.current.cards)
        # copy of the discarded deck
        newDiscarded = Hand(self.discarded.cards)
        # if everyone passes in this round: current play is empty and this round started wit next player 
        # clear the current deck 
        if len(hand.cards) == 0 and self.lastPlayerIndex == self.nextPlayer(currentPlayerIndex):
            # return the new state with current cleared
            return GameState(newDiscarded,newPlayers,PlayableHand([]),self.nextPlayer(self.currentPlayerIndex),self.lastPlayerIndex)

        # if current play continues the round
        else:
            # modify the current player's card: filter the hand that current player plays this round
            newPlayers[currentPlayerIndex].hand.cards = [i for i in self.players[currentPlayerIndex].hand.cards if i not in hand]
            # append hand to cuurent deck: put played hand to current round
            newRound.hand.cards.append(hand)
            # *push the played hand to discarded list
            newDiscarded.cards.extend(hand)
            # return a new start regarding to the changes to the fields
            return GameState(newDiscarded,newPlayers,newRound,self.nextPlayer(self.currentPlayerIndex),currentPlayerIndex)
        
