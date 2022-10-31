

class Player:
    """
    This class represents a player of a game of Fighting the Landlord.
    A player is either a PEASANT or a LANDLORD, and has a Hand.
    The role of a Player is to play a move.
    
    PARAMS:
    name        name to identify player
    hand        Hand
    role        "PEASANT" or "LANDLORD"
    """

    def __init__(self, name, hand, role):
        assert role == "PEASANT" or role == "LANDLORD"
        self.name = name
        self.hand = hand
        self.role = role
    
    def makeMove(self, currState):
        """
        Uses user input to make a valid move and update state
        """
        input(f'{self.name}\'s turn. Press any key to continue.\n')
        #TODO need a method on hand (and card) that returns a string for display
        print(self.hand.print(), "\n")

        actionOptions = currState.getActions()
        # TODO determine how we want users to specify moves (ex: '33'?, display possible moves and specify index?)
        action = input("Specify Move: ")

        # TODO need method that looks at user input and player's cards, produces a Hand object if possible
        # if action hand is not in actionOptions, loop and prompt user again
