
class ActionContext():
    def __init__(self, state):
        self.state = state.state

    #shortcuts
    @property
    def selected(self):
        return self.state.selected
    
    @property
    def fraction(self):
        return self.state.current_fraction
    
    @property
    def board(self):
        return self.state.board

    def player(self):
        return self.state.current_player