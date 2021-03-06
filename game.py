from typing import Dict, Set, Optional

import engine
import kingsburg

# TODO right now a player can influence the same advisor twice with King's Envoy
# available_advisors stuff should take that into account

# TODO king's envoy should be taken away if influencing an advisor with it

# It is currently able to spend two plustwos in a row

class Game():
    """
    Plays through a game, using inputs from an Engine.
    """

    def __init__(self, engine: engine.Engine, state: kingsburg.State):
        # TODO it appears to be impossible to specify the type of self.engine
        # TODO also, self.state does not appear to be type-checked
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
        Initial turn order is assumed to be the order the players were entered.
        """
        self.state = self.state.setPlayers(self.engine.setupPlayers())
        self.engine.start(self.state)

    def tick(self) -> bool:
        """
        Advance to the next step of the game.
        Returns True if the game is over.
        """
        if self.state.last_phase_played == self.state.phase:
            self.state = self.state.nextPhase()
            if self.state.over:
                return True
            self.engine.log(self.state, self.state.clearMessages())
            return False

        phase = kingsburg.PHASES[self.state.phase]
        if phase == kingsburg.PHASE_KINGS_FAVOR:
            self.kingsFavor()
        elif phase in kingsburg.PRODUCTIVE_SEASONS:
            self.productiveSeason(phase)
        elif phase == kingsburg.PHASE_KINGS_REWARD:
            # TODO
            self.state = self.state.phaseComplete(kingsburg.PHASE_KINGS_REWARD)
        elif phase == kingsburg.PHASE_KINGS_ENVOY:
            # TODO
            self.state = self.state.phaseComplete(kingsburg.PHASE_KINGS_ENVOY)
        elif phase == kingsburg.PHASE_RECRUIT_SOLDIERS:
            # TODO
            self.state = self.state.phaseComplete(kingsburg.PHASE_RECRUIT_SOLDIERS)
        elif phase == kingsburg.PHASE_WINTER:
            # TODO
            self.state = self.state.phaseComplete(kingsburg.PHASE_WINTER)

        return False

    def kingsFavor(self):
        """
        Plays the King's Favor phase.
        """
        result = self.state.kingsFavor()
        if result == kingsburg.KINGS_FAVOR_TIE:
            messages = self.state.clearMessages()
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

        # Each player rolls dice and turn order is set.
        rolls: Dict[str, kingsburg.ProductiveSeasonRoll] = {}
        for name in self.state.players:
            rolls[name] = self.engine.rollDice(self.state, name)
        self.state = self.state.productiveSeasonRolls(rolls)
        self.engine.log(self.state, self.state.clearMessages())

        # TODO Statue & Chapel allow re-rolls

        # Players take turns influencing advisors until each player passes.
        passes: Set[str] = set()
        while len(passes) < len(self.state.turn_order):
            for name in self.state.turn_order:
                if name in passes:
                    continue
                influence = self.engine.chooseAdvisor(self.state, name)
                if influence == kingsburg.ADVISOR_INFLUENCE_PASS:
                    passes.add(name)
                self.state = self.state.influenceAdvisor(name, influence)
            self.engine.log(self.state, self.state.clearMessages())

        # Players take their rewards in order of advisor score.
        for advisorScore in kingsburg.ADVISORS:
            if advisorScore in self.state.taken_advisors:
                for name in self.state.taken_advisors[advisorScore]:
                    # TODO refactor possible_rewards into engine/player
                    # In fact make engine list the possible stuff for every move
                    # That way it can be fed into both CliPlayer and RandomPlayer
                    possible_rewards = kingsburg.ADVISOR[advisorScore].choices__rewards(self.state.players[name].resources)
                    reward: Optional[kingsburg.Reward] = None
                    if len(possible_rewards) == 1:
                        reward = possible_rewards[0]
                    else:
                        self.engine.log(self.state, self.state.clearMessages())
                        reward = self.engine.chooseReward(self.state, name, advisorScore, possible_rewards)
                    if reward is not None:
                        # TODO view enemies
                        self.state = self.state.giveReward(name, advisorScore, reward)
        self.engine.log(self.state, self.state.clearMessages())

        # In turn order, players construct buildings.
        for name in self.state.turn_order:
            building = self.engine.chooseBuilding(self.state, name, use_kings_envoy=False)
            self.state = self.state.giveBuilding(name, building, use_kings_envoy=False)
            if building != kingsburg.BUILD_PASS and self.state.players[name].has_kings_envoy:
                building = self.engine.chooseBuilding(self.state, name, use_kings_envoy=True)
                self.state = self.state.giveBuilding(name, building, use_kings_envoy=True)
        self.engine.log(self.state, self.state.clearMessages())

        self.engine.log(self.state, "Productive season done")
        self.state = self.state.clearAdvisorInfluences()

        # TODO at end of summer, Inn rewards token thingie
        # TODO Town hall allows trading token for VP
        # TODO Embassy grants VP

        self.state = self.state.phaseComplete(phase)
