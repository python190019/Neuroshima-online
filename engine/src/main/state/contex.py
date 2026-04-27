from main.state.game_state import GameState

class ActionContext():
    def __init__(self, state : GameState):
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

    @property
    def player(self):
        return self.state.current_player
    
    @property
    def active_token(self):
        token = self.player.hand.get_active_token()
        if token:
            return token
        else:
            return self.board.get_tile(self.selected.unit_position)

    @property
    def ui_state(self):
        return self.state.interaction_state