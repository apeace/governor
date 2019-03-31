import game
import engine
import logger

if __name__ == "__main__":
    l = logger.StdoutLogger()
    rand = engine.RandomCliEngine(l)
    state = game.State()
    g = game.Game(rand, state)
    g.play()