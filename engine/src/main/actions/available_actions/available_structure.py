from main.utils.variable import Bottom
from main.actions.available_actions.available_action_result import AvailableActionResult

class AvailableStructure:
    BOTTOM_KEY = "bottom"
    HAND_KEY = "hand"
    BOARD_KEY = "board"
    def __init__(self, hand, board, bottoms):
        self.hand = hand
        self.board = board
        self.bottoms = bottoms

    @classmethod
    def build(cls, ctx):
        hand = {
            fraction: [False for _ in range(player.hand.size())]
            for fraction, player in ctx.state.players.items()
        }
        board = {
            hex: False
            for hex in ctx.state.board.ALL_HEXES
        }
        bottoms = {
            bottom: False
            for bottom in Bottom
        }
        return cls(hand, board, bottoms)

    @staticmethod
    def false_dict(dict):
        return {
            key : False
            for key in dict
        }

    def false_hand(self):
        false_hand = {}
        for fraction in self.hand:
            false_hand[fraction] = [False for _ in self.hand[fraction]]
        return false_hand

    def reset(self):
        self.board = self.false_dict(self.board)
        self.bottoms = self.false_dict(self.bottoms)
        self.hand = self.false_hand()

    def apply_active_key(self, dict, result):
        for key in result:
            dict[key] = True

    def apply_hand(self, hand_result):
        for fraction, idxes in hand_result.items():
            for i in idxes:
                self.hand[fraction][i] = True

    def apply(self, result : AvailableActionResult):
        self.reset()
        self.apply_active_key(dict=self.board, keys=result.positions)
        self.apply_active_key(dict=self.bottoms, keys=result.bottoms)
        self.apply_hand(result.hand)

    def to_dict(self):
        return {
            self.BOARD_KEY : self.board,
            self.BOTTOM_KEY : self.bottoms,
            self.HAND_KEY : self.hand
        }