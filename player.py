import random
from typing import Sequence

import kingsburg

class Player():
    """
    Makes decisions based on game state.
    """
    def __init__(self, name):
        self.name = name

    def pickFreeResource(self, state: kingsburg.State) -> str:
        raise NotImplementedError

class CliPlayer(Player):
    """
    A player which asks for choices via CLI.
    """

    def pickFreeResource(self, state):
        resource = input(self.name + " picks free resource: ")
        if resource not in kingsburg.RESOURCES:
            print("That's not a resource")
            return self.pickFreeResource(state)
        return resource

class AutomatedChoicePlayer(Player):
    """
    A player type that auto-generates all possible choices
    and picks one of them.
    """

    def pickFreeResource_choices(self, state: kingsburg.State) -> Sequence[str]:
        return kingsburg.RESOURCES

class RandomPlayer(AutomatedChoicePlayer):

    def pickFreeResource(self, state):
        return random.choice(self.pickFreeResource_choices(state))
