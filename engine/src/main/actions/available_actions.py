from main.utils.variable import State, Selected, Phase, Bottom
from main.board.board_query import BoardQuery
from main.actions.contex import ActionContextContext
from main.actions.available_action_result import AvailableActionResult
# from 

class AvailableActions():
    BOTTOM_KEY = "bottom"
    HAND_KEY = "hand"
    BOARD_KEY = "board"
    def __init__(self, ctx):
        self.ctx = ctx
        self.state = ctx.state
        self.rules = ctx.rules
        self.hand = {
            fraction : [False for _ in range(player.hand.size())]
            for fraction, player in self.state.players.items()
        }
        self.board = {
            hex : False
            for hex in self.state.board.ALL_HEXES
        }
        self.bottoms = {
            bottom : False
            for bottom in Bottom
        }
        self.state_handlers = {
            # State.SELECTED_HAND : self.hand_available_actions,
            State.NO_SELECTION : self.default_available_actions,
            # State.MOVING : InstantToken(Token.Type.Instant.MOVE).available_actions,
            State.ROTATE : self.rotate_available_actions,
            # State.PLACING : self.placing_available_actions,
            # State.SELECTED_PUSHer : InstantToken(Token.Type.Instant.PUSH).available_actions,
        }

    def update_hand_availability(self, value):
        for i in range(self.state.current_player.hand.size()):
            self.hand[self.state.current_fraction][i] = value
    
    def update_board_availability(self, positions):
        for (x, y) in self.state.board.ALL_HEXES:
            self.board[x][y] = ((x, y) in positions)
        
    def default_available_actions(self):
        if(self.ctx.rules.can_end_turn()):
            self.enable(Bottom.END_TURN)
        
        self.update_hand_availability(True)

    def rotate_available_actions(self):
        self.update_board_availability([self.state.seleced[Selected.POS]])

    def enable(self, bottom):
        if bottom in Bottom:
            self.bottoms[bottom] = True

    def placing_available_actions(self):
        query = BoardQuery([self.rules.is_empty()])
        self.update_board_availability(query.apply())
        
        self.enable(Bottom.CANCEL)
        if(self.state.phase != Phase.HQ_PLACEMENT):
            self.enable(Bottom.DISCARD)
            
    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def update_available_actions(self, actions : AvailableActionResult):
        self.update_board_availability(actions.positions)
        if(actions.can_cancel):
            self.enable(Bottom.CANCEL)

        if(actions.can_discard):
            self.enable(Bottom.DISCARD)

        if(actions.can_use):
            self.enable(Bottom.USE)

    def user_available_actions(self, ctx):
        token = self.ctx.player.hand.get_active_token()

        if token:
            actions = token.get_available_actions(self.ctx)
            self.update_available_actions(actions)

        function = self.state_handlers.get(ctx.state, None)
        if not (function is None):
            function(ctx)
