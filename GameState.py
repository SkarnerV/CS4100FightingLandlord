from Hand import Hand
from Player import Player


class GameState:
    def __init__(self, discarded: Hand, players: List[Player], current: List[Hand], currentPlayerIndex = -1,lastPlayerIndex = -1):
        self.discarded = discarded 
        self.players = players
        self.current = current # list of hands
        self.lastPlayerIndex = lastPlayerIndex # last player who puts down non empty Hand, 
        self.currentPlayerIndex = currentPlayerIndex # current player index to make an action

    # determine the next player to make action: using currentPlayerIndex
    def toMove(self):
        # if the game just started, start with landlord player
        if len(self.discarded) == 0:
            for i in range(0,len(self.players)):
                if self.players[i].role == 'LANDLORD': # check the lanlord and return landlord player index
                    return i
        # move to the next player from the last player
        else: 
            return self.nextPlayer(self.currentPlayerIndex) # for the next move +1 on the index of current player
   
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


        def getSingle():
            collection = []
            for i in currentHand:
                collection.push([i])
            return collection

        def getDouble():
            collection = []
            for i in range(0,len(currentHand)-1):
                if currentHand[i].value == currentHand[i+1].value:
                    collection.push([currentHand[i],currentHand[i+1]])
            return collection

        def getTriple():
            collection = []
            for i in range(0,len(currentHand)-2):
                if currentHand[i].value == currentHand[i+1].value and currentHand[i+1].value == currentHand[i+2].value:
                    collection.push([currentHand[i],currentHand[i+1],currentHand[i+2]])
                    for i in currentHand:
                        if i != currentHand[i].value and i.suit != 'BJ' and i.suit != 'RJ':
                            collection.push([currentHand[i],currentHand[i+1],currentHand[i+2]],i)
            return collection

        def getBomb():
            collection = []
            for i in range(0,len(currentHand)-3):
                if currentHand[i].value == currentHand[i+1].value and currentHand[i+1].value == currentHand[i+2].value and currentHand[i+2].value == currentHand[i+3].value:
                    collection.push([currentHand[i],currentHand[i+1],currentHand[i+2],currentHand[i+3]])
            if currentHand[len(currentHand-1)].suit == 'RJ' and currentHand[len(currentHand-2)].suit == 'BJ':
                    collection.push([currentHand[len(currentHand-2)],currentHand[len(currentHand-1)]])
            return collection
        
        def getSequence():
            collection = []
            for i in range(0,len(currentHand)-4):
                if currentHand[i].value == currentHand[i+1].value+1 and currentHand[i+1].value == currentHand[i+2].value+1 and currentHand[i+2].value == currentHand[i+3].value+1 and currentHand[i+3].value == currentHand[i+4].value+1:
                    if currentHand[i+4].suit != 'RJ' and currentHand[i+4].suit != 'BJ':
                        collection.push([currentHand[i],currentHand[i+1],currentHand[i+2],currentHand[i+3],currentHand[i+4]])
            return collection

        # if this is a new round
        if(len(self.current) == 0):
            actions.extend(getSingle())
            actions.extend(getDouble())
            actions.extend(getTriple())
            actions.extend(getBomb())
            actions.extend(getSequence())

        # if the round gets continued from lastPlayerIndex
        else:
            currentCombo = self.current[len(self.current)-1]# the last hand for current round
            if currentCombo.checkType() == 'single':
                 actions.extend(getSingle())
            if currentCombo.checkType() == 'double':    
                actions.extend(getDouble())
            if currentCombo.checkType() == 'triple':
                actions.extend(getTriple())
            if currentCombo.checkType() == 'bomb':
                actions.extend(getBomb())
            if currentCombo.checkType() == 'sequence':
                actions.extend(getSequence())

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
        currentPlayer = self.players[self.toMove()]

        # if currentplayer has empty hand or the next player has empty hand with same role
        if len(currentPlayer.hand) == 0 or (len(self.players[nextPlayerIndex].hand) == 0 and self.players[nextPlayerIndex].role == currentPlayer.role):
            return +100
        
        nextPlayerIndex = self.nextPlayer(self.toMove())

        # if next player has empty hand and different role
        if (len(self.players[nextPlayerIndex].hand) == 0 and self.players[nextPlayerIndex].role != currentPlayer.role):
            return -100
        
        # if no one has empty hand
        return 0

    # move the game to the next stage by placing a hand/pass in a round
    # @return: a new game state after placing a hand
    def generateSuccessor(self,hand):

        # copy the current player
        newPlayers = self.players.copy()
        #current player
        currentPlayerIndex = self.toMove()
        # copy the current deck
        newRound = self.current.copy()
        # copy of the discarded deck
        newDiscarded = self.discarded.copy()
        # if everyone passes in this round: current play is empty and this round started wit next player 
        # clear the current deck 
        if len(hand.cards) == 0 and self.lastPlayerIndex == self.nextPlayer(currentPlayerIndex):
            # return the new state with current cleared
            return GameState(newDiscarded,newPlayers,[],self.currentPlayerIndex+1,self.lastPlayerIndex)

        # if current play continues the round
        else:
            # modify the current player's card: filter the hand that current player plays this round
            newPlayers[currentPlayerIndex].hand.cards = [i for i in self.players[currentPlayerIndex].hand.cards if i not in hand]
            # append hand to cuurent deck: put played hand to current round
            newRound.hand.cards.append(hand)
            # *push the played hand to discarded list
            newDiscarded.extend(hand)
            # return a new start regarding to the changes to the fields
            return GameState(newDiscarded,newPlayers,newRound,self.currentPlayerIndex+1,currentPlayerIndex)
        
