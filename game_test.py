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

    num_ticks = 0
    ## TODO actually test some states
    for i in range(0, 5000):
        if g.tick():
            return
        num_ticks += 1

    assert num_ticks > 20
    assert kingsburg.PHASES[g.state.phase] == kingsburg.PHASE_KINGS_REWARD
