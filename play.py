import game
import engine

if __name__ == "__main__":
    logger = engine.Logger()
    cli = engine.CliEngine(logger)
    state = game.State()
    game = game.Game(cli, state)
    game.play()
