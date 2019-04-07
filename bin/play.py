import kingsburg
import engine
import logger
import game

if __name__ == "__main__":
    cli = engine.CliEngine(logger.StdoutLogger())
    g = game.Game(cli, kingsburg.State())
    g.play()
