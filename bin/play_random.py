import kingsburg
import engine
import logger
import game

if __name__ == "__main__":
    l = logger.StdoutLogger()
    rand = engine.RandomCliEngine(l)
    state = kingsburg.State()
    g = game.Game(rand, state)
    g.play()