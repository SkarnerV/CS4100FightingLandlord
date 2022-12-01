import sys

from Agent import StrategyAgent
from Deck import Deck
from GameState import GameState
from Hand import Hand
from QLearningAgent import QLearningAgent


class QLearningTraining:
    """
    Similar to game.py, manages control flow of training sessions for Q-Learning Agent
    """

    def __init__(self, weights=None):
        # shuffle and deal deck
        deck = Deck()

        landlordCards = deck.deal(numCards=20)
        peasant1Cards = deck.deal(numCards=17)
        peasant2Cards = deck.deal(numCards=17)

        # create players with dealt hands of cards
        landlord = QLearningAgent(weights, landlordCards)
        peasant1 = StrategyAgent("Peasant 1", peasant1Cards, "PEASANT")
        peasant2 = StrategyAgent("Peasant 2", peasant2Cards, "PEASANT")

        discarded = Hand([])  # discard pile initially empty
        players = [landlord, peasant1, peasant2]
        current = []  # initially no cards in play

        self.state = GameState(discarded, players, current)


    def run(self):
        """
        Main control loop for game play
        """
        while self.state.isTerminal() == -1:
            print()
            print(self.state.toString())
            print()

            # Fetch next agent
            agentIndex = self.state.toMove()
            agent = self.state.players[agentIndex]

            # Prompt agent for action - will be a Hand of cards
            action = agent.makeMove(self.state)
            print(f'{agent.name}\'s move: {action.toString()}')

            originalState = self.state
            # Execute action
            nextState = self.state.generateSuccessor(action)
            self.state = nextState

            if agentIndex == 0:
                newAgent = self.state.players[agentIndex]
                newAgent.observeTransition(originalState, action, nextState)

        # game ended - print winner
        winner = self.state.players[self.state.isTerminal()]
        print()
        print(winner.name + " won!")
        print()

        qLearningAgent = self.state.players[0]
        return qLearningAgent.getWeights()


def readCommand(argv):
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
                      help='the number of games to play to train the agent', metavar='GAMES', default=10000)

    options, other = parser.parse_args(argv)
    if len(other) != 0:
        raise Exception('Command line input not understood: ' + str(other))
    args = dict()

    args['numGames'] = options.numGames
    return args

def runGames(numGames):
    """
    Run multiple games in succession with the same agent and reports resulting feature weights
    """
    games = []
    weights = []
    # run all games

    for i in range(numGames):
        print("Game number " + str(i))
        if len(weights) > 0:
            game = QLearningTraining(weights=weights[-1])
        else:
            game = QLearningTraining(weights=None)
        recentWeights = game.run()
        print(recentWeights)
        weights.append(recentWeights)
        games.append(game)


    # tally up wins - utility positive if landlord wins
    landlordWins = [game.state.getUtility() > 0 for game in games]

    totalGames = len(games)
    landlordWinCount = landlordWins.count(True)
    peasantsWinCount = totalGames - landlordWinCount  # someone must get rid of all cards first, can simply subtract

    # win rate for landlord
    print()
    landlordWinRate = landlordWinCount / float(totalGames)
    print('Landlord Win Rate:      %d/%d (%.2f)' % (landlordWinCount, totalGames, landlordWinRate))

    # win rate for peasants
    peasantsWinRate = peasantsWinCount / float(totalGames)
    print('Peasants Win Rate:      %d/%d (%.2f)' % (peasantsWinCount, totalGames, peasantsWinRate))

    print()
    print("Most recent weights for features:")
    print(weights[-1])
    return weights[-1]


if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    runGames(**args)
    print("done")
