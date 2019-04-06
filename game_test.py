import kingsburg
import engine
import logger
import game

def test_random_game():
    l = logger.SilentLogger()
    rand = engine.RandomEngine(l)
    state = kingsburg.State()
    g = game.Game(rand, state)
    g.setup()

    ## TODO actually test some states
    for i in range(0, 5000):
        if g.tick():
            break

    assert g.state.year == kingsburg.MAX_YEAR
    assert g.state.phase == kingsburg.MAX_PHASE
    assert g.state.over
