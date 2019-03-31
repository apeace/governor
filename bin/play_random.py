import game
import engine

if __name__ == "__main__":
    logger = engine.StdoutLogger()
    rand = engine.RandomCliEngine(logger)
    state = game.State()
    g = game.Game(rand, state)
    g.play()