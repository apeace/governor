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

    def log(self, state: kingsburg.State, message: Union[str, List[str], None]=None):
        """
        Let the engine know when states have changed.
        """
        self.logger.log(state, message=message)

    def setupPlayers(self) -> List[str]:
        raise NotImplementedError

    def pickFreeResource(self, state: kingsburg.State, name: str) -> str:
        raise NotImplementedError

    def rollDice(self, state: kingsburg.State, name: str) -> kingsburg.ProductiveSeasonRoll:
        raise NotImplementedError

    def chooseAdvisor(self, state: kingsburg.State, name: str) -> kingsburg.AdvisorInfluence:
        raise NotImplementedError

    def chooseReward(self, state: kingsburg.State, name: str, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        raise NotImplementedError

    def chooseBuilding(self, state: kingsburg.State, name: str, use_kings_envoy: bool) -> kingsburg.Building:
        raise NotImplementedError

    def choices__buildings(self, state: kingsburg.State, name: str) -> List[kingsburg.Building]:
        return state.choices__buildings(name)

class PlayerEngine(Engine):
    """
    Calls on Player objects to make decisions.
    """

    def __init__(self, logger):
        super().__init__(logger)
        self.players: Dict[str, player.Player] = {}

    def pickFreeResource(self, state, name):
        return self.players[name].pickFreeResource(state)

    def rollDice(self, state: kingsburg.State, name: str) -> kingsburg.ProductiveSeasonRoll:
        return self.players[name].rollDice(state)

    def chooseAdvisor(self, state: kingsburg.State, name: str) -> kingsburg.AdvisorInfluence:
        return self.players[name].chooseAdvisor(state)

    def chooseReward(self, state: kingsburg.State, name: str, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        return self.players[name].chooseReward(state, advisorScore, possible_rewards)

    def chooseBuilding(self, state: kingsburg.State, name: str, use_kings_envoy: bool) -> kingsburg.Building:
        return self.players[name].chooseBuilding(state, self.choices__buildings(state, name), use_kings_envoy)

class CliEngine(PlayerEngine):
    """
    Play the game via CLI.
    """

    def wait(self):
        input("")

    def start(self, state):
        super().start(state)
        self.wait()

    def log(self, state, message=None):
        super().log(state, message=message)
        self.wait()

    def setupPlayers(self):
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

    def setupPlayers(self):
        names = ["fred", "george", "ron"]
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

    def log(self, state, message=None):
        return CliEngine.log(self, state, message=message)

    def setupPlayers(self):
        return RandomEngine.setupPlayers(self)

    def chooseReward(self, state: kingsburg.State, name: str, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        return RandomEngine.chooseReward(self, state, name, advisorScore, possible_rewards)

    def chooseBuilding(self, state: kingsburg.State, name: str, use_kings_envoy: bool) -> kingsburg.Building:
        return RandomEngine.chooseBuilding(self, state, name, use_kings_envoy)
