import kingsburg
import engine
import logger
import game

if __name__ == "__main__":
    l = logger.StdoutLogger()
    cli = engine.CliEngine(l)
    state = kingsburg.State()
    g = game.Game(cli, state)
    g.play()
