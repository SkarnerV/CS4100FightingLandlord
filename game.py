import sys

from Deck import Deck
from GameState import GameState
from Hand import Hand


class Game:
    """
    The Game manages the control flow and solicits actions from agents.
    """

    def __init__(self, landlordType, peasant1Type, peasant2Type):
        # shuffle and deal deck
        deck = Deck()

        landlordCards = deck.deal(numCards=20)
        peasant1Cards = deck.deal(numCards=17)
        peasant2Cards = deck.deal(numCards=17)

        print("landlord cards", len(landlordCards))
        print("peasant1 cards", len(peasant1Cards))
        print("peasant2 cards", len(peasant2Cards))


        # create players with dealt hands of cards
        landLord = loadPlayer(landlordType, landlordCards, "LANDLORD")
        peasant1 = loadPlayer(peasant1Type, peasant1Cards, "PEASANT")
        peasant2 = loadPlayer(peasant2Type, peasant2Cards, "PEASANT")


        discarded = Hand([]) # discard pile initially empty
        players = [landLord, peasant1, peasant2]
        current = [] # initially no cards in play

        self.state = GameState(discarded, players, current)
        self.moveHistory = []


    def run(self):
        """
        Main control loop for game play
        """

        while not self.state.isTerminal():
            # Fetch next agent
            agentIndex = self.state.toMove()
            agent = self.state.player[agentIndex]

            # Prompt agent for action - will be a Hand of cards
            action = agent.getAction(self.state)

            # Execute action
            self.moveHistory.append((agentIndex, action))
            self.state = self.state.generateSuccessor(action)

            # Change display -- if the player did not pass, print the cards they played
            if len(action.cards) > 0:
                print(action.print())




def readCommand( argv ):
    """
    Process command line arguments used to set up game
    """
    from optparse import OptionParser
    usageStr = """
        USAGE:      python game.py <options>
        EXAMPLES:   (1) python game.py
                        - starts a card game with 3 random agents (1 landlord, 2 peasants)
                    (2) python game.py --landlord expectiminimax --peasant1 random --peasant2 human
                    OR  python game.py -l expectiminimax -p1 random -p2 human
                        - starts a card game with a landlord agent using an expectiminimax algorithm, 
                        one peasant agent that plays randomly, and one human controlled peasant player 
        """
    parser = OptionParser(usageStr)

    parser.add_option('-n', '--numGames', dest='numGames', type='int',
                      help='the number of games to play', metavar='GAMES', default=1)
    parser.add_option('-l', '--landlord', dest='landlordAgent',
                      help='The agent type for the landlord player', default='RandomAgent')
    parser.add_option('-p', '--peasant1', dest='peasantAgent1',
                      help='The agent type for the first peasant player', default='RandomAgent')
    parser.add_option('-q', '--peasant2', dest='peasantAgent2',
                      help='The agent type for the second peasant player', default='RandomAgent')

    options, other = parser.parse_args(argv)
    if len(other) != 0:
        raise Exception('Command line input not understood: ' + str(other))
    args = dict()

    args['landlordType'] = options.landlordAgent
    args['peasant1Type'] = options.peasantAgent1
    args['peasant2Type'] = options.peasantAgent2
    args['numGames'] = options.numGames

    return args

def runGames(landlordType, peasant1Type, peasant2Type, numGames, timeout):
    """
    Run multiple games in succession and report landlord rate of winning
    """
    games = []

    # run all games
    for i in range(numGames):
        game = Game(landlordType, peasant1Type, peasant2Type, timeout)
        game.run()
        games.append(game)

    # tally up wins - utility positive if landlord wins
    landlordWins = [game.state.getUtility() > 0 for game in games]

    totalGames = len(games)
    landlordWinCount = landlordWins.count(True)
    peasantsWinCount = totalGames - landlordWinCount # someone must get rid of all cards first, can simply subtract

    # win rate for landlord
    landlordWinRate = landlordWinCount / float(totalGames)
    print('Landlord Win Rate:      %d/%d (%.2f)' % (landlordWinCount, totalGames, landlordWinRate))

    print()

    # win rate for peasants
    peasantsWinRate = peasantsWinCount / float(totalGames)
    print('Peasants Win Rate:      %d/%d (%.2f)' % (peasantsWinCount, totalGames, peasantsWinRate))



if __name__ == '__main__':
    args = readCommand( sys.argv[1:] )
    runGames( **args )