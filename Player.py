

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
        # alert user that it is their turn (prevent another player from seeing their hand)
        input(f"{self.name}\'s turn. Press enter to continue.\n")

        # print the player's hand
        print("Your current hand: " + self.hand.toString())

        actionOptions = currState.getActions()

        print("Your possible actions for this turn: ")
        print(len(actionOptions))
        for i in range(0, len(actionOptions)):
            actionOption = actionOptions[i]
            print(str(i) + ": " + actionOption.toString())

        actionIndex = input("Specify the index of your intended move: ")

        # if user input is invalid, ask again
        while (not actionIndex.isnumeric() or int(actionIndex) < 0 or int(actionIndex) >= len(actionOptions)):
            actionIndex = input("Invalid move index. Please try again: ")

        # return chosen action
        action = actionOptions[int(actionIndex)]
        return action
    
    def toString(self):
        return self.name + " " + self.hand.toString() + " " + self.role