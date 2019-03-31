from __future__ import annotations
import copy
from typing import Dict, Union, List

import util

##############################################
# Resources
##############################################

Resource = str
ResourceInventory = Dict[Resource, int]

RESOURCE_GOLD: Resource = "gold"
RESOURCE_STONE: Resource = "stone"
RESOURCE_WOOD: Resource = "wood"

RESOURCES: List[Resource] = [RESOURCE_GOLD, RESOURCE_STONE, RESOURCE_WOOD]

##############################################
# Buildings
##############################################

Building = str

BUILDING_STATUE: Building = "statue"
BUILDING_CHAPEL: Building = "chapel"
BUILDING_CHURCH: Building = "church"
BUILDING_CATHEDRAL: Building = "cathedral"
BUILDING_INN: Building = "inn"
BUILDING_MARKET: Building = "market"
BUILDING_FARMS: Building = "farms"
BUILDING_MERCHANTS_GUILD: Building = "merchants-guild"
BUILDING_GUARD_TOWER: Building = "guard-tower"
BUILDING_BLACKSMITH: Building = "blacksmith"
BUILDING_BARRACKS: Building = "barracks"
BUILDING_WIZARDS_GUILD: Building = "wizards-guild"
BUILDING_PALISADE: Building = "palisade"
BUILDING_STABLE: Building = "stable"
BUILDING_STONE_WALL: Building = "stone-wall"
BUILDING_FORTRESS: Building = "fortress"
BUILDING_BARRICADE: Building = "barricade"
BUILDING_CRANE: Building = "crane"
BUILDING_TOWN_HALL: Building = "town-hall"
BUILDING_EMBASSY: Building = "embassy"

PROVINCE_SHEET: List[List[Building]] = [
    [BUILDING_STATUE, BUILDING_CHAPEL, BUILDING_CHURCH, BUILDING_CATHEDRAL],
    [BUILDING_INN, BUILDING_MARKET, BUILDING_FARMS, BUILDING_MERCHANTS_GUILD],
    [BUILDING_GUARD_TOWER, BUILDING_BLACKSMITH, BUILDING_BARRACKS, BUILDING_WIZARDS_GUILD],
    [BUILDING_PALISADE, BUILDING_STABLE, BUILDING_STONE_WALL, BUILDING_FORTRESS],
    [BUILDING_BARRICADE, BUILDING_CRANE, BUILDING_TOWN_HALL, BUILDING_EMBASSY],
]

##############################################
# Phases
##############################################

Phase = str

PHASE_KINGS_FAVOR: Phase = "kings-favor"
PHASE_SPRING: Phase = "spring"
PHASE_KINGS_REWARD: Phase = "kings-reward"
PHASE_SUMMER: Phase = "summer"
PHASE_KINGS_ENVOY: Phase = "kings-envoy"
PHASE_FALL: Phase = "fall"
PHASE_RECRUIT_SOLDIERS: Phase = "recruit-soldiers"
PHASE_WINTER: Phase = "winter"

PHASES: List[Phase] = [
    PHASE_KINGS_FAVOR, PHASE_SPRING, PHASE_KINGS_REWARD, PHASE_SUMMER,
    PHASE_KINGS_ENVOY, PHASE_FALL, PHASE_RECRUIT_SOLDIERS, PHASE_WINTER
]

MAX_YEAR = 5
MAX_PHASE = len(PHASES) - 1

PRODUCTIVE_SEASONS: List[Phase] = [
    PHASE_SPRING, PHASE_SUMMER, PHASE_FALL
]

KINGS_FAVOR_TIE = "tie"

##############################################
# Advisors
##############################################

AdvisorScore = int

ADVISOR_JESTER: AdvisorScore = 1
ADVISOR_SQUIRE: AdvisorScore = 2
ADVISOR_ARCHITECT: AdvisorScore = 3
ADVISOR_MERCHANT: AdvisorScore = 4
ADVISOR_SERGEANT: AdvisorScore = 5
ADVISOR_ALCHEMIST: AdvisorScore = 6
ADVISOR_ASTRONOMER: AdvisorScore = 7
ADVISOR_TREASURER: AdvisorScore = 8
ADVISOR_MASTER_HUNTER: AdvisorScore = 9
ADVISOR_GENERAL: AdvisorScore = 10
ADVISOR_SWORDSMITH: AdvisorScore = 11
ADVISOR_DUCHESS: AdvisorScore = 12
ADVISOR_CHAMPION: AdvisorScore = 13
ADVISOR_SMUGGLER: AdvisorScore = 14
ADVISOR_INVENTOR: AdvisorScore = 15
ADVISOR_WIZARD: AdvisorScore = 16
ADVISOR_QUEEN: AdvisorScore = 17
ADVISOR_KING: AdvisorScore = 18

