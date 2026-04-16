from hand import Hand
from pile import Pile

class TokenManager:
    CURRENT_FRACTION_KEY = "current_fraction"
    HAND_KEY = "hand"
    PILE_KEY = "pile"
    def __init__(self, fractions):
        self.fractions = fractions
        self.hand = Hand(fractions)
        self.pile = Pile(fractions)
        self.current_fracition = None

    def import_tokens(self, data):
        self.current_fraction = data.get(TokenManager.CURRENT_FRACTION_KEY, None)
        self.hand.from_dict(data.get(TokenManager.HAND_KEY, {}))
        self.pile.from_dict(data.get(TokenManager.PILE_KEY, {}))