
class ActionContext():

    def __init__(self, state, actions, rules):
        self.state = state.state
        
        #shortcuts
        self.selected = state.selected
        self.fraction = state.current_fraction
        self.board = state.board
        self.player = state.current_player
        
        self.actions = actions
        self.rules = rules