ADVISORS: List[AdvisorScore] = [
    ADVISOR_JESTER, ADVISOR_SQUIRE, ADVISOR_ARCHITECT, ADVISOR_MERCHANT,
    ADVISOR_SERGEANT, ADVISOR_ALCHEMIST, ADVISOR_ASTRONOMER, ADVISOR_TREASURER,
    ADVISOR_MASTER_HUNTER, ADVISOR_GENERAL, ADVISOR_SWORDSMITH, ADVISOR_DUCHESS,
    ADVISOR_CHAMPION, ADVISOR_SMUGGLER, ADVISOR_INVENTOR, ADVISOR_WIZARD,
    ADVISOR_QUEEN, ADVISOR_KING
]

ADVISOR_MAX = len(ADVISORS)

class Advisor():
    """
    Represents an advisor which has a name and a set
    of rewards it can give.
    """

##############################################
# Die
##############################################

DiceRoll = List[int]

class ProductiveSeasonRoll():
    """
    Represents a productive season dice roll.
    For each productive season, players roll three dice.
    They may also have bonus dice to roll.
    """

    def __init__(self, player_dice: DiceRoll, bonus_dice: DiceRoll):
        self.player_dice: DiceRoll = player_dice
        self.bonus_dice: DiceRoll = bonus_dice

    def totalValue(self) -> int:
        """
        Returns the total value of all player dice and hit dice together.
        """
        total = 0
        for die in self.player_dice:
            total += die
        for die in self.bonus_dice:
            total += die
        return total

class AdvisorInfluence():
    """
    Represents a combination of player dice, bonus dice,
    plustwo tokens, and market influence used to influence
    a particular advisor.

    Only zero or one plustwo tokens may be used.

    Zero or more bonus dice may be used, but they must be used
    in combination with at least one player dice.

    The Market building may be used to add one or minus one
    to a given roll.
    """

    def __init__(self, player_dice: DiceRoll, bonus_dice: DiceRoll, plus_two: bool=False, market_modifier: int=0):
        self.player_dice: DiceRoll = player_dice
        self.bonus_dice: DiceRoll = bonus_dice
        self.plus_two: bool = plus_two
        self.market_modifier: int = market_modifier

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def advisorScore(self) -> AdvisorScore:
        total = 0
        for die in self.player_dice:
            total += die
        for die in self.bonus_dice:
            total += die
        if self.plus_two:
            total += 2
        total += self.market_modifier
        return total

##############################################
# Game state
##############################################

# TODO instead of throwing exceptions, log messages and return same state
# err, set error state so that Game knows to redo step

