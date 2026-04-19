from variable import Selected, Phase
from boardfilter import BoardFilter
from contex import ActionContextContext
# from 

class Bottom:
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"


class AvailableActions():
    BOTTOM_KEY = "bottom"
    HAND_KEY = "hand"
    BOARD_KEY = "board"
    all_bottoms = [
        Bottom.END_TURN, 
        Bottom.DISCARD, 
        Bottom.USE, 
        Bottom.CANCEL, 
        Bottom.YES, 
        Bottom.NO
    ]
    def __init__(self, ctx):
        self.ctx = ctx
        self.state = ctx.state
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
            for bottom in self.all_bottoms
        }

    def update_hand_availability(self, value):
        for i in range(self.state.current_player.hand.size()):
            self.hand[self.state.current_fraction][i] = value
        
    def update_board_availability(self, filter : BoardFilter):
        # allowed_types = filter.types or self.all_types
        # allowed_positions = filter.positions or board.ALL_HEXES
        # predicate = filter.predicate
        for hex in self.ctx.board.ALL_HEXES:
            x, y = hex
            self.board[x][y] = filter.matches(self.ctx, hex)
            # type = board.get_type(x, y)
            # if(type not in allowed_types):
            #     self.board[x][y] = False
            #     continue
            
            # if(hex not in allowed_positions):
            #     self.board[x][y] = False
            #     continue

            # if(predicate is None):
            #     self.board[x][y] = True
            #     continue
            
            # else:
            #     self.board[x][y] = board.predicate(x, y)
    
    def default_available_actions(self):
        if(self.ctx.actions.koniec_tury(self.state, check=True)):
            self.enable(Bottom.END_TURN)
        
        # self.update_board_availability(state.board, self.all_hexes_type, state.board.ALL_HEXES, None)
        self.update_hand_availability(True)

    def rotate_available_actions(self):
        # x = state.selected[Selected.X]
        # y = state.selected[Selected.Y]
        # pos = 
        # available = deepcopy(game.available_structure)
        filter = BoardFilter(
            positions=[self.state.seleced[Selected.POS]]
        )
        self.update_board_availability(filter)

    def enable(self, bottom):
        if bottom in self.all_bottomsbottoms:
            self.bottoms[bottom] = True

    def placing_available_actions(self):
        # available = deepcopy(game.available_structure)
        
        filter = BoardFilter(
            predicate=lambda ctx, tile : ctx.board.is_empty(tile)
        )
        self.update_board_availability(filter)
        # state.board.update_available_hexs([None], game.board.ALL_HEXES, None)

        # available[UI.BOTTOM][Bottom.CANCEL] = True
        # self.bottom[Bottom.CANCEL] = True
        self.enable(Bottom.CANCEL)
        if(self.state.phase != Phase.HQ_PLACEMENT):
            self.enable(Bottom.DISCARD)
            # self.bottom[Bottom.DISCARD] = True
            # available[UI.BOTTOM][Bottom.DISCARD] = True
        
        # self.update_available_actions(game, available)

    # def hand_available_actions(self):
    #     # name = game.selected[Selected.NAME]
    #     token = self.state.current_player.hand.get_active_token()
    #     token.get_available_actions(self.ctx)
    #     # InstantToken(game.active_action).resolve(game, Mode.AVAILABLE_ACTIONS)
    #     # return True

    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def instant_taken_available_actions(self):
        token = self.ctx.player.hand.get_active_token()
        token.get_available_actions(self.ctx)
        # name = game.active_action
        # InstantToken(name).resolve(game, Mode.AVAILABLE_ACTIONS)

    def user_available_actions(self, game):
        # print("Updating available actions...")
        # print("Current state:", game.state)
        token = self.ctx.player.hand.get_active_token()

        if(token is not None):
            token.get_available_actions(self.ctx)
            # print("active action:", game.active_action)
            # self.instant_taken_available_actions(game)
            # return True

        function = self.state_handlers.get(game.state, None)
        if not (function is None):
            function(game)
        #     return False
        # return True

