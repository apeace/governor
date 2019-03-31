import random
from typing import List

import kingsburg

class Player():
    """
    Makes decisions based on game state.
    """

    def __init__(self, name):
        self.name = name

    def pickFreeResource(self, state: kingsburg.State) -> str:
        raise NotImplementedError

    def rollDice(self, state: kingsburg.State) -> kingsburg.DiceRoll:
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

    def rollDice(self, state: kingsburg.State) -> kingsburg.DiceRoll:
        num = state.getNumDice(self.name)
        rolls = input(self.name + " rolls " + str(num) + " dice: ")
        dice = rolls.split()
        if len(dice) != num:
            return self.rollDice(state)
        return [int(die) for die in dice]

class RandomPlayer(Player):
    """
    A player which makes completely random choices.
    """

    def pickFreeResource(self, state):
        return random.choice(state.pickFreeResourceChoices(self.name))

    def rollDice(self, state: kingsburg.State) -> kingsburg.DiceRoll:
        dice: List[int] = []
        for i in range(0, state.getNumDice(self.name)):
            dice.append(random.randint(1, 6))
        return dice
