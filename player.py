import random

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

class RandomPlayer(Player):
    """
    A player which makes completely random choices.
    """
    def pickFreeResource(self, state):
        return random.choice(state.pickFreeResourceChoices())
