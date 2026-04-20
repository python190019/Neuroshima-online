from variable import *
from board_query import BoardQuery

class GameRules():
    def __init__(self, state):
        self.state = state
        self.player = state.current_player

    #############################################################################
    #   lowlevel functions       
    #############################################################################

    def _can_move_to(self, ctx, pos, new_pos):
        if self.is_wired(ctx, pos) or not self.is_empty(ctx, new_pos):
            return False
        
        return ctx.board.is_adjacent(pos, new_pos)

    def _can_move(self, ctx, pos):
        if self.is_wired(ctx, pos):
            return False
        
        for hex in ctx.board.adjacent_hexes(pos):
            if self.is_empty(ctx, hex):
                return True
        return False

    def _can_be_pushed_by(self, ctx, pos, pusher_pos):
        if self.is_wired(ctx, pos) or not self.is_enemy(ctx, pos):
            return False
        
        for hex in ctx.board.adjacent_hexes(pos):
            if not self._can_move_to(ctx, pos, hex):
                continue
            if not ctx.board.is_adjacent(hex, pusher_pos):
                return True
        return False
            
    def _can_push(self, ctx, pos):
        if self.is_wired(ctx, pos):
            return False
        for hex in ctx.board.adjacent_hexes(pos):
            if self._can_be_pushed_by(ctx, hex, pos):
                return True
        return False

    #############################################################################
    #   BoardQuery predicators (can only takes context and position as arguments)     
    #############################################################################
         
    def is_ally(self, ctx, pos):
        return ctx.board.get_fraction(pos) == ctx.fraction

    def is_enemy(self, ctx, pos):
        return ctx.board.get_fraction(pos) != ctx.fraction

    def is_empty(self, ctx, pos):
        return ctx.board.is_empty(pos)

    def can_move(self, ctx, pos):
        return self._can_move(ctx, pos)

    def not_on_border(self, ctx, pos):
        return not ctx.board.on_border(pos)

    def is_wired(self, ctx, pos):
        return ctx.board.is_wired(pos)

    def is_hq(self, ctx, pos):
        return ctx.board.is_hq(pos)

    #############################################################################
    #   Other useful functions       
    #############################################################################

    def can_end_turn(self):
        return not self.player.hand.is_full()

    def can_push(self, ctx, pusher_pos):
        return self._can_push(ctx, pusher_pos)

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
    
    def is_hq_not_wired(self, ctx):
        return not ctx.board.is_wired(ctx, ctx.board.get_hq_pos(ctx.fraction))