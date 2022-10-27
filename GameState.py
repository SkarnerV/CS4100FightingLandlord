from Hand import Hand
from Player import Player

class GameState:
    def __init__(self, discarded: Hand, players: List[Player], current: List[Hand]):
        self.discarded = discarded 
        self.players = players
        self.current = current # list of hands
        self.lastIndex = -1
        # separately track current player, last player to put down cards, 

    
    def toMove(self):
        if len(self.discarded) == 0:
            for i in range(0,len(self.players)):
                if self.players[i].role == 'LANDLORD':
                    return i
        else: 
            if self.lastIndex == len(self.players)-1:
                return 0
            else:
                return self.lastIndex+1


    # hand is sorted
    # hand would be able to check types and weight
    # hand: list of hand or list
    def getActions(self):
        
        currentHand = self.players[self.toMove()].hand

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


        if(len(self.current) == 0):
            actions.extend(getSingle())
            actions.extend(getDouble())
            actions.extend(getTriple())
            actions.extend(getBomb())
            actions.extend(getSequence())
        
        else:
            currentCombo = self.current[len(self.current-1)]
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
        

    def isTerminal(self):
        for i in self.players:
            if len(i.hand) == 0:
                return True
        return False
    
    def getUtility(self):
        if len(self.players[self.toMove()].hand) == 0:
            return +1
        
        for i in self.players: 
            if len(i.hand) == 0:
                return -1
            
        return 0

    def generateSuccessor(self,cards):

        newPlayers = self.players.copy()
        newPlayers[self.toMove()].hand.cards = [i for i in self.players[self.toMove()].hand.cards if i not in cards]
        newRound = self.round.copy()
        newRound.hand.cards.append(cards)
        newDiscarded = self.discarded.copy()
        newDiscarded.extend(cards)
        


        newState = GameState(newDiscarded,newPlayers,self.toMove)

        return newState