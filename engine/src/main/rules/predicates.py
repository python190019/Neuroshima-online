def NOT(predicate):
    def not_predicate(ctx, pos):
        return not predicate(ctx, pos)
    return not_predicate

def is_ally_at(ctx, pos):
    return ctx.board.get_fraction(pos) == ctx.fraction

def is_enemy_at(ctx, pos):
    return ctx.board.get_fraction(pos) != ctx.fraction

def is_empty_at(ctx, pos):
    return ctx.board.is_empty(pos)

def is_not_on_border(ctx, pos):
    return not ctx.board.on_border(pos)

def is_wired_at(ctx, pos):
    return ctx.board.is_wired(pos)

def not_is_wired_at(ctx, pos):
    return not ctx.board.is_wired(pos)

def is_hq_at(ctx, pos):
    return ctx.board.is_hq(pos)

def not_hq_at(ctx, pos):
    return not is_hq_at(ctx, pos)

def adjacent_to(my_pos):
    def predicate(ctx, pos):
        return pos in ctx.board.adjacent_hexes(my_pos)
    return predicate
    
def not_adjacent_to(my_pos):
    def predicate(ctx, pos):
        return pos not in ctx.board.adjacent_hexes(my_pos)
    return predicate