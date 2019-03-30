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
        self.setup()
        while True:
            msg = []

            self.state = self.state.nextPhase()
            msg.append("Next phase")

            if self.state.over:
                break

            self.engine.tick(self.state, message=msg)

        self.engine.over(self.state)

    def setup(self):
        if len(self.state.players) == 0:
            self.state.setPlayers(self.engine.getPlayers())
        self.engine.start(self.state)

class State():
    """
    Tracks state of a game and implements state transitions.
    """
    def __init__(self):
        self.players = []
        self.over = False
        self.year = 1
        self.phase = 0

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