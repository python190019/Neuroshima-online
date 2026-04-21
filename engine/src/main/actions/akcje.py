from copy import deepcopy

from collections import defaultdict
from main.utils.variable import *
# from zeton import Zeton
from main.actions.sieciarze import Sieciarze
from main.tokens.instant_token import InstantToken
from main.battle.battle import Battle

class Actions:
    def __init__(self, game):
        # self.MAX_HAND_SIZE = game.MAX_HAND_SIZE
        # self.bottom_handlers = {
        #     Bottom.END_TURN : self.handle_end_turn,
        #     Bottom.DISCARD : self.handle_discard,
        #     Bottom.CANCEL : self.handle_cancel,
        #     Bottom.USE : self.handle_use
        # }
        self.action_handlers = {
            Action.Type.BOARD : self.handle_board,
            Action.Type.HAND : self.handle_hand,
            Action.Type.ROTATE : self.handle_rotate,
            Action.Type.BOTTOM : self.handle_bottom,
        }

        

    #############################################################################
    #   Board functions       
    #############################################################################
    def wstawianie(self, state, action):
        # print("Wstawianie:", action, name)
        player = state.current_player
        pos = action[Action.Key.POS]
        token = player.hand.get_active_token()
        state.board.assign_to_tile(pos, token)
        state.player.hand.discard_active_token()
        state.state = State.ROTATE
        state.selected = {Selected.POS : pos, Selected.NAME : token.name}
        state.active_action = {}
        
    def kwestia_sieciarzy(self, board):
        Sieciarze().kwestia_sieciarzy(board)

    #############################################################################
    #   Turn functions       
    #############################################################################
    def poczatek_tury(self, state):
        if(state.current_frakcja != None):
            return False
        fraction = state.next_turns[0][Turn.FRACTION]
        type = state.next_turns[0][Turn.TYPE]
        state.current_frakcja = fraction
        
        if(fraction == Turn.BITWA):
            Battle(state)
            return True

        if(type == Turn.Type.HQ_PLACEMENT):
            state.phase = Phase.HQ_PLACEMENT
            # self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

        else:
            state.phase = Phase.GAME
        
        player = state.current_player
        player.draw_tokens(type)

        if(player.pile.is_empty()):
            state.next_turns.append({Turn.FRACTION : Turn.BITWA, Turn.TYPE : Turn.Type.LAST})

        self.prepare_for_new_action(state)
        return True

    def koniec_tury(self, state):
        # print("next turns:", game.next_turns)
        next_turn = state.next_turns[0]
        fraction = next_turn[Turn.FRACTION]
        
        state.next_turns.pop(0)
        state.next_turns.append({Turn.FRACTION : fraction, Turn.TYPE : Turn.Type.STANDARD})
        state.current_fraction = None

    #############################################################################
    #   General functions       
    #############################################################################
    # def get_zeton_type(self, nazwa, frakcja):
    #     return wszystkie_frakcje.frakcje.get(frakcja, {}).get(nazwa, {}).get(Token.TYPE, None)

    def invalid_move(self, message=""):
        print("INVALID MOVE")
        if(message):
            print(message)

    def get_enemy(self, my_fraction, fractions):
        for fraction in fractions:
            if(my_fraction != fraction):
                return fraction

    #############################################################################
    #   Validation functions       
    #############################################################################

   

    
   
    #############################################################################
    #   Bottoms functions      
    #############################################################################
    def handle_end_turn(self, game):
        self.poczatek_tury(game)
        self.koniec_tury(game)
        self.prepare_for_new_action(game)
        return True

    def handle_cancel(self, game):
        self.prepare_for_new_action(game)
        return True
    
    def handle_use(self, game):
        InstantToken(game.active_action).resolve(game, Mode.USE)
        return True

    def handle_discard(self, game):
        self.odrzuc(self.game.hand[game.current_frakcja], self.selected[Selected.SLOT])
        self.prepare_for_new_action(game)
        return True

    #############################################################################
    #   Handler functions      
    #############################################################################
    def prepare_for_new_action(self, state):
        self.kwestia_sieciarzy(state.board)
        state.state = State.NO_SELECTION
        state.selected = None
        state.active_action = None

    def handle_board(self, game, action):
        print("handle_board")
        # print(f"Selected token: {name}")
        if game.state == State.PLACING:
            name = game.selected[Selected.NAME]
            return self.wstawianie(game, action, name)
        
        InstantToken(game.active_action).resolve(game, Mode.USE)
        return True
        
    def handle_hand(self, game, action):
        hand = game.hand[game.current_frakcja]
        nazwa = self.get_from_hand(hand, action[Action.Key.SLOT])
        type = self.get_zeton_type(nazwa, game.current_frakcja)
        print("handle_hand")
        print(f"Selected token: {nazwa}, type: {type}")

        if(type == Token.Type.BOARD):
            game.state = State.PLACING
            game.active_action = None
        
        if(type == Token.Type.INSTANT):
            game.state = State.SELECTED_HAND
            game.active_action = nazwa
        game.selected = {Selected.SLOT : action[Action.Key.SLOT], Selected.NAME : nazwa}
        return True

    def handle_bottom(self, game, action):
        name = action[Action.Key.BOTTOM]
        function = self.bottom_handlers.get(name, None)
        return function(game)
        
    def handle_rotate(self, game, action):
        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        rotation = action[Action.Key.ROTATION]
        game.board.rotate(x, y, rotation)
        self.prepare_for_new_action(game)
        return True


    def handler(self, game):
        action = game.action
        if(action is None):
            return True
        
        print("USER ACTION:", action)
        print("Validating game state...")
        if(not self.validate_action(game, action)):
            return False
        
        print(f"action: {action} is valid")
        function = self.action_handlers.get(action[Action.Key.TYPE], None)
        return function(game, action)