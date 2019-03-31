import game
import engine

if __name__ == "__main__":
    logger = engine.StdoutLogger()
    cli = engine.CliEngine(logger)
    state = game.State()
    g = game.Game(cli, state)
    g.play()
