
class ActionResult():
    def __init__(self, 
        effects=None, 
        interaction_state_changes=None, 
        flow_effects=None
    ):
        self.effects = effects or []
        self.interaction_state_changes = interaction_state_changes or []
        self.flow_effects = flow_effects or []