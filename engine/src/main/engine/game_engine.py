from random import shuffle
from main.state.contex import ActionContext
from main.utils.variable import *


class GameEngine:

    def __init__(
        self,
        rules,
        effect_engine,
        passive_system,
        state_changes_engine,
        flow_engine,
        validator,
        actions,
        available_actions
    ):
        self.rules              = rules
        self.validator          = validator
        
        self.actions            = actions
        self.available_actions  = available_actions

        self.effect_engine      = effect_engine
        self.state_engine       = state_changes_engine
        self.flow_engine        = flow_engine
        
        self.passive_system     = passive_system

    def handle_action(self, ctx : ActionContext, action):
        if not self.validator.is_valid_action(ctx, action):
            return False
        # if not self.rules.can_execute_action(ctx, action):
        #     return False

        result = self.actions.execute_action(ctx, action)
        
        self.state_engine.apply(ctx, result.interaction_state_changes)
        self.effect_engine.apply(ctx, result.effects)
        
        ctx.state.flow_queue.extend(result.flow_events)
        flow_result = self.flow_engine.apply(ctx)
        self.state_engine.apply(ctx, flow_result.interaction_state_changes)

        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions()
    

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
