
class BoardQuery():
    def __init__(self, predicates=None):
        self.predicates = predicates or []

    def matches(self, ctx, pos):
        return all(p(ctx, pos) for p in self.predicates)

    def apply(self, ctx):
        return [
            pos for pos in ctx.board.ALL_HEXES
            if self.matches(ctx, pos)
        ]