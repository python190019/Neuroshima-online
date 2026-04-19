
class AvailableActionResult():
    def __init__(self, board_filter=None, can_use=False, can_cancel=False, can_discard=False):
        self.board_filter = board_filter
        self.can_use = can_use
        self.can_discard = can_discard
        self.can_cancel = can_cancel