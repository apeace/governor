from typing import Union, List, Dict

import kingsburg
import player
import logger

class Engine():
    """
    Provides inputs necessary to advance through game states.
    """

    def __init__(self, logger: logger.Logger):
        self.logger = logger

    def start(self, state: kingsburg.State):
        """
        Let the engine know the game is starting.
        """
        self.logger.start(state)

    def over(self, state: kingsburg.State):
        """
        Let the engine know the game is over.
        """
        self.logger.over(state)

    def tick(self, state: kingsburg.State, message: Union[str, List[str], None]=None):
        """
        Let the engine know the game has ticked.
        """
        self.logger.log(state, message=message)

    # TODO rename setupPlayers
    def getPlayers(self) -> List[str]:
        raise NotImplementedError

    def pickFreeResource(self, state: kingsburg.State, name: str) -> str:
        raise NotImplementedError

    def rollDice(self, state: kingsburg.State, name: str) -> kingsburg.DiceRoll:
        raise NotImplementedError

class PlayerEngine(Engine):
    """
    Calls on Player objects to make decisions.
    """

    def __init__(self, logger):
        super().__init__(logger)
        self.players: Dict[str, player.Player] = {}

    def pickFreeResource(self, state, name):
        return self.players[name].pickFreeResource(state)

    def rollDice(self, state: kingsburg.State, name: str) -> kingsburg.DiceRoll:
        return self.players[name].rollDice(state)

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
