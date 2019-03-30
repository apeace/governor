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

class GameState(object):

    def __init__(self):
        self.over = False
        self.year = 1
        self.phase = 0

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
