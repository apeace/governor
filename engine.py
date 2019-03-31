import collections

import game
import player

class Logger():
    """
    Logs game state.
    """
    def log(self, state, message=None):
        pass

    def start(self, state):
        pass

    def over(self, state):
        pass

class SilentLogger(Logger):
    """
    Does not log anything.
    """
    pass

class StdoutLogger(Logger):
    """
    Logs to stdout.
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
        elif isinstance(message, collections.Iterable) and len(message) > 0:
            print("\n".join(["> " + m for m in message]))
        print("Year: " + str(state.year))
        print("Phase: " + game.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.endLog()

    def start(self, state):
        self.startLog()
        print("Players: " + str([player.name for player in state.playerList()]))
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

    # TODO rename setupPlayers
    def getPlayers(self):
        raise NotImplementedError

    def pickFreeResource(self, state, name):
        raise NotImplementedError

class PlayerEngine(Engine):
    """
    Calls on Player objects to make decisions.
    """
    def __init__(self, logger):
        super().__init__(logger)
        self.players = {}

    def pickFreeResource(self, state, name):
        p = self.players[name]
        return p.pickFreeResource(state)

class CliEngine(PlayerEngine):
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
        names = []
        while True:
            name = input("Enter player: ")
            if name == "":
                return names
            names.append(name)
            self.players[name] = player.CliPlayer(name)

class RandomEngine(PlayerEngine):
    """
    Play the game with automated random players.
    """
    def getPlayers(self):
        names =["fred", "george", "ron"]
        for name in names:
            self.players[name] = player.RandomPlayer(name)
        return names

class RandomCliEngine(CliEngine, RandomEngine):
    """
    Play the game with automated random players.
    Press Enter on the CLI to advance the game.
    """
    def __init__(self, logger):
        super(RandomEngine, self).__init__(logger)

    def start(self, state):
        return CliEngine.start(self, state)

    def tick(self, state, message=None):
        return CliEngine.tick(self, state, message=message)

    def getPlayers(self):
        return RandomEngine.getPlayers(self)
