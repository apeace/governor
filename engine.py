import collections

import game

class Logger():
    """
    Logs game state.
    """
    def startLog(self):
        print("")
        self.divider()

    def endLog(self):
        self.divider()

    def divider(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def log(self, state, message=None):
        self.startLog()
        if isinstance(message, str):
            print("> " + message)
        elif isinstance(message, collections.Iterable):
            print("\n".join(["> " + m for m in message]))
        print("Year: " + str(state.year))
        print("Phase: " + game.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.endLog()

    def start(self, state):
        self.startLog()
        print("Players: " + str([player.name for player in state.players]))
        print("Year: " + str(state.year))
        print("Phase: " + game.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.endLog()

    def over(self, state):
        self.startLog()
        print("Game over!")
        self.endLog()

class Engine():
    """
    Provides a means to advance through game states.
    """
    def __init__(self, logger):
        self.logger = logger

    def start(self, state):
        """
        Let the engine know the game is starting.
        """
        self.logger.start(state)

    def over(self, state):
        """
        Let the engine know the game is over.
        """
        self.logger.over(state)

    def tick(self, state, message=None):
        """
        Let the engine know the game has ticked.
        """
        self.logger.log(state, message=message)

    def getPlayers(self):
        raise NotImplementedError

class CliEngine(Engine):
    """
    Play the game via CLI.
    """
    def wait(self):
        input("")

    def start(self, state):
        super().start(state)
        self.wait()

    def tick(self, state, message=None):
        super().tick(state, message=message)
        self.wait()

    def getPlayers(self):
        players = []
        while True:
            player = input("Enter player: ")
            if player == "":
                return players
            players.append(player)
