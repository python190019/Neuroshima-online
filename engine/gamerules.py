from variable import *

class GameRules():
    def __init__(self, state):
        self.state = state
        self.player = state.current_player

    def can_end_turn(self):
         if(self.player.hand.is_full()):
            return False