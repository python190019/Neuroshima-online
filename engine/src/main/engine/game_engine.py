from random import shuffle
from main.state.contex import ActionContext
from main.utils.variable import Turn, Phase

class GameEngine:

    def __init__(
        self,
        rules,
        passive_system,
        resolver,
        validator,
        actions,
        available_actions
    ):
        self.validator          = validator
        
        self.actions            = actions
        self.available_actions  = available_actions

        self.resolver = resolver
        
        self.passive_system     = passive_system

    def handle_action(self, ctx : ActionContext, action):
        if not self.validator.is_valid_action(ctx, action):
            raise ValueError("invalid action")
        # if not self.rules.can_execute_action(ctx, action):
        #     return False

        result = self.actions.execute_action(ctx, action)
        self.resolver.resolve(ctx, result)

        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions(ctx)


    def _setup_players(self, ctx : ActionContext):
        shuffle(ctx.state.fractions)
        ctx.fraction = ctx.state.fractions[0]
        for fraction in ctx.state.fractions:
            ctx.state.add_player(fraction)

    def _setup_turn_order(self, ctx : ActionContext):
        for fraction in ctx.state.fractions:
            ctx.state.next_turns.append(
                {Turn.FRACTION : fraction, 
                 Turn.TYPE : Turn.Type.HQ_PLACEMENT}
            )

    def _set_initial_phase(self, ctx : ActionContext):
        ctx.state.phase = Phase.GAME

    def start_game(self, ctx : ActionContext):
        self._setup_players(ctx)
        self._setup_turn_order(ctx)
        self._set_initial_phase(ctx)
        self.flow_engine.start_turn(ctx)
        
        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions()
