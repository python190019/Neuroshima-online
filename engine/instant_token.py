from variable import *
from copy import deepcopy
from variable import *
from token import Token
from boardfilter import BoardFilter
from available_action_result import AvailableActionResult

class InstantToken(Token):
    TYPE = "instant"

    def __init__(self, name, fraction=None):
        super().__init__(name, fraction, self.TYPE)
        # self.name = name
        self.use_handlers = {
            TokenType.Instant.BITWA : self.use_bitwa,
            TokenType.Instant.MOVE : self.use_move,
            TokenType.Instant.BOMB : self.use_bomb,
            TokenType.Instant.GRENADE : self.use_grenade,
            TokenType.Instant.SNIPER : self.use_sniper,
            TokenType.Instant.PUSH : self.use_push,
        }
        self.available_actions_handlers = {
            TokenType.Instant.BITWA : self.available_actions_bitwa,
            TokenType.Instant.MOVE : self.available_actions_move,
            TokenType.Instant.BOMB : self.available_actions_bomb,
            TokenType.Instant.GRENADE : self.available_actions_grenade,
            TokenType.Instant.SNIPER : self.available_actions_sniper,
            TokenType.Instant.PUSH : self.available_actions_push,
        }
        # self.use = self.use_handlers.get(name, None)
        # self.get_available_actions = self.available_actions_handlers.get(name, None)

    def get_available_actions(self, ctx):
        handler = self.available_actions_handlers.get(self.name, None)
        if handler:
            return handler(ctx)
        return AvailableActionResult()
    
    def use(self, ctx):
        handler = self.use_handlers.get(self.name, None)
        if handler:
            return handler(ctx)

    # def resolve(self, game, mode):
    #     if(mode == Mode.AVAILABLE_ACTIONS):
    #         if(self.available_actions):
    #             self.available_actions(game)
    #     if(mode == Mode.USE):
    #         if(self.use):
    #             return self.use(game)
    #     return False

    #############################################################################
    #   Bitwa functions       
    #############################################################################

    def available_actions_bitwa(self, ctx):
        # print("bitwa available actions")
        # available = deepcopy(game.available_structure)
        return AvailableActionResult(
            can_use=ctx.rules.can_end_turn(),
            can_discard=True
        )
        # game.board.update_available_hexs([], [], None)
        # if(game.actions.koniec_tury(game, True)):
        #     available[UI.BOTTOM][Bottom.USE] = True

        # available[UI.BOTTOM][Bottom.DISCARD] = True
        # # print("available:", available)
        # game.actions.update_available_actions(game, available)

    def use_bitwa(self, ctx):
        actions = ctx.actions
        state = ctx.state
        # actions.odrzuc(game.hand[game.current_frakcja], InstantType.BITWA)
        ctx.player.hand.discard_active_token()
        actions.koniec_tury(state)
        state.next_turns.insert(0, {Turn.FRACTION : Turn.BITWA, Turn.TYPE : None})
        actions.poczatek_tury(state)
        # return True

    #############################################################################
    #   Move functions       
    #############################################################################

    def available_actions_move(self, ctx):
        # available = deepcopy(game.available_structure)
        # print("move available actions:", available)
        state = ctx.state
        # fraction = state.current_fraction
        # board = state.board

        if(state.state == State.SELECTED_HAND):
            return AvailableActionResult(
                board_filter=BoardFilter(
                    positions=[
                        hex for hex in ctx.board.ALL_HEXES
                        if ctx.board.can_move(hex)
                        and ctx.board.get_relation(hex, ctx.fraction) == Relation.FRIENDLY
                    ]
                ),
                can_discard=True,
                can_cancel=True
            )
            # game.board.update_available_hexs([game.current_frakcja], game.board.ALL_HEXES, game.board.can_move)
            # available[UI.BOTTOM][Bottom.DISCARD] = True
            # available[UI.BOTTOM][Bottom.CANCEL] = True
        
        if(state.state == State.MOVING):
            pos = state.selected[Selected.POS]
            # x = state.selected[Selected.X]
            # y = state.selected[Selected.Y]
            positions = [
                hex for hex in ctx.board.adjacent_hexes(pos)
                if ctx.board.is_empty(hex)
            ]
            return AvailableActionResult(
                positions = positions + [pos] 
            )
            # adj = game.board.adjacent_hexes(x, y)
            # # print(adj)
            # game.board.update_available_hexs([None], adj, None)
            # game.board.available_hexs[x][y] = True
            # # print(game.board.available_hexs)
            # available[UI.BOTTOM][Bottom.CANCEL] = True

        # game.actions.update_available_actions(game, available)

    def use_move(self, ctx):
        state = ctx.state
        action = state.action
        # board = state.board
        # print("state:", game.state)
        if(state.state == State.SELECTED_HAND):
            # x = action[Action.Key.X]
            # y = action[Action.Key.Y]
            pos = Action.Key.POS
            state.state = State.MOVING
            state.selected = {
                Selected.POS : pos, 
                Selected.NAME : ctx.board.get_name(pos)
            }
            # return True

        if(state.state == State.MOVING):
            # print("finishing move...")
            # x = game.selected[Selected.X]
            # y = game.selected[Selected.Y]
            old_pos = state.selected[Selected.POS]
            new_pos = action[Action.Key.POS]
            # nx = action[Action.Key.X]
            # ny = action[Action.Key.Y]              
            ctx.board.przenies(old_pos, new_pos)
            state.state = State.ROTATE
            state.selected[Selected.POS] = new_pos
            # game.active_action = None
            player = state.current_player
            player.hand.discard_active_token()
            # print(game.state)
            
        # return True
    
    #############################################################################
    #   Bomb functions       
    #############################################################################

    def available_actions_bomb(self, ctx):
        # state = ctx.state
        # board = ctx.board
        # print("bomb available actions")
        # available = deepcopy(game.available_structure)
        return AvailableActionResult(
            board_filter=BoardFilter(
                pos for pos in ctx.board.ALL_HEXES
                if ctx.board.not_on_bound(pos)
            ),
            can_discard=True,
            can_cancel=True
        )
        # available[UI.BOTTOM][Bottom.DISCARD] = True
        # available[UI.BOTTOM][Bottom.CANCEL] = True
        # game.board.update_available_hexs(Variable.ALL, game.board.ALL_HEXES, game.board.not_on_bound)
        # game.actions.update_available_actions(game, available)
    
    def use_bomb(self, ctx):
        # state = ctx.state
        # action = state.action
        pos = ctx.state.action[Action.Key.POS]
        # x = action[Action.Key.X]
        # y = action[Action.Key.Y]
        targets = [pos] + ctx.board.adjacent_hexes(pos)
        for target in targets:
            if(ctx.board.is_not_hq(target)):
                ctx.board.deal_damage(pos, 1)
                # continue
        
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()
        ctx.actions.prepare_for_new_action(ctx.state)
        return True
    
    #############################################################################
    #   Grenade functions       
    #############################################################################

    def available_actions_grenade(self, ctx):
        # available = deepcopy(game.available_structure)
        # available[UI.BOTTOM][Bottom.DISCARD] = True
        # available[UI.BOTTOM][Bottom.CANCEL] = True

        positions = []
        predicate = lambda ctx, tile : True
        pos = ctx.board.find_zeton(BoardType.HQ, ctx.fraction)
        tile = ctx.board.get_tile(pos)
        if not tile.czy_zasieciowany():
            positions = [
                hex for hex in ctx.board_adjacent_hexes(pos)
                if ctx.board.get_relation(hex, ctx.fraction) == Relation.ENEMY
            ]
            predicate = lambda ctx, tile : ctx.board.not_is_hq(tile)
        
        return AvailableActionResult(
            board_filter=BoardFilter(
                positions=positions,
                predicate=predicate
            ),
            can_cancel=True,
            can_discard=True
        )

        # # hq = game.board.find_zeton(Token.Type.Board.HQ, game.current_frakcja)
        # # print("HQ found at:", (hq.x, hq.y))
        # if(not hq.czy_zasieciowany()):
        #     fractions = [game.enemy[game.current_frakcja]]
        #     hexes = game.board.adjacent_hexes(hq.x, hq.y)
        #     game.board.update_available_hexs(fractions, hexes, game.board.not_is_hq)
        # game.actions.update_available_actions(game, available)

    def use_grenade(self, ctx):
        # action = game.action
        pos = ctx.state.action[Action.Key.POS]
        # x = action[Action.Key.X]
        # y = action[Action.Key.Y]
        ctx.board.deal_damage(pos, 100)
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()
        # game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.GRENADE)
        ctx.actions.prepare_for_new_action(ctx.state)

    #############################################################################
    #   Sniper functions       
    #############################################################################

    def available_actions_sniper(self, ctx):
        # available = deepcopy(game.available_structure)
        # available[UI.BOTTOM][Bottom.DISCARD] = True
        # available[UI.BOTTOM][Bottom.CANCEL] = True
        return AvailableActionResult(
            board_filter=BoardFilter(
                positions=[
                    hex for hex in ctx.board.ALL_HEXES
                    if ctx.board.get_relation(hex, ctx.fraction) == Relation.ENEMY
                ]
            ),
            can_cancel=True,
            can_discard=True
        )

        # game.board.update_available_hexs([game.enemy[game.current_frakcja]], game.board.ALL_HEXES, game.board.not_is_hq)
        # game.actions.update_available_actions(game, available)
    
    def use_sniper(self, ctx):
        pos = ctx.state.action[Action.Key.POS]
        # action = game.action
        # x = action[Action.Key.X]
        # y = action[Action.Key.Y]
        ctx.board.deal_damage(pos, 1)
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()

        # game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.SNIPER)
        ctx.actions.prepare_for_new_action(ctx.state)

    #############################################################################
    #   Push functions       
    #############################################################################
    def _push_selected_hand(self, ctx):
        # if(state.state == State.SELECTED_HAND):
        #     return self.selecting_pusher_available_actions(ctx)
        #     # game.board.update_available_hexs([game.current_frakcja], game.board.ALL_HEXES, game.board.can_push)
        #     # available[UI.BOTTOM][Bottom.DISCARD] = True
        #     # available[UI.BOTTOM][Bottom.CANCEL] = True
        return AvailableActionResult(
            board_filter= BoardFilter(
                positions=[
                    hex for hex in ctx.board.ALL_HEXES
                    if ctx.board.can_push(hex)
                ]
            ),
            can_cancel=True,
            can_discard=True
        )

    def _push_selected_pusher(self, ctx):
         # elif(ctx.state == State.SELECTED_PUSHER):
        #     # print("selected pusher available actions")
        #     pusher_pos = ctx.selected[Selected.POS]
        #     # x = game.selected[Selected.X]
        #     # y = game.selected[Selected.Y]
        #     adj = game.board.adjacent_hexes(x, y)
        #     # print("adjacent hexes:", adj)
        #     game.board.update_available_hexs([game.enemy[game.current_frakcja]], adj, game.board.can_move)
        #     available[UI.BOTTOM][Bottom.CANCEL] = True
        pos = ctx.selected[Selected.POS]
        return AvailableActionResult(
            board_filter=BoardFilter(
                positions=[
                    hex for hex in ctx.board.adjacent_hexes(pos)
                    if ctx.board.get_relation(hex, ctx.fraction) is Relation.ENEMY
                    and ctx.board.can_move(hex)
                ]
            ),
            can_discard=True,
            can_cancel=True
        )

    def _push_selected_pushing(self, ctx):
        # elif(game.state == State.PUSHING):
        #     x = game.selected[Selected.X]
        #     y = game.selected[Selected.Y]
        #     px = game.selected[Selected.PUSHER_X]
        #     py = game.selected[Selected.PUSHER_Y]

        #     my_adj = game.board.adjacent_hexes(x, y)
        #     pusher_adj = game.board.adjacent_hexes(px, py)
        #     adj = []
        #     for hex in my_adj:
        #         if(hex not in pusher_adj):
        #             adj.append(hex)
        #     game.board.update_available_hexs([None], adj, None)
        my_pos = ctx.selected[Selected.POS]
        pusher_pos = ctx.selected[Selected.PUSHER_POS]
        return AvailableActionResult(
            board_filter=BoardFilter(
                positions=[
                    hex for hex in ctx.board.adjacent_hexes(my_pos)
                    if not ctx.board.is_adjactent(hex, pusher_pos)
                ]
            )
        )

    def available_actions_push(self, ctx):
        state = ctx.state.state

        handler = {
            State.SELECTED_HAND: self._push_selected_hand,
            State.SELECTED_PUSHER: self._push_selected_pusher,
            State.PUSHING: self._push_pushing,
        }.get(state)

        if handler:
            return handler(ctx)

        return AvailableActionResult()

    def use_push(self, ctx):
        # print("using push...")
        # action = ct.action
        if(ctx.state.state == State.SELECTED_HAND):
            ctx.state.state = State.SELECTED_PUSHER
            pos = ctx.state.action[Action.Key.POS]
            # x = action[Action.Key.X]
            # y = action[Action.Key.Y]
            # name = game.board.get_name(x, y)
            ctx.state.selected = {
                Selected.POS : pos, 
                Selected.NAME : ctx.board.get_name(pos)
            }
            ctx.active_action = InstantType.PUSH
            # return True

        elif(ctx.state.state == State.SELECTED_PUSHER):
            # print("selected pusher:", game.selected)
            # x = action[Action.Key.X]
            # y = action[Action.Key.Y]
            pos = ctx.state.action[Action.Key.POS]
            pusher_pos = ctx.selected[Selected.POS]
            # name = game.board.get_name(x, y)
            # px = game.selected[Selected.X]
            # py = game.selected[Selected.Y]
            ctx.state.selected={
                Selected.POS : pos,
                Selected.NAME : ctx.board.get_name(pos),
                Selected.PUSHER_POS : pusher_pos
            }
            # game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
            # game.selected[Selected.PUSHER_X] = px
            # game.selected[Selected.PUSHER_Y] = py
            ctx.state.state = State.PUSHING
            ctx.state.active_action = InstantType.PUSH
            # print("enemy fraction:", game.enemy[game.current_frakcja])
            ctx.state.current_frakcja = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            # print("state after selecting target:", game.current_frakcja, game.state)
            return True

        elif(ctx.state.state == State.PUSHING):
            target_pos = ctx.selected[Selected.POS]
            # target_x = game.selected[Selected.X]
            # target_y = game.selected[Selected.Y]
            new_pos = ctx.state.action[Action.Key.POS]
            # nx = action[Action.Key.X]
            # ny = action[Action.Key.Y]
            ctx.board.przenies(target_pos, new_pos)
            ctx.state.current_frakcja = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            ctx.player.hand.discard_active_token()
            ctx.actions.prepare_for_new_action(ctx.state)

            # game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.PUSH)
            # game.actions.prepare_for_new_action(game)
            # return True
