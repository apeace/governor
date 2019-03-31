from typing import Union, List
import collections

import kingsburg

class Logger():
    """
    Logs game state.
    """
    def log(self, state: kingsburg.State, message: Union[str, List[str], None]=None):
        pass

    def start(self, state: kingsburg.State):
        pass

    def over(self, state: kingsburg.State):
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
        print("Phase: " + kingsburg.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.endLog()

    def start(self, state):
        self.startLog()
        print("Players: " + str([player.name for player in state.playerList()]))
        print("Year: " + str(state.year))
        print("Phase: " + kingsburg.PHASES[state.phase] + " (" + str(state.phase) + ")")
        self.endLog()

    def over(self, state):
        self.startLog()
        print("Game over!")
        self.endLog()
