from __future__ import annotations
import copy
from typing import Dict, Union, List, Optional

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

class Reward():
    """
    Represents a reward or a penalty that can be given to a player.
    """

    def __init__(
            self,
            victory_points: int=0,
            resources: Optional[ResourceInventory]=None,
            soldiers: int=0,
            plustwos: int=0,
            receive_any_resource: int=0,
            view_enemy: bool=False
    ):
        self.victory_points: int = victory_points
        self.resources: ResourceInventory = {} if resources is None else resources
        self.soldiers: int = soldiers
        self.plustwos: int = plustwos
        self.receive_any_resource: int = receive_any_resource
        self.view_enemy: bool = view_enemy

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

# A lookup of the possible resource inventories you can get based on
# a reward of "receive_any_resource" of the given amount.
# I was too lazy to write code to generate these.
# And it's... more efficient...
RECEIVE_ANY_RESOURCE: Dict[int, List[ResourceInventory]] = {
    1: [
        {RESOURCE_GOLD: 1},
        {RESOURCE_STONE: 1},
        {RESOURCE_WOOD: 1},
    ],
    2: [
        {RESOURCE_GOLD: 2},
        {RESOURCE_STONE: 2},
        {RESOURCE_WOOD: 2},
        {RESOURCE_GOLD: 1, RESOURCE_WOOD: 1},
        {RESOURCE_GOLD: 1, RESOURCE_STONE: 1},
        {RESOURCE_STONE: 1, RESOURCE_WOOD: 1},
    ],
    3: [
        {RESOURCE_GOLD: 3},
        {RESOURCE_STONE: 3},
        {RESOURCE_WOOD: 3},
        {RESOURCE_GOLD: 2, RESOURCE_WOOD: 1},
        {RESOURCE_GOLD: 2, RESOURCE_STONE: 1},
        {RESOURCE_WOOD: 2, RESOURCE_GOLD: 1},
        {RESOURCE_WOOD: 2, RESOURCE_STONE: 1},
        {RESOURCE_STONE: 2, RESOURCE_WOOD: 1},
        {RESOURCE_STONE: 2, RESOURCE_GOLD: 1},
        {RESOURCE_WOOD: 1, RESOURCE_GOLD: 1, RESOURCE_STONE: 1},
    ]
}

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

BUILD_PASS: Building = "pass"

BUILDING_VP: Dict[Building, int] = {
    BUILDING_STATUE: 3,
    BUILDING_CHAPEL: 5,
    BUILDING_CHURCH: 7,
    BUILDING_CATHEDRAL: 9,
    BUILDING_INN: 0,
    BUILDING_MARKET: 1,
    BUILDING_FARMS: 2,
    BUILDING_MERCHANTS_GUILD: 4,
    BUILDING_GUARD_TOWER: 1,
    BUILDING_BLACKSMITH: 2,
    BUILDING_BARRACKS: 4,
    BUILDING_WIZARDS_GUILD: 6,
    BUILDING_PALISADE: 0,
    BUILDING_STABLE: 2,
    BUILDING_STONE_WALL: 2,
    BUILDING_FORTRESS: 4,
    BUILDING_BARRICADE: 0,
    BUILDING_CRANE: 1,
    BUILDING_TOWN_HALL: 2,
    BUILDING_EMBASSY: 4,
}

