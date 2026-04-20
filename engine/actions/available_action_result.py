
class AvailableActionResult():
    def __init__(self, positions=None, can_use=False, can_cancel=False, can_discard=False):
        self.positions = positions or []
        self.can_use = can_use
        self.can_discard = can_discard
        self.can_cancel = can_cancel