class State():
    """
    Tracks state of a game, implements state transitions, and
    computes possible next moves.
    """

    def __init__(self):
        self.messages: List[str] = []
        self.players: Dict[str, PlayerState] = {}
        self.over: bool = False
        self.year: int = 1
        self.phase: int = 0
        self.last_phase_played: int = -1
        self.turn_order: List[str] = []
        self.taken_advisors = Dict[AdvisorScore, List[str]]

    def copy(self) -> State:
        return copy.deepcopy(self)

    def message(self, message) -> State:
        state = self.copy()
        state.messages.append(message)
        return state

    def clearMessages(self) -> State:
        state = self.copy()
        state.messages = []
        return state

    def playerList(self) -> List[PlayerState]:
        return [self.players[name] for name in self.players]

    def updatePlayer(self, name: str, player: PlayerState) -> State:
        state = self.copy()
        state.players[name] = player
        return state

    def setPlayers(self, playerNames: List[str]) -> State:
        """
        Initialize player states and turn order.
        The rules specify that the initial turn order should be "random".
        Therefore, it is assumed the playerNames input has already been
        randomized by whatever method the Engine chose.
        """
        state = self.copy()
        for name in playerNames:
            player = PlayerState(name)
            state.players[name] = player
            state.turn_order.append(name)
        return state

    def nextYear(self) -> State:
        state = self.copy()
        if state.year == MAX_YEAR:
            state.over = True
        else:
            state.year += 1
        return state

    def nextPhase(self) -> State:
        state = self.copy()
        if state.phase == MAX_PHASE:
            state = state.nextYear()
            if not state.over:
                state.phase = 0
        else:
            state.phase += 1
        return state.message("Transitioning to year: " + str(state.year) + ", phase: " + PHASES[state.phase])

    def phaseComplete(self, phase: Phase) -> State:
        if phase != PHASES[self.phase]:
            raise Exception("Completed the wrong phase")
        state = self.copy()
        state.last_phase_played = self.phase
        return state

    def kingsFavor(self) -> Union[State, str]:
        """
        Phase 1: The King's Favor

        The player with the fewest buildings gets a bonus die.
        If there is a tie for fewest buildings, the player with
        the fewest resources gets a bonus die. If there is a tie
        for fewest resources, each player chooses one free resource.

        If a player wins the king's favor, returns the updated state.
        If there is a tie, returns KINGS_FAVOR_TIE.

        In the case of a tie, games should call takeFreeResource for
        each player.
        """
        building_count = {}
        resource_count = {}
        for name in self.players:
            player = self.players[name]
            building_count[name] = len(player.buildings)
            resource_count[name] = 0
            for resource in player.resources:
                resource_count[name] += player.resources[resource]

        fewest_buildings = util.lowest(building_count)
        if fewest_buildings is not None:
            return self.message(fewest_buildings + " has the fewest buildings").giveKingsFavorBonusDie(fewest_buildings)

        fewest_resources = util.lowest(resource_count)
        if fewest_resources is not None:
            return self.message(fewest_resources + " has the fewest resources").giveKingsFavorBonusDie(fewest_resources)

        return KINGS_FAVOR_TIE

    def takeFreeResource(self, name: str, resource: Resource) -> State:
        """
        Gives one of the given resource to the given player.
        """
        return self.giveResources(name, {resource: 1})

    def giveResources(self, name: str, resources: ResourceInventory):
        """
        Gives the given resources to the given player.
        """
        resource_message = []
        for resource in resources:
            amount = resources[resource]
            if amount >= 0:
                resource_message.append("+" + str(amount) + " " + resource)
            else:
                resource_message.append("-" + str(amount) + " " + resource)
        message = name + ": " + ",".join(resource_message)
        player = self.players[name]
        return self.message(message).updatePlayer(name, player.addResources(resources))

    def giveBuilding(self, name: str, building: Building):
        """
        Gives the given building to the given player.
        """
        player = self.players[name]
        return self.updatePlayer(name, player.addBuilding(building))

    def giveKingsFavorBonusDie(self, name: str):
        """
        Gives a bonus die to the given player.
        """
        message = name + " gets King's Favor bonus die"
        player = self.players[name]
        return self.message(message).updatePlayer(name, player.addKingsFavorBonusDie())

    def getNumPlayerDice(self, name: str) -> int:
        """
        Returns the number of player dice the given player can roll
        for the current productive season.
        """
        return self.players[name].getNumPlayerDice(PHASES[self.phase])

    def getNumBonusDice(self, name: str) -> int:
        """
        Returns the number of bonus dice the given player can roll
        for the current productive season.
        """
        return self.players[name].getNumBonusDice(PHASES[self.phase])

    def productiveSeasonRolls(self, rolls: Dict[str, ProductiveSeasonRoll]) -> State:
        """
        Sets the productive season rolls for each player.
        Sets the turn order.
        Resets bonus die.
        """
        state = self.copy()

        # Update player rolls.
        for name in state.players:
            player = state.players[name]
            roll = rolls[name]
            roll.player_dice.sort()
            roll.bonus_dice.sort()
            message = name + " rolled player dice: " + ", ".join([str(die) for die in roll.player_dice])
            if len(roll.bonus_dice) > 0:
                message += ", bonus dice: " + ", ".join([str(die) for die in roll.bonus_dice])
            state = state.message(message)
            state = state.updatePlayer(name, player.roll(roll))

        # Set turn order. The lowest total roll goes first.
        # If there is a tie, the tied players maintain the
        # same order in relation to each other that they
        # had in the existing turn order.
        rollers_by_score: Dict[int, List[str]] = {}
        for name in rolls:
            score = rolls[name].totalValue()
            if score not in rollers_by_score:
                rollers_by_score[score] = []
            rollers_by_score[score].append(name)
        scores: List[int] = []
        for score in rollers_by_score:
            scores.append(score)
        scores.sort()
        new_turn_order: List[str] = []
        for score in scores:
            if len(rollers_by_score[score]) == 1:
                new_turn_order.append(rollers_by_score[score][0])
            else:
                for name in state.turn_order:
                    if name in rollers_by_score[score]:
                        new_turn_order.append(name)
        state.turn_order = new_turn_order

        return state

    def choices_freeResource(self, name: str) -> List[Resource]:
        """
        Returns the list of resources available to the given player
        when picking a free resource.
        """
        return RESOURCES

    def choices_advisorInfluence(self, name: str) -> List[AdvisorInfluence]:
        available: List[AdvisorScore] = []
        for advisor in ADVISORS:
            if advisor not in self.taken_advisors:
                available.append(advisor)
        return self.players[name].choices_advisorInfluence(available)