BUILDING_COST: Dict[Building, ResourceInventory] = {
    BUILDING_STATUE: {RESOURCE_GOLD: -2},
    BUILDING_CHAPEL: {RESOURCE_GOLD: -3, RESOURCE_STONE: -1},
    BUILDING_CHURCH: {RESOURCE_GOLD: -3, RESOURCE_WOOD: -1, RESOURCE_STONE: -2},
    BUILDING_CATHEDRAL: {RESOURCE_GOLD: -5, RESOURCE_STONE: -3},
    BUILDING_INN: {RESOURCE_GOLD: -1, RESOURCE_WOOD: -1},
    BUILDING_MARKET: {RESOURCE_GOLD: -2, RESOURCE_WOOD: -2},
    BUILDING_FARMS: {RESOURCE_GOLD: -2, RESOURCE_WOOD: -3, RESOURCE_STONE: -1},
    BUILDING_MERCHANTS_GUILD: {RESOURCE_GOLD: -3, RESOURCE_WOOD: -1, RESOURCE_STONE: -2},
    BUILDING_GUARD_TOWER: {RESOURCE_GOLD: -1, RESOURCE_STONE: -1},
    BUILDING_BLACKSMITH: {RESOURCE_GOLD: -1, RESOURCE_WOOD: -2},
    BUILDING_BARRACKS: {RESOURCE_GOLD: -2, RESOURCE_WOOD: -2, RESOURCE_STONE: -1},
    BUILDING_WIZARDS_GUILD: {RESOURCE_GOLD: -3, RESOURCE_WOOD: -2, RESOURCE_STONE: -2},
    BUILDING_PALISADE: {RESOURCE_WOOD: -2},
    BUILDING_STABLE: {RESOURCE_GOLD: -1, RESOURCE_WOOD: -1, RESOURCE_STONE: -1},
    BUILDING_STONE_WALL: {RESOURCE_GOLD: -2, RESOURCE_STONE: -2},
    BUILDING_FORTRESS: {RESOURCE_GOLD: -3, RESOURCE_STONE: -2},
    BUILDING_BARRICADE: {RESOURCE_WOOD: -1},
    BUILDING_CRANE: {RESOURCE_WOOD: -1, RESOURCE_STONE: -1},
    BUILDING_TOWN_HALL: {RESOURCE_GOLD: -2, RESOURCE_WOOD: -1, RESOURCE_STONE: -1},
    BUILDING_EMBASSY: {RESOURCE_GOLD: -2, RESOURCE_WOOD: -2, RESOURCE_STONE: -2},
}

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
    def __init__(self, name: str, rewards: List[Reward]):
        self.name: str = name
        self.rewards: List[Reward] = rewards

    def choices__rewards(self, player_resources: ResourceInventory) -> List[Reward]:
        possible_rewards = []
        for reward in self.rewards:
            skip_reward = False
            # Can't trade a resource if you don't have it
            for resource in RESOURCES:
                player_amount = player_resources[resource] if resource in player_resources else 0
                if resource in reward.resources and (reward.resources[resource] + player_amount < 0):
                    skip_reward = True
                    continue
            # If you can receive any resource, then instead of adding this
            # reward directly to the list we'll generate all possible resource rewards.
            if reward.receive_any_resource > 0:
                for resource_reward in RECEIVE_ANY_RESOURCE[reward.receive_any_resource]:
                    rew = copy.deepcopy(reward)
                    rew.receive_any_resource = 0
                    rew.resources = resource_reward
                    possible_rewards.append(rew)
                continue
            if not skip_reward:
                possible_rewards.append(reward)
        return possible_rewards

