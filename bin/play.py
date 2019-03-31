import game
import engine
import logger

if __name__ == "__main__":
    l = logger.StdoutLogger()
    cli = engine.CliEngine(l)
    state = game.State()
    g = game.Game(cli, state)
    g.play()