##############################################
# Player state
##############################################

class PlayerState():
    """
    Tracks the state of an individual player.
    """

    def __init__(self, name: str):
        self.name: str = name
        self.has_kings_favor_bonus_die: bool = False
        self.has_kings_envoy = False
        self.used_kings_envoy = False
        self.plustwo_tokens = 0
        self.used_plustwo_token = False
        self.used_market = False
        self.buildings: List[Building] = []
        self.resources: ResourceInventory = {
            RESOURCE_WOOD: 0,
            RESOURCE_GOLD: 0,
            RESOURCE_STONE: 0
        }
        self.dice: ProductiveSeasonRoll = ProductiveSeasonRoll([], [])

    def copy(self) -> PlayerState:
        return copy.deepcopy(self)

    def addResources(self, resources: ResourceInventory) -> PlayerState:
        """
        Adds the given resources to this player's resources.
        """
        state = self.copy()
        for resource in resources:
            state.resources[resource] += resources[resource]
        return state

    def addBuilding(self, building: Building) -> PlayerState:
        """
        Adds the given building to this player's buildings.
        """
        if building in self.buildings:
            raise Exception("Adding an already-owned building")
        state = self.copy()
        state.buildings.append(building)
        return state

    def addKingsFavorBonusDie(self) -> PlayerState:
        """
        Adds a bonus die to this player.
        """
        state = self.copy()
        state.has_kings_favor_bonus_die = True
        return state

    def getNumPlayerDice(self, phase: Phase) -> int:
        """
        Returns the number of player dice this player can roll
        for the given productive season.
        To my knowledge this is always 3, as any additional
        dice gained are bonus dice, not player dice. I left
        this as a method just in case I was wrong.
        """
        return 3

    def getNumBonusDice(self, phase: Phase) -> int:
        """
        Returns the number of bonus dice this player can roll
        for the given productive season.
        """
        num = 0
        if self.has_kings_favor_bonus_die:
            num += 1
        if BUILDING_FARMS in self.buildings:
            num += 1
        return num

    def roll(self, roll: ProductiveSeasonRoll) -> PlayerState:
        """
        Set's this player's roll to the given roll.
        Resets bonus die.
        """
        state = self.copy()
        state.dice = copy.deepcopy(roll)
        state.has_kings_favor_bonus_die = False
        return state

    def choices_advisorInfluence(self, available: List[AdvisorScore]) -> List[AdvisorInfluence]:
        # Determine available market modifiers.
        market_modifiers: List[int] = []
        if not self.used_market and BUILDING_MARKET in self.buildings:
            market_modifiers = [-1, 1]

        # Determine available plustwo modifiers.
        plustwos: List[int] = []
        if not self.used_plustwo_token and self.plustwo_tokens > 0:
            plustwos = [1]

        # Determine all unique combinations of each component.
        player_dice_combos = util.unique_combinations(self.dice.player_dice)
        bonus_dice_combos = util.unique_combinations(self.dice.bonus_dice)
        plustwo_combos = util.unique_combinations(plustwos)
        market_combos = util.unique_combinations(market_modifiers, 1)

        # Determine all possible moves.
        all_possible_moves = util.unique_list_pairs(
            util.unique_list_pairs(
                util.unique_list_pairs(player_dice_combos, bonus_dice_combos),
                plustwo_combos
            ),
            market_combos
        )

        possible_influences: List[AdvisorInfluence] = []
        for move in all_possible_moves:
            player_dice: DiceRoll = move[0][0][0]
            bonus_dice: DiceRoll = move[0][0][1]
            plustwo: bool = len(move[0][1]) > 0
            market_modifier: int = move[1][0] if len(move[1]) > 0 else 0
            influence = AdvisorInfluence(player_dice, bonus_dice, plustwo, market_modifier)
            score = influence.advisorScore()
            # Can't score below 1 or above 18.
            if score < 1 or score > ADVISOR_MAX:
                continue
            # Must use at least one player die.
            if len(influence.player_dice) == 0:
                continue
            # If the player has the king's envoy and has not used it
            # yet, they can influence already-influenced advisors
            # Otherwise, in order for the move to be valid, it must be
            # in the list of available advisors.
            if (not self.has_kings_envoy or self.used_kings_envoy) and score not in available:
                continue
            possible_influences.append(influence)

        return possible_influences