ADVISOR = {
    ADVISOR_JESTER: Advisor("jester", [Reward(victory_points=1)]),
    ADVISOR_SQUIRE: Advisor("squire", [Reward(resources={RESOURCE_GOLD: 1})]),
    ADVISOR_ARCHITECT: Advisor("architect", [Reward(resources={RESOURCE_WOOD: 1})]),
    ADVISOR_MERCHANT: Advisor("merchant", [Reward(resources={RESOURCE_WOOD: 1}), Reward(resources={RESOURCE_GOLD: 1})]),
    ADVISOR_SERGEANT: Advisor("sergeant", [Reward(soldiers=1)]),
    ADVISOR_ALCHEMIST: Advisor("alchemist", [
        Reward(resources={RESOURCE_WOOD: -1, RESOURCE_GOLD: 1, RESOURCE_STONE: 1}),
        Reward(resources={RESOURCE_WOOD: 1, RESOURCE_GOLD: -1, RESOURCE_STONE: 1}),
        Reward(resources={RESOURCE_WOOD: 1, RESOURCE_GOLD: 1, RESOURCE_STONE: -1}),
    ]),
    ADVISOR_ASTRONOMER: Advisor("astronomer", [Reward(receive_any_resource=1, plustwos=1)]),
    ADVISOR_TREASURER: Advisor("treasurer", [Reward(resources={RESOURCE_GOLD: 2})]),
    ADVISOR_MASTER_HUNTER: Advisor("master-hunter", [Reward(resources={RESOURCE_WOOD: 1, RESOURCE_GOLD: 1}), Reward(resources={RESOURCE_WOOD: 1, RESOURCE_STONE: 1})]),
    ADVISOR_GENERAL: Advisor("general", [Reward(soldiers=2, view_enemy=True)]),
    ADVISOR_SWORDSMITH: Advisor("swordsmith", [Reward(resources={RESOURCE_STONE: 1, RESOURCE_WOOD: 1}), Reward(resources={RESOURCE_STONE: 1, RESOURCE_GOLD: 1})]),
    ADVISOR_DUCHESS: Advisor("duchess", [Reward(receive_any_resource=2, plustwos=1)]),
    ADVISOR_CHAMPION: Advisor("champion", [Reward(resources={RESOURCE_STONE: 3})]),
    # TODO is this really -1 VP?
    ADVISOR_SMUGGLER: Advisor("smuggler", [Reward(victory_points=-1, receive_any_resource=3)]),
    ADVISOR_INVENTOR: Advisor("inventor", [Reward(resources={RESOURCE_GOLD: 1, RESOURCE_WOOD: 1, RESOURCE_STONE: 1})]),
    ADVISOR_WIZARD: Advisor("wizard", [Reward(resources={RESOURCE_GOLD: 4})]),
    ADVISOR_QUEEN: Advisor("queen", [Reward(receive_any_resource=2, view_enemy=True, victory_points=3)]),
    ADVISOR_KING: Advisor("king", [Reward(resources={RESOURCE_GOLD: 1, RESOURCE_WOOD: 1, RESOURCE_STONE: 1}, soldiers=1)]),
}

ADVISORS_STABLE = [score for score in ADVISORS if ADVISOR[score].rewards[0].soldiers > 0]

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

    def __init__(self, player_dice: DiceRoll, bonus_dice: DiceRoll, plus_two: bool=False, market_modifier: int=0, reward: Optional[Reward]=None):
        self.player_dice: DiceRoll = player_dice
        self.bonus_dice: DiceRoll = bonus_dice
        self.plus_two: bool = plus_two
        self.market_modifier: int = market_modifier
        self.reward: Optional[Reward] = reward

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

