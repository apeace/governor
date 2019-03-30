import engine

if __name__ == "__main__":
    logger = engine.Logger()
    cli = engine.CliEngine(logger)
    cli.play()