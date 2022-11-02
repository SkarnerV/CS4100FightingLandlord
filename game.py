import sys

from Agent import RandomAgent
from Deck import Deck
from Hand import Hand
from GameState import GameState
from Player import Player


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


        # create players with dealt hands of cards
        landlord = loadPlayer("Landlord", landlordType, landlordCards, "LANDLORD")
        peasant1 = loadPlayer("Peasant 1", peasant1Type, peasant1Cards, "PEASANT")
        peasant2 = loadPlayer("Peasant 2", peasant2Type, peasant2Cards, "PEASANT")


        discarded = Hand([]) # discard pile initially empty
        players = [landlord, peasant1, peasant2]
        current = [] # initially no cards in play

        self.state = GameState(discarded, players, current)
        self.moveHistory = []


    def run(self):
        """
        Main control loop for game play
        """
        print(self.state.isTerminal())
        while self.state.isTerminal() == -1:
            # TODO - need method on GameState that outputs string for display

            # Fetch next agent
            agentIndex = self.state.toMove()
            agent = self.state.players[agentIndex]

            # Prompt agent for action - will be a Hand of cards
            action = agent.makeMove(self.state)
            print("Action move: " + action)

            # Execute action
            self.moveHistory.append((agentIndex, action))
            self.state = self.state.generateSuccessor(action)

            #print(self.state.players[0].toString())
            # Change display -- if the player did not pass, print the cards they played
            # if len(action.cards) > 0:
            #     print(action.print())


def loadPlayer(playerName, playerType, initialCards, role):
  """
   Instantiates a player/agent of the given type, initial hand, and player role
  :param playerName: name assigned to player (used when prompting a human player to make a move)
  :param playerType: denotes the implementation of player to be used (ex: 'RandomAgent', 'Human')
  :param initialCards: the player's initial hand of cards
  :param role: "LANDLORD" | "PEASANT"
  :return: a new player with the given attributes
  """
  assert role == "LANDLORD" or role == "PEASANT", "Unknown role: " + role

  playerType = playerType.lower()
  if playerType == 'human':
      return Player(playerName, initialCards, role)
  elif playerType == 'randomagent':
      return RandomAgent(playerName, initialCards, role)
  else:
      raise Exception("Unknown player type: " + playerType)



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

def runGames(landlordType, peasant1Type, peasant2Type, numGames):
    """
    Run multiple games in succession and report landlord rate of winning
    """
    games = []

    # run all games
    for i in range(numGames):
        game = Game(landlordType, peasant1Type, peasant2Type)
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