ADVISOR_INFLUENCE_PASS = AdvisorInfluence([], [])

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
        self.taken_advisors: Dict[AdvisorScore, List[str]] = {}

    def toDict(self):
        d = self.__dict__
        del d["messages"]
        d["players"] = [p.toDict() for p in self.playerList()]
        return d

    # TODO make static method
    def fromDict(self, d):
        self.messages = []
        self.players = {}
        for p in d["players"]:
            player = PlayerState("foo").fromDict(p)
            self.players[player.name] = player
        self.over = d["over"]
        self.year = d["year"]
        self.phase = d["phase"]
        self.last_phase_played = d["last_phase_played"]
        self.turn_order = d["turn_order"]
        self.taken_advisors = d["taken_advisors"]
        return self

    def copy(self) -> State:
        return copy.deepcopy(self)

    def message(self, message) -> State:
        state = self.copy()
        state.messages.append(message)
        return state

    def clearMessages(self) -> List[str]:
        messages = self.messages
        self.messages = []
        return messages

    def clearAdvisorInfluences(self) -> State:
        # TODO test
        state = self.copy()
        state.taken_advisors = {}
        return state

    def playerList(self) -> List[PlayerState]:
        return [self.players[name] for name in self.players]

    def updatePlayer(self, name: str, player: PlayerState) -> State:
        state = self.copy()
        state.players[name] = player
        messages = player.clearMessages()
        for message in messages:
            state = state.message(message)
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
        player = self.players[name]
        return self.updatePlayer(name, player.addResources(resources))

    def giveBuilding(self, name: str, building: Building, use_kings_envoy: bool):
        """
        Gives the given building to the given player.
        """
        state = self.copy()
        player_advisors: List[AdvisorScore] = []
        for score in ADVISORS:
            if score in self.taken_advisors and name in self.taken_advisors[score]:
                player_advisors.append(score)
        state = state.updatePlayer(name, state.players[name].addBuilding(building, player_advisors))
        if building != BUILD_PASS and use_kings_envoy:
            state = state.updatePlayer(name, state.players[name].useKingsEnvoy())
        return state

    def giveKingsFavorBonusDie(self, name: str):
        """
        Gives a bonus die to the given player.
        """
        player = self.players[name]
        return self.updatePlayer(name, player.addKingsFavorBonusDie())

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

    def getWinners(self) -> List[str]:
        highest_vp_players = []
        highest_vp = 0
        highest_resource_players = []
        highest_resource = 0
        highest_building_players = []
        highest_building = 0
        for p in self.playerList():
            if p.victory_points == highest_vp:
                highest_vp_players.append(p.name)
            elif p.victory_points > highest_vp:
                highest_vp = p.victory_points
                highest_vp_players = [p.name]
            if p.getTotalResources() == highest_resource:
                highest_resource_players.append(p.name)
            elif p.getTotalResources() > highest_resource:
                highest_resource = p.getTotalResources()
                highest_resource_players = [p.name]
            if len(p.buildings) == highest_building:
                highest_building_players.append(p.name)
            elif len(p.buildings) > highest_building:
                highest_building = len(p.buildings)
                highest_building_players = [p.name]
        if len(highest_vp_players) == 1:
            return highest_vp_players
        highest_resource_players = [p for p in highest_resource_players if p in highest_vp_players]
        if len(highest_resource_players) == 1:
            return highest_resource_players
        highest_building_players = [p for p in highest_building_players if p in highest_resource_players]
        return highest_building_players

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
        state = state.message("Turn order: " + str(state.turn_order))

        return state

    def influenceAdvisor(self, name: str, influence: AdvisorInfluence) -> State:
        # TODO test
        state = self.copy()
        if influence == ADVISOR_INFLUENCE_PASS:
            return state.message(name + " passes")
        score = influence.advisorScore()
        influencers = state.taken_advisors[score] if score in state.taken_advisors else []
        influencers.append(name)
        state.taken_advisors[score] = influencers
        return state.updatePlayer(name, state.players[name].influenceAdvisor(influence))

    def giveReward(self, name: str, advisor_score: AdvisorScore, reward: Reward) -> State:
        # TODO test
        state = self.copy()
        state = state.message(name + " takes reward from " + ADVISOR[advisor_score].name + " (" + str(advisor_score) + ")")
        state = state.updatePlayer(name, state.players[name].applyReward(reward))
        return state

    def choices_freeResource(self, name: str) -> List[Resource]:
        """
        Returns the list of resources available to the given player
        when picking a free resource.
        """
        return RESOURCES

    def choices__advisorInfluence(self, name: str) -> List[AdvisorInfluence]:
        """
        Returns the list of available advisor influences for the given player.
        Rewards are not included, this only represents possible dice placements.
        """
        available: List[AdvisorScore] = []
        for advisor in ADVISORS:
            if advisor not in self.taken_advisors:
                available.append(advisor)
        return self.players[name].choices__advisorInfluence(available)

    def choices__buildings(self, name: str) -> List[Building]:
        """
        Returns the list of buildings that the given player can build.
        """
        return self.players[name].choices__buildings()

