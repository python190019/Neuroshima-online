from variable import *


class Validate():
    def __init__(self):
        self.validate_handlers = {
            Action.Type.BOARD : self.validate_board_action,
            Action.Type.HAND : self.validate_hand_action,
            Action.Type.BOTTOM : self.validate_bottom_action,
            Action.Type.ROTATE : self.validate_rotate_action
        }

    def validate_board_action(self, state, action):
        pos = action[Action.Key.POS]
        if(not isinstance(pos, tuple)):
            return False
        if(len(pos) != 2):
            return False
        x, y = pos
        if(not isinstance(x, int) or not isinstance(y, int)):
            return False
        if(not state.board.on_board(x, y)):
            return False
        return True
        # return state.available_actions[UI.BOARD][x][y]

    def validate_hand_action(self, state, action):
        slot = action.get(Action.Key.SLOT, None)
        if(not isinstance(slot, int)):
            return False
        
        if(state.current_player.hand.get_token(slot) is None):
            return False
        return True
        # return game.available_actions[UI.HAND][game.current_frakcja][slot]

    def validate_bottom_action(self, state, action):
        name = action.get(Action.Key.BOTTOM, None)
        return name in Bottom
        # return game.available_actions[UI.BOTTOM][name]

    def validate_rotate_action(self, state, action):
        rotation = action.get(Action.Key.ROTATION, None)
        return isinstance(rotation, int)

    def is_valid_action(self, state, action):
        if (action is None):
            return True
        type = action.get(Action.Key.TYPE, None)
        function = self.validate_handlers.get(type, None)
        if(function is None):
            return False
        return function(state, action)
