import game

def test_next_year():
    state = game.GameState()
    newState = state.nextYear()
    assert state.year == 1
    assert newState.year == 2
