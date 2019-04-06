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

    def rollDice(self, state: kingsburg.State) -> kingsburg.ProductiveSeasonRoll:
        raise NotImplementedError

    def influenceAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        raise NotImplementedError

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        raise NotImplementedError

    def chooseBuilding(self, state: kingsburg.State, choices: List[kingsburg.Building], use_kings_envoy: bool) -> kingsburg.Building:
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

    def rollDice(self, state: kingsburg.State) -> kingsburg.ProductiveSeasonRoll:
        numpdice = state.getNumPlayerDice(self.name)
        numbdice = state.getNumBonusDice(self.name)
        rolls = input(self.name + " rolls " + str(numpdice) + " player dice: ")
        pdice = rolls.split()
        bdice: List[str] = []
        if numbdice > 0:
            rolls = input(self.name + " rolls " + str(numpdice) + " bonus dice: ")
            bdice = rolls.split()
        if len(pdice) != numpdice or len(bdice) != numbdice:
            return self.rollDice(state)
        return kingsburg.ProductiveSeasonRoll(
            player_dice=[int(die) for die in pdice],
            bonus_dice=[int(die) for die in bdice]
        )

    def influenceAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        # TODO
        return kingsburg.ADVISOR_INFLUENCE_PASS

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        # TODO
        raise NotImplementedError

    def chooseBuilding(self, state: kingsburg.State, choices: List[kingsburg.Building], use_kings_envoy: bool) -> kingsburg.Building:
        # TODO
        raise NotImplementedError

class RandomPlayer(Player):
    """
    A player which makes completely random choices.
    Dice rolls are randomly generated.
    """

    def pickFreeResource(self, state):
        return random.choice(state.choices_freeResource(self.name))

    def rollDice(self, state: kingsburg.State) -> kingsburg.ProductiveSeasonRoll:
        pdice: List[int] = []
        bdice: List[int] = []
        for i in range(0, state.getNumPlayerDice(self.name)):
            pdice.append(random.randint(1, 6))
        for i in range(0, state.getNumBonusDice(self.name)):
            bdice.append(random.randint(1, 6))
        return kingsburg.ProductiveSeasonRoll(
            player_dice=pdice,
            bonus_dice=bdice
        )

    def influenceAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        return random.choice(state.choices_advisorInfluence(self.name))

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> kingsburg.Reward:
        return random.choice(possible_rewards)

    def chooseBuilding(self, state: kingsburg.State, choices: List[kingsburg.Building], use_kings_envoy: bool) -> kingsburg.Building:
        return random.choice(choices)
