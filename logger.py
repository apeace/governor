from typing import Union, Sequence
import collections

import game

class Logger():
    """
    Logs game state.
    """
    def log(self, state: game.State, message: Union[str, Sequence[str], None]=None):
        pass

    def start(self, state: game.State):
        pass

    def over(self, state: game.State):
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
