from main.utils.variable import State
from main.state.selection import Selection

class StateChange:
    pass

class SetInteractionState(StateChange):
    def __init__(self, new_state=None):
        super().__init__()
        self.new_state = new_state or State.NO_SELECTION

    def apply(self, ctx):
        ctx.state.interaction_state = self.new_state
    
class SetSelected(StateChange):
    def __init__(self, selected):
        super().__init__()
        self.selected = selected

    def apply(self, ctx):
        ctx.selectdc = self.selected

class ResetInteraction(StateChange):
    def __init__(self):
        super().__init__()
        pass

    def apply(self, ctx):
        SetSelected(Selection()).apply(ctx)
        SetInteractionState().apply(ctx)