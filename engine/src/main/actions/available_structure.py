from main.utils.variable import Bottom

class AvailableStructure:
    def __init__(self, hand, board, bottom):
        self.hand = hand
        self.board = board
        self.bottom = bottom

        @classmethod
        def build(cls, ctx):
            self.hand = {
            fraction : [False for _ in range(player.hand.size())]
            for fraction, player in ctx.state.players.items()
            }
            self.board = {
                hex : False
                for hex in ctx.state.board.ALL_HEXES
            }
            self.bottoms = {
                bottom : False
                for bottom in Bottom
            }
            return cls(hand, board, bottom)