import game

def test_next_year():
    state = game.GameState()
    newState = state.nextYear()
    assert state.year == 1
    assert newState.year == 2

    state.year = game.MAX_YEAR
    newState = state.nextYear()
    assert newState.over

def test_next_phase():
    state = game.GameState()
    newState = state.nextPhase()
    assert newState.year == 1
    assert newState.phase == 1

    state.phase = game.MAX_PHASE
    newState = state.nextPhase()
    assert newState.year == 2
    assert newState.phase == 0

    state.year = game.MAX_YEAR
    state.phase = game.MAX_PHASE
    newState = state.nextPhase()
    assert newState.year == game.MAX_YEAR
    assert newState.phase == game.MAX_PHASE
    assert newState.over
