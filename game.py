import sys

from GameState import GameState


class Game:
    """
    The Game manages the control flow and solicits actions from agents.
    """

    def __init__(self, landlordType, peasant1Type, peasant2Type, timeout):
        # shuffle and deal deck
        deck = None  # TODO UPDATE with deck object and .shuffle() with a random seed

        landlordCards = deck.deal(numCards=20)
        peasant1Cards = deck.deal(numCards=17)
        peasant2Cards = deck.deal(numCards=17)

        # create players with dealt hands of cards
        landLordAgent = loadAgent(landlordType, landlordCards)
        peasant1Agent = loadAgent(peasant1Type, peasant1Cards)
        peasant2Agent = loadAgent(peasant2Type, peasant2Cards)

        self.state = GameState([], [landLordAgent, peasant1Agent, peasant2Agent], [])
        self.moveHistory = []
        self.timeout = timeout # TODO currently not in use


    def run(self):
        """
        Main control loop for game play
        """

        while not self.state.isTerminal():
            # Fetch next agent
            agentIndex = self.state.toMove()
            agent = self.state.player[agentIndex]

            # Prompt agent for action
            action = agent.getAction(self.state)

            # Execute action
            self.moveHistory.append((agentIndex, action))
            self.state = self.state(generateSuccessor(agentIndex, action))

            # Change display -- if the player did not pass, print the cards they played
            # TODO - currently hardcoded to print to console, should be more flexible
            if len(action > 0):
                print(action.print())

            # need to update next player to move -- will likely need to modify current toMove function
            # because if the player passes, lastPlayerIndex will not update




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
    parser.add_option('--timeout', dest='timeout', type='int',
                      help='Maximum length of time an agent can spend computing in a single game', default=30)

    options, other = parser.parse_args(argv)
    if len(other) != 0:
        raise Exception('Command line input not understood: ' + str(other))
    args = dict()

    args['landlordType'] = options.landlordAgent
    args['peasant1Type'] = options.peasantAgent1
    args['peasant2Type'] = options.peasantAgent2
    args['numGames'] = options.numGames
    args['timeout'] = options.timeout

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

    # tally up win rate for landlord
    wins = [game.state.isWin() for game in games]
    winRate = wins.count(True) / float(len(wins))
    print('Landlord Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate))

    return games


if __name__ == '__main__':
    args = readCommand( sys.argv[1:] )
    runGames( **args )