##############################################
# Player state
##############################################

class PlayerState():
    """
    Tracks the state of an individual player.
    """

    def __init__(self, name: str):
        self.messages: List[str] = []
        self.name: str = name
        self.has_kings_favor_bonus_die: bool = False
        self.has_kings_envoy = False
        # TODO get rid of this.
        # Should get taken away when influencing an advisor with it.
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
        self.victory_points = 0
        self.soldiers = 0

    def toDict(self):
        d = self.__dict__
        d['dice'] = self.dice.__dict__
        return d

    # TODO make static method
    def fromDict(self, d):
        self.messages = []
        self.name = d["name"]
        self.has_kings_favor_bonus_die = d["has_kings_favor_bonus_die"]
        self.has_kings_envoy = d["has_kings_envoy"]
        self.plustwo_tokens = d["plustwo_tokens"]
        self.used_plustwo_token = d["used_plustwo_token"]
        self.used_market = d["used_market"]
        self.buildings = d["buildings"]
        self.resources = d["resources"]
        self.victory_points = d["victory_points"]
        self.soldiers = d["soldiers"]
        self.dice = ProductiveSeasonRoll(
            player_dice=d["dice"]["player_dice"],
            bonus_dice=d["dice"]["bonus_dice"],
        )
        return self

    def copy(self) -> PlayerState:
        return copy.deepcopy(self)

    def message(self, message: str) -> PlayerState:
        state = self.copy()
        state.messages.append(self.name + " " + message)
        return state

    def clearMessages(self) -> List[str]:
        messages = self.messages
        self.messages = []
        return messages

    def addVictoryPoints(self, victory_points: int) -> PlayerState:
        """
        Adds the given victory points to the player.
        """
        state = self.copy()
        state.victory_points += victory_points
        if victory_points >= 0:
            state = state.message("gains +" + str(victory_points) + " victory points")
        else:
            state = state.message("loses -" + str(victory_points) + " victory points")
        return state

    def addSoldiers(self, soldiers: int) -> PlayerState:
        """
        Adds the given number of soliders to the player.
        """
        state = self.copy()
        state.soldiers += soldiers
        if soldiers >= 0:
            state = state.message("gains +" + str(soldiers) + " soldiers")
        else:
            state = state.message("loses -" + str(soldiers) + " soldiers")
        return state

    def addResources(self, resources: ResourceInventory) -> PlayerState:
        """
        Adds the given resources to this player's resources.
        """
        state = self.copy()
        for resource in resources:
            amount = resources[resource]
            if amount > 0:
                state = state.message("gains +" + str(amount) + " " + resource)
            else:
                state = state.message("loses " + str(amount) + " " + resource)
            state.resources[resource] += resources[resource]
        return state

    def addBuilding(self, building: Building, player_advisors: List[AdvisorScore]) -> PlayerState:
        """
        Adds the given building to this player's buildings.
        Subtract the cost of the building from the player's resources.
        Give the player victory points for the building.
        Special rule for buying Stable.
        """
        if building in self.buildings:
            raise Exception("Adding an already-owned building")
        state = self.copy()
        if building == BUILD_PASS:
            return state.message("passes")
        state = state.message("gains building " + building)
        state.buildings.append(building)
        state = state.addResources(BUILDING_COST[building])
        state = state.addVictoryPoints(BUILDING_VP[building])
        if building == BUILDING_STABLE:
            for advisor in ADVISORS_STABLE:
                if advisor in player_advisors:
                    state = state.message("Stable gives +1 solidier when influencing an advisor giving you at least 1 soldier")
                    state = state.addSoldiers(1)
                    break
            pass
        return state

    def addKingsFavorBonusDie(self) -> PlayerState:
        """
        Adds a bonus die to this player.
        """
        state = self.copy()
        state = state.message("gains King's Favor bonus die")
        state.has_kings_favor_bonus_die = True
        return state

    def influenceAdvisor(self, influence: AdvisorInfluence) -> PlayerState:
        # TODO test
        state = self.copy()
        score = influence.advisorScore()
        state = state.message("influences " + ADVISOR[score].name + " (" + str(score) + ")")
        state = state.spendDice(influence)
        return state

    def spendDice(self, influence: AdvisorInfluence) -> PlayerState:
        state = self.copy()
        state = state.message("spends player dice: " + str(influence.player_dice))
        state.dice.player_dice = util.list_minus(state.dice.player_dice, influence.player_dice)
        if len(influence.bonus_dice) > 0:
            state = state.message("spends bonus dice: " + str(influence.bonus_dice))
            state.dice.bonus_dice = util.list_minus(state.dice.bonus_dice, influence.bonus_dice)
        if influence.plus_two:
            state = state.message("spends a plustwo")
            state.plustwo_tokens -= 1
        if influence.market_modifier == -1:
            state = state.message("uses market -1")
        if influence.market_modifier == 1:
            state = state.message("uses market +1")
        return state

    def applyReward(self, reward: Reward) -> PlayerState:
        """
        Applies the given reward to this player.
        """
        state = self.copy()
        if reward.victory_points != 0:
            state = state.addVictoryPoints(reward.victory_points)
        state = state.addResources(reward.resources)
        if reward.soldiers != 0:
            state = state.addSoldiers(reward.soldiers)
        if reward.plustwos < 0:
            state = state.message("loses " + str(reward.plustwos) + " plustwo tokens")
        elif reward.plustwos > 0:
            state = state.message("gains +" + str(reward.plustwos) + " plustwo tokens")
        state.plustwo_tokens += reward.plustwos
        # TODO view enemy
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

    def getTotalResources(self) -> int:
        return self.resources[RESOURCE_GOLD] + self.resources[RESOURCE_WOOD] + self.resources[RESOURCE_STONE]

    def roll(self, roll: ProductiveSeasonRoll) -> PlayerState:
        """
        Set's this player's roll to the given roll.
        Resets bonus die.
        """
        state = self.copy()
        state.dice = copy.deepcopy(roll)
        state.has_kings_favor_bonus_die = False
        message = "rolled player dice: " + ", ".join([str(die) for die in roll.player_dice])
        if len(roll.bonus_dice) > 0:
            message += ", bonus dice: " + ", ".join([str(die) for die in roll.bonus_dice])
        state = state.message(message)
        return state

    def useKingsEnvoy(self):
        if not self.has_kings_envoy:
            raise Exception("Cannot use King's Envoy")
        state = self.copy()
        state.has_kings_envoy = False
        return state.message("loses King's Envoy")

    def choices__advisorInfluence(self, available: List[AdvisorScore]) -> List[AdvisorInfluence]:
        """
        Returns the possible advisor influences this player could make.
        Does not compute all possible rewards.
        """
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

        # Determine valid influences. Start with only the "Pass" influence.
        possible_influences: List[AdvisorInfluence] = [ADVISOR_INFLUENCE_PASS]
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

    def choices__buildings(self) -> List[Building]:
        """
        Returns the list of buildings this player can buy.
        """
        buildings: List[Building] = []
        for row in PROVINCE_SHEET:
            for building in row:
                if building in self.buildings:
                    continue
                after_buying = self.addResources(BUILDING_COST[building])
                if after_buying.resources[RESOURCE_GOLD] < 0:
                    break
                if after_buying.resources[RESOURCE_WOOD] < 0:
                    break
                if after_buying.resources[RESOURCE_STONE] < 0:
                    break
                buildings.append(building)
                break
        buildings.append(BUILD_PASS)
        return buildings
