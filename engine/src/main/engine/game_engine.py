
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
        self.flow_engine     = flow_engine
        
        self.passive_system     = passive_system


    def handle_action(self, ctx, action):
        if not self.validator.is_valid_action(ctx, action):
            return False
        # if not self.rules.can_execute_action(ctx, action):
        #     return False

        result = self.actions.execute_action(ctx, action)
        
        self.state_engine.apply(ctx, result.interaction_state_changes)
        self.effect_engine.apply(ctx, result.effects)
        
        flow_result = self.flow_engine.apply(ctx, result.flow_events)
        self.state_engine.apply(ctx, flow_result.interaction_state_changes)

        self.passive_system.compute(ctx)
        return self.available_actions.get_available_actions()