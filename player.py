import random
from typing import List, Optional

import keras
import numpy

import kingsburg
import training
import util

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

    def chooseAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        raise NotImplementedError

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> Optional[kingsburg.Reward]:
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

    def chooseAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        # TODO
        return kingsburg.ADVISOR_INFLUENCE_PASS

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> Optional[kingsburg.Reward]:
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

    def chooseAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        # Give a bias towards not passing.
        # Pass will happen 5% of the time, unless it is the only option.
        choices = state.choices__advisorInfluence(self.name)
        if len(choices) == 1:
            return choices[0]
        if random.randint(0, 100) > 95:
            return kingsburg.ADVISOR_INFLUENCE_PASS
        choices = [c for c in choices if c != kingsburg.ADVISOR_INFLUENCE_PASS]
        return random.choice(choices)

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> Optional[kingsburg.Reward]:
        if len(possible_rewards) == 0:
            return None
        return random.choice(possible_rewards)

    def chooseBuilding(self, state: kingsburg.State, choices: List[kingsburg.Building], use_kings_envoy: bool) -> kingsburg.Building:
        # Give a bias towards not passing.
        # Pass will happen 5% of the time, unless it is the only option.
        choices = state.choices__buildings(self.name)
        if len(choices) == 1:
            return choices[0]
        if random.randint(0, 100) > 95:
            return kingsburg.BUILD_PASS
        choices = [c for c in choices if c != kingsburg.BUILD_PASS]
        return random.choice(choices)

class GovAlphaPlayer(RandomPlayer):
    """
    The Governor.
    The very first version where I was just messing around.
    """

    def __init__(self, name, filename):
        Player.__init__(self, name)
        self.model = keras.models.load_model(filename)

    def pickFreeResource(self, state: kingsburg.State) -> str:
        choices = state.choices_freeResource(self.name)
        scored_choices = []
        for c in choices:
            new_state = state.takeFreeResource(self.name, c)
            inp = training.state_to_input(new_state)
            prediction = self.model.predict(numpy.asarray([inp]))[0][0]
            scored_choices.append((prediction, c))
        print(str(scored_choices))
        chosen = util.pick_best(scored_choices)
        print("Score: " + str(chosen[0]))
        return chosen[1]

    def chooseAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        choices = state.choices__advisorInfluence(self.name)
        scored_choices = []
        for c in choices:
            new_state = state.influenceAdvisor(self.name, c)
            inp = training.state_to_input(new_state)
            prediction = self.model.predict(numpy.asarray([inp]))[0][0]
            scored_choices.append((prediction, c))
        print(str(scored_choices))
        chosen = util.pick_best(scored_choices)
        print("Score: " + str(chosen[0]))
        return chosen[1]

    def chooseReward(self, state: kingsburg.State, advisorScore: kingsburg.AdvisorScore, possible_rewards: List[kingsburg.Reward]) -> Optional[kingsburg.Reward]:
        scored_choices = []
        for c in possible_rewards:
            new_state = state.giveReward(self.name, advisorScore, c)
            inp = training.state_to_input(new_state)
            prediction = self.model.predict(numpy.asarray([inp]))[0][0]
            scored_choices.append((prediction, c))
        print(str(scored_choices))
        chosen = util.pick_best(scored_choices)
        print("Score: " + str(chosen[0]))
        return chosen[1]

    def chooseBuilding(self, state: kingsburg.State, choices: List[kingsburg.Building], use_kings_envoy: bool) -> kingsburg.Building:
        scored_choices = []
        for c in choices:
            new_state = state.giveBuilding(self.name, c, use_kings_envoy)
            inp = training.state_to_input(new_state)
            prediction = self.model.predict(numpy.asarray([inp]))[0][0]
            scored_choices.append((prediction, c))
        print(str(scored_choices))
        chosen = util.pick_best(scored_choices)
        print("Score: " + str(chosen[0]))
        return chosen[1]

class GovAlpha2Player(RandomPlayer):
    """
    The Governor.
    The second version where I tried a different neural net.

    Currently makes random choices for everything except placing dice.
    TODO: All other choices.
    """

    def __init__(self, name, filename):
        Player.__init__(self, name)
        self.advisor_chooser = keras.models.load_model(filename + '_advisor_chooser')

    def chooseAdvisor(self, state: kingsburg.State) -> kingsburg.AdvisorInfluence:
        choices = state.choices__advisorInfluence(self.name)
        best_choice = None
        best_choice_score = None
        base_inputs = training.state_to_input(state)
        for c in choices:
            additional_inputs = training.advisor_choice_to_input(state, c)
            inputs = base_inputs + additional_inputs
            prediction = self.advisor_chooser.predict(numpy.asarray([inputs]))[0][0]
            if best_choice_score is None or prediction > best_choice_score:
                best_choice_score = prediction
                best_choice = c
        print("Score: " + str(best_choice_score))
        return best_choice
