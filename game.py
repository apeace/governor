from typing import Dict

import engine
import kingsburg

class Game():
    """
    Plays through a game, using inputs from an Engine.
    """

    def __init__(self, engine: engine.Engine, state: kingsburg.State):
        self.engine = engine
        self.state: kingsburg.State = state

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
            self.engine.log(self.state, self.state.messages)
            self.state.clearMessages()
            return False

        phase = kingsburg.PHASES[self.state.phase]
        if phase == kingsburg.PHASE_KINGS_FAVOR:
            self.kingsFavor()
        elif phase in kingsburg.PRODUCTIVE_SEASONS:
            self.productiveSeason(phase)

        self.engine.log(self.state, self.state.messages)
        self.state.clearMessages()

        return False

    def kingsFavor(self):
        """
        Plays the King's Favor phase.
        """
        result = self.state.kingsFavor()
        if result == kingsburg.KINGS_FAVOR_TIE:
            messages = self.state.messages
            self.state.clearMessages()
            messages.append("Kings Favor is a tie")
            self.engine.log(self.state, messages)
            for player in self.state.players:
                resource = self.engine.pickFreeResource(self.state, player)
                self.state = self.state.takeFreeResource(player, resource)
        else:
            self.state = result
        self.state = self.state.phaseComplete(kingsburg.PHASE_KINGS_FAVOR)

    def productiveSeason(self, phase: kingsburg.Phase):
        """
        Productive season.
        """

        # TODO Merchant's guild rewards gold
        # TODO 2-player rule: block advisors

        # Each player rolls dice.
        rolls: Dict[str, kingsburg.ProductiveSeasonRoll] = {}
        for name in self.state.players:
            rolls[name] = self.engine.rollDice(self.state, name)
        self.state = self.state.productiveSeasonRolls(rolls)
        self.engine.log(self.state, self.state.messages)
        self.state.clearMessages()

        # TODO Statue & Chapel allow re-rolls

        # Players take turns influencing advisors
        num_passes = 0
        while num_passes < len(self.state.turn_order):
            num_passes = 0
            for name in self.state.turn_order:
                influence = self.engine.influenceAdvisor(self.state, name)
                if influence == kingsburg.ADVISOR_INFLUENCE_PASS:
                    num_passes += 1
                self.state = self.state.influenceAdvisor(name, influence)
            self.engine.log(self.state, self.state.messages)
            self.state.clearMessages()

        self.engine.log(self.state, "Productive season done")

        # TODO construct buildings
        # TODO king's envoy allows to build an additional building

        # TODO at end of summer, Inn rewards token thingie
        # TODO Town hall allows trading token for VP
        # TODO Embassy grants VP

        self.state = self.state.phaseComplete(phase)
