import copy

import util

MAX_YEAR = 5

RESOURCE_GOLD = "gold"
RESOURCE_STONE = "stone"
RESOURCE_WOOD = "wood"

RESOURCES = [RESOURCE_GOLD, RESOURCE_STONE, RESOURCE_WOOD]

BUILDING_STATUE = "statue"
BUILDING_CHAPEL = "chapel"
BUILDING_CHURCH = "church"
BUILDING_CATHEDRAL = "cathedral"
BUILDING_INN = "inn"
BUILDING_MARKET = "market"
BUILDING_FARMS = "farms"
BUILDING_MERCHANTS_GUILD = "merchants-guild"
BUILDING_GUARD_TOWER = "guard-tower"
BUILDING_BLACKSMITH = "blacksmith"
BUILDING_BARRACKS = "barracks"
BUILDING_WIZARDS_GUILD = "wizards-guild"
BUILDING_PALISADE = "palisade"
BUILDING_STABLE = "stable"
BUILDING_STONE_WALL = "stone-wall"
BUILDING_FORTRESS = "fortress"
BUILDING_BARRICADE = "barricade"
BUILDING_CRANE = "crane"
BUILDING_TOWN_HALL = "town-hall"
BUILDING_EMBASSY = "embassy"

PROVINCE_SHEET = [
    [BUILDING_STATUE, BUILDING_CHAPEL, BUILDING_CHURCH, BUILDING_CATHEDRAL],
    [BUILDING_INN, BUILDING_MARKET, BUILDING_FARMS, BUILDING_MERCHANTS_GUILD],
    [BUILDING_GUARD_TOWER, BUILDING_BLACKSMITH, BUILDING_BARRACKS, BUILDING_WIZARDS_GUILD],
    [BUILDING_PALISADE, BUILDING_STABLE, BUILDING_STONE_WALL, BUILDING_FORTRESS],
    [BUILDING_BARRICADE, BUILDING_CRANE, BUILDING_TOWN_HALL, BUILDING_EMBASSY],
]

PHASE_KINGS_FAVOR = "kings-favor"
PHASE_SPRING = "spring"
PHASE_KINGS_REWARD = "kings-reward"
PHASE_SUMMER = "summer"
PHASE_KINGS_ENVOY = "kings-envoy"
PHASE_FALL = "fall"
PHASE_RECRUIT_SOLDIERS = "recruit-soldiers"
PHASE_WINTER = "winter"

PHASES = [
    PHASE_KINGS_FAVOR, PHASE_SPRING, PHASE_KINGS_REWARD, PHASE_SUMMER,
    PHASE_KINGS_ENVOY, PHASE_FALL, PHASE_RECRUIT_SOLDIERS, PHASE_WINTER
]

MAX_PHASE = len(PHASES) - 1

PRODUCTIVE_SEASONS = [
    PHASE_SPRING, PHASE_SUMMER, PHASE_FALL
]

KINGS_FAVOR_TIE = "tie"

class Game():
    """
    Plays through a game, using inputs from an Engine.
    """
    def __init__(self, engine, state):
        self.engine = engine
        self.state = state

    def play(self):
        """
        Play through an entire game from start to finish.
        """
        self.setup()
        while True:
            over = self.tick()
            if over:
                break
        self.engine.over(self.state)

    def setup(self):
        """
        Setup game state for the start of the game.
        """
        self.state = self.state.setPlayers(self.engine.getPlayers())
        self.engine.start(self.state)

    def tick(self):
        """
        Advance to the next tick of the game.
        """
        if self.state.last_phase_played == self.state.phase:
            self.state = self.state.nextPhase()
            if self.state.over:
                return True
            self.engine.tick(self.state, "Next phase")
            return False

        if PHASES[self.state.phase] == PHASE_KINGS_FAVOR:
            self.kingsFavor()

        return False

    def kingsFavor(self):
        """
        Plays the King's Favor phase.
        """
        result = self.state.kingsFavor()
        if result == KINGS_FAVOR_TIE:
            for player in self.state.players:
                resource = self.engine.pickFreeResource(player)
                self.state = self.state.takeFreeResource(player, resource)
        else:
            self.state = result

class State():
    """
    Tracks state of a game and implements state transitions.
    """
    def __init__(self):
        self.players = {}
        self.over = False
        self.year = 1
        self.phase = 0
        self.last_phase_played = -1

    def copy(self):
        return copy.deepcopy(self)

    def playerList(self):
        return [self.players[name] for name in self.players]

    def updatePlayer(self, name, player):
        state = self.copy()
        state.players[name] = player
        return state

    def setPlayers(self, playerNames):
        state = self.copy()
        for name in playerNames:
            player = PlayerState(name)
            state.players[name] = player
        return state

    def nextYear(self):
        state = self.copy()
        if state.year == MAX_YEAR:
            state.over = True
        else:
            state.year += 1
        return state

    def nextPhase(self):
        state = self.copy()
        if state.phase == MAX_PHASE:
            state = state.nextYear()
            if not state.over:
                state.phase = 0
            return state
        else:
            state.phase += 1
            return state

    def phaseComplete(self, phase):
        if phase != PHASES[self.phase]:
            raise Exception("Completed the wrong phase")
        state = self.copy()
        state.last_phase_played = self.phase
        return state

    def kingsFavor(self):
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
        print(fewest_buildings)
        if fewest_buildings is not None:
            return self.giveBonusDie(fewest_buildings)

        fewest_resources = util.lowest(resource_count)
        if fewest_resources is not None:
            return self.giveBonusDie(fewest_resources)

        return KINGS_FAVOR_TIE

    def takeFreeResource(self, name, resource):
        """
        Gives one of the given resource to the given player.
        """
        return self.giveResources(name, {resource: 1})

    def giveResources(self, name, resources):
        """
        Gives the given resources to the given player.
        """
        player = self.players[name]
        return self.updatePlayer(name, player.addResources(resources))

    def giveBuilding(self, name, building):
        """
        Gives the given building to the given player.
        """
        player = self.players[name]
        return self.updatePlayer(name, player.addBuilding(building))

    def giveBonusDie(self, name):
        """
        Gives a bonus die to the given player.
        """
        player = self.players[name]
        return self.updatePlayer(name, player.addBonusDie())

class PlayerState():
    """
    Tracks the state of an individual player.
    """
    def __init__(self, name):
        self.name = name
        self.bonusDie = False
        self.buildings = []
        self.resources = {
            RESOURCE_WOOD: 0,
            RESOURCE_GOLD: 0,
            RESOURCE_STONE: 0
        }

    def copy(self):
        return copy.deepcopy(self)

    def addResources(self, resources):
        """
        Adds the given resources to this player's resources.
        """
        state = self.copy()
        for resource in resources:
            state.resources[resource] += resources[resource]
        return state

    def addBuilding(self, building):
        """
        Adds the given building to this player's buildings.
        """
        if building in self.buildings:
            raise Exception("Adding an already-owned building")
        state = self.copy()
        state.buildings.append(building)
        return state

    def addBonusDie(self):
        """
        Adds a bonus die to this player.
        """
        state = self.copy()
        state.bonusDie = True
        return state
