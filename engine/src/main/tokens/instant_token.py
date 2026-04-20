from main.utils.variable import *
from main.tokens.abstract_token import Token
from main.board.board_query import BoardQuery
from main.actions.available_action_result import AvailableActionResult

class InstantToken(Token):
    # TYPE = "instant"

    def __init__(self, name, fraction):
        super().__init__(name, fraction, TokenType.INSTANT)
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

    def export(self):
        return self.name

    def get_available_actions(self, ctx):
        handler = self.available_actions_handlers.get(self.name, None)
        if handler:
            return handler(ctx)
        return AvailableActionResult()
    
    def use(self, ctx):
        handler = self.use_handlers.get(self.name, None)
        if handler:
            return handler(ctx)
    #############################################################################
    #   Bitwa functions       
    #############################################################################

    def available_actions_bitwa(self, ctx):
        return AvailableActionResult(
            can_use=ctx.rules.can_end_turn(),
            can_discard=True
        )

    def use_bitwa(self, ctx):
        actions = ctx.actions
        state = ctx.state

        ctx.player.hand.discard_active_token()
        actions.koniec_tury(state)
        state.next_turns.insert(0, {Turn.FRACTION : Turn.BITWA, Turn.TYPE : None})
        actions.poczatek_tury(state)

    #############################################################################
    #   Move functions       
    #############################################################################
    

    def available_actions_move(self, ctx):
        state = ctx.state
        rules = ctx.rules

        if(state.state == State.SELECTED_HAND):
            query = BoardQuery([
                    rules.is_ally,
                    rules.can_move
                ])
            return AvailableActionResult(
                positions=query.apply(),
                can_discard=True,
                can_cancel=True
            )
        
        if(state.state == State.MOVING):
            pos = state.selected[Selected.POS]
            query = BoardQuery([
                    rules.adjacent_to(pos),
                    rules.is_empty
                ])
            return AvailableActionResult(
                positions = query.apply() + [pos],
                can_cancel=True 
            )
        
    def use_move(self, ctx):
        state = ctx.state
        action = state.action
        if(state.state == State.SELECTED_HAND):
            pos = action[Action.Key.POS]
            state.state = State.MOVING
            state.selected = {
                Selected.POS : pos, 
                Selected.NAME : ctx.board.get_name(pos)
            }

        if(state.state == State.MOVING):
            old_pos = state.selected[Selected.POS]
            new_pos = action[Action.Key.POS]
            ctx.board.przenies(old_pos, new_pos)
            state.state = State.ROTATE
            state.selected[Selected.POS] = new_pos
            player = state.current_player
            player.hand.discard_active_token()
          
    #############################################################################
    #   Bomb functions       
    #############################################################################

    def available_actions_bomb(self, ctx):
        query = BoardQuery([ctx.rules.not_on_border])
        return AvailableActionResult(
            positions=query.apply(),
            can_discard=True,
            can_cancel=True
        )
    
    def use_bomb(self, ctx):
        pos = ctx.state.action[Action.Key.POS]
        targets = [pos] + ctx.board.adjacent_hexes(pos)
        for target in targets:
            if(ctx.board.is_not_hq(target)):
                ctx.board.deal_damage(pos, 1)
        
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()
        ctx.actions.prepare_for_new_action(ctx.state)
    
    #############################################################################
    #   Grenade functions       
    #############################################################################

    def available_actions_grenade(self, ctx):
        positions = []
        rules = ctx.rules
        # pos = ctx.board.find_zeton(BoardType.HQ, ctx.fraction)
        # tile = ctx.board.get_tile(pos)
        pos = ctx.board.get_hq_pos(ctx.fraction)
        if rules.is_hq_not_wired(ctx.fraction):
            query = BoardQuery([
                rules.adjacent_to(pos),
                rules.is_enemy,
                rules.not_hq
            ])
            

        return AvailableActionResult(
            positions = query.apply(),
            can_cancel=True,
            can_discard=True
        )

    def use_grenade(self, ctx):
        pos = ctx.state.action[Action.Key.POS]
        ctx.board.deal_damage(pos, 100)
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()
        ctx.actions.prepare_for_new_action(ctx.state)

    #############################################################################
    #   Sniper functions       
    #############################################################################

    def available_actions_sniper(self, ctx):
        rules = ctx.rules
        query = BoardQuery([
            rules.is_enemy,
            rules.not_hq
        ])
        return AvailableActionResult(
            positions=query.apply(),  
            can_cancel=True,
            can_discard=True
        )

    
    def use_sniper(self, ctx):
        pos = ctx.state.action[Action.Key.POS]
        ctx.board.deal_damage(pos, 1)
        ctx.board.zdejmij_trupy()
        ctx.player.hand.discard_active_token()

        ctx.actions.prepare_for_new_action(ctx.state)

    #############################################################################
    #   Push functions       
    #############################################################################
    def _push_selected_hand(self, ctx):
        rules = ctx.rules
        query = BoardQuery([
            rules.can_push,
            rules.is_ally
        ])
        return AvailableActionResult(
            positions=query.apply(),
            can_cancel=True,
            can_discard=True
        )

    def _push_selected_pusher(self, ctx):
        pusher_pos = ctx.selected[Selected.POS]
        rules = ctx.rules
        query = BoardQuery([
            rules.adjacent_to(pusher_pos),
            rules.is_enemy,
            rules.can_be_pushed_by(pusher_pos)
        ])
        return AvailableActionResult(
            positions=query.apply(),
            can_discard=True,
            can_cancel=True
        )

    def _push_selected_pushing(self, ctx):
        my_pos = ctx.selected[Selected.POS]
        pusher_pos = ctx.selected[Selected.PUSHER_POS]
        rules = ctx.rules
        query = BoardQuery([
            rules.adjacent_to(my_pos),
            rules.is_empty,
            rules.not_adjacent_to(pusher_pos)
        ])
        return AvailableActionResult(positions=query.apply())

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
        if(ctx.state.state == State.SELECTED_HAND):
            ctx.state.state = State.SELECTED_PUSHER
            pos = ctx.state.action[Action.Key.POS]
            ctx.state.selected = {
                Selected.POS : pos, 
                Selected.NAME : ctx.board.get_name(pos)
            }
            ctx.active_action = InstantType.PUSH
        
        elif(ctx.state.state == State.SELECTED_PUSHER):
            pos = ctx.state.action[Action.Key.POS]
            pusher_pos = ctx.selected[Selected.POS]
            ctx.state.selected={
                Selected.POS : pos,
                Selected.NAME : ctx.board.get_name(pos),
                Selected.PUSHER_POS : pusher_pos
            }
            ctx.state.state = State.PUSHING
            ctx.state.active_action = InstantType.PUSH
            ctx.state.current_frakcja = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            

        elif(ctx.state.state == State.PUSHING):
            target_pos = ctx.selected[Selected.POS]
            new_pos = ctx.state.action[Action.Key.POS]
            ctx.board.przenies(target_pos, new_pos)
            ctx.state.current_frakcja = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            ctx.player.hand.discard_active_token()
            ctx.actions.prepare_for_new_action(ctx.state)