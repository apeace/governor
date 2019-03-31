import kingsburg
import engine
import logger
import game

def test_random_game():
    l = logger.SilentLogger()
    rand = engine.RandomEngine(l)
    state = kingsburg.State()
    g = game.Game(rand, state)

    ## TODO actually test some states
    for i in range(0, 1000):
        g.tick()

