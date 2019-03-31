import engine
import kingsburg

class Game():
    """
    Plays through a game, using inputs from an Engine.
    """
    def __init__(self, engine: engine.Engine, state: kingsburg.State):
        self.engine = engine
        self.state = state

    def play(self):
        """
        Play through an entire game from start to finish.
        """
        self.setup()
        while True:
            over = self.tick()
            if over:
                break
        self.engine.over(self.state)

    def setup(self):
        """
        Setup game state for the start of the game.
        """
        self.state = self.state.setPlayers(self.engine.getPlayers())
        self.engine.start(self.state)

    def tick(self):
        """
        Advance to the next step of the game.
        """
        if self.state.last_phase_played == self.state.phase:
            self.state = self.state.nextPhase()
            if self.state.over:
                return True
            self.engine.tick(self.state, "Next phase")
            return False

        if kingsburg.PHASES[self.state.phase] == kingsburg.PHASE_KINGS_FAVOR:
            self.kingsFavor()

        messages = self.state.messages
        self.state = self.state.clearMessages()
        self.engine.tick(self.state, messages)

        return False

    def kingsFavor(self):
        """
        Plays the King's Favor phase.
        """
        result = self.state.kingsFavor()
        if result == kingsburg.KINGS_FAVOR_TIE:
            messages = self.state.messages
            self.state = self.state.clearMessages()
            messages.append("Kings Favor is a tie")
            self.engine.tick(self.state, messages)
            for player in self.state.players:
                resource = self.engine.pickFreeResource(self.state, player)
                self.state = self.state.takeFreeResource(player, resource)
        else:
            self.state = result
        self.state = self.state.phaseComplete(kingsburg.PHASE_KINGS_FAVOR)
