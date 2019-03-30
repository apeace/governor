import copy

MAX_YEAR = 5

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
        self.state.setPlayers(self.engine.getPlayers())
        self.engine.start(self.state)

    def tick(self):
        """
        Advance to the next tick of the game.
        """
        msg = []

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
        Phase 1: The King's Favor
        The player with the fewest buildings gets a bonus die.
        If there is a tie for fewest buildings, the player with
        the fewest resources gets a bonus die. If there is a tie
        for fewest resources, each player chooses one free resource.
        """
        input("Kings favor stuff")
        self.state = self.state.phaseComplete(PHASE_KINGS_FAVOR)


class State():
    """
    Tracks state of a game and implements state transitions.
    """
    def __init__(self):
        self.players = []
        self.over = False
        self.year = 1
        self.phase = 0
        self.last_phase_played = -1

    def setPlayers(self, playerNames):
        self.players = [PlayerState(name) for name in playerNames]

    def nextYear(self):
        state = copy.deepcopy(self)
        if state.year == MAX_YEAR:
            state.over = True
        else:
            state.year += 1
        return state

    def nextPhase(self):
        state = copy.deepcopy(self)
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
        state = copy.deepcopy(self)
        state.last_phase_played = self.phase
        return state

class PlayerState():
    """
    Tracks the state of an individual player.
    """
    def __init__(self, name):
        self.name = name
        self.bonusDie = False
        self.buildings = []
        self.gold = 0
        self.stone = 0
        self.wood = 0