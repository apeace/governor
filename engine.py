import game

class Logger(object):
    """
    Logs game state.
    """

    def start(self):
        print("")
        self.divider()

    def end(self):
        self.divider()
        print("")

    def divider(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def log(self, state):
        self.start()
        print("Year: " + str(state.year))
        print("Phase: " + game.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.end()

    def over(self, state):
        self.start()
        print("Game over!")
        self.end()

class Engine():
    """
    Provides a means to advance through game states.
    """

    def __init__(self, logger):
        self.logger = logger
        self.state = game.State()

    def play(self):
        self.setup()
        while not self.state.over:
            self.state = self.state.nextPhase()
            self.logger.log(self.state)
        self.logger.over(self.state)

    def setup(self):
        self.state.players = self.getPlayers()

    def getPlayers(self):
        raise NotImplementedError

class CliEngine(Engine):
    """
    Play the game via CLI.
    """

    def getPlayers(self):
        players = []
        while True:
            player = input("Enter player: ")
            if player == "":
                return players
            players.append(player)
