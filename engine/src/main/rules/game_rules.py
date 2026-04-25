from main.utils.variable import *

class GameRules():
    def __init__(self):
        pass
    #############################################################################
    #   bottom validation functions       
    #############################################################################
    def can_execute_use(self, ctx):
        if(ctx.ui_state != State.SELECTED_HAND):
            return False
        
        if(ctx.state.active_token.name != InstantType.BITWA):
            return True
        
        if(self.is_hand_full(ctx.state.player.hand)):
            return False
        
        return self.can_end_turn(ctx)
    
    def can_execute_discard(self, ctx):
        if(ctx.ui_state != State.SELECTED_HAND):
            return False
            
        return not self.is_token_hq(ctx.state.active_token)

    def can_use_bottom(self, ctx, bottom):
        if(bottom == Bottom.USE):
            return self.can_execute_use(ctx)
        
        if(bottom == Bottom.DISCARD):
            return self.can_execute_discard(ctx)
        
        if(bottom == Bottom.END_TURN):
            return self.can_end_turn(ctx)
        return True

    #############################################################################
    #   get_available_* functions       
    #############################################################################

    def get_available_bottoms(self, ctx, wanted):
        return [
            bottom for bottom in wanted
            if self.can_use_bottom(ctx=ctx, bottom=bottom)
        ]

    def get_available_from_hand(self, ctx, hand):
        if(hand.fraction != ctx.fraction):
            return []
        return [i for i in range(hand.size)]

    #############################################################################
    #   lowlevel functions       
    #############################################################################

    def _can_move_to(self, ctx, pos, new_pos):
        if self.is_wired_at(ctx, pos) or not self.is_empty_at(ctx, new_pos):
            return False
        
        return ctx.board.is_adjacent(pos, new_pos)

    def _can_move(self, ctx, pos):
        if self.is_wired_at(ctx, pos):
            return False
        
        for hex in ctx.board.adjacent_hexes(pos):
            if self.is_empty_at(ctx, hex):
                return True
        return False

    def _can_be_pushed_by(self, ctx, pos, pusher_pos):
        if self.is_wired_at(ctx, pos) or not self.is_enemy_at(ctx, pos):
            return False
        
        for hex in ctx.board.adjacent_hexes(pos):
            if not self._can_move_to(ctx, pos, hex):
                continue
            if not ctx.board.is_adjacent(hex, pusher_pos):
                return True
        return False
            
    def _can_push(self, ctx, pos):
        if self.is_wired_at(ctx, pos):
            return False
        for hex in ctx.board.adjacent_hexes(pos):
            if self._can_be_pushed_by(ctx, hex, pos):
                return True
        return False

    #############################################################################
    #   BoardQuery predicators (can only takes context and position as arguments)     
    #############################################################################
         
    def is_ally_at(self, ctx, pos):
        return ctx.board.get_fraction(pos) == ctx.fraction

    def is_enemy_at(self, ctx, pos):
        return ctx.board.get_fraction(pos) != ctx.fraction

    def is_empty_at(self, ctx, pos):
        return ctx.board.is_empty(pos)

    def is_not_on_border(self, ctx, pos):
        return not ctx.board.on_border(pos)

    def is_wired_at(self, ctx, pos):
        return ctx.board.is_wired(pos)

    def is_hq_at(self, ctx, pos):
        return ctx.board.is_hq(pos)
    
    def can_move_from(self, ctx, pos):
        return self._can_move(ctx, pos)

    def can_push_from(self, ctx, pusher_pos):
        return self._can_push(ctx, pusher_pos)
    
    #############################################################################
    #   Other useful functions       
    #############################################################################
    def is_hand_full(self, hand):
        return hand.is_full()

    def can_end_turn(self, ctx):
        return not ctx.state.player.hand.is_full()

    def is_hq_not_wired(self, ctx):
        return not ctx.board.is_wired(ctx, ctx.board.get_hq_pos(ctx.fraction))
    
    def is_token_hq(self, token):
        return token.name == BoardType.HQ

    #############################################################################
    #   Predicate makers       
    #############################################################################
    def can_be_pushed_by(self, pusher_pos):
        def prediacte(ctx, pos):
            return self._can_be_pushed_by(ctx, pos, pusher_pos)
        return prediacte
    
    def adjacent_to(self, my_pos):
        def predicate(ctx, pos):
            return pos in ctx.board.adjacent_hexes(my_pos)
        return predicate
    
    def not_adjacent_to(self, my_pos):
        def predicate(ctx, pos):
            return pos not in ctx.board.adjacent_hexes(my_pos)
        return predicate
    