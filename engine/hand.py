from variable import *
from token_manager import TokenManager

class Hand(TokenManager):
    MAX_HAND_SIZE = 3
    CURRENT_MAX_HAND_SIZE_KEY = "current_max_hand_size"
    def __init__(self):
        self.current_max_hand_size = 1

    @property
    def active_hand(self):
        return self.hand.get(self.current_fraction, None)

    def add_token(self, token):
        if(len(self.active_hand) >= self.current_max_hand_size):
            return False
        self.active_hand.append(token)
        return True

    def discard_token(self, token):
        if(token in self.active_hand):
            self.active_hand.remove(token)
            return True
        return False

    def draw_tokens(self, pile):
        while(len(self.active_hand) < self.current_max_hand_size and len(pile) > 0):
            drawn_token = pile.pop()
            self.add_token(drawn_token)

    def get_token(self, place):
        if(place < 0 or place >= len(self.active_hand)):
            return None
        return self.active_hand[place]

    def update_current_max_hand_size(self, turn_type):
        if(turn_type == Turn.Type.HQ_PLACEMENT or turn_type == Turn.Type.FIRST):
            self.current_max_hand_size = 1
            return
        
        if(turn_type == Turn.Type.SECOND):
            self.current_max_hand_size = 2
            return

        self.current_max_hand_size = Hand.MAX_HAND_SIZE

    def from_dict(self, hand_data):
        self.current_max_hand_size = hand_data.get(Hand.CURRENT_MAX_HAND_SIZE_KEY, Hand.MAX_HAND_SIZE)
        for fraction in self.fractions:
            self.hand[fraction] = hand_data.get(fraction, [])

    def to_dict(self):
        data = {Hand.CURRENT_MAX_HAND_SIZE_KEY : self.current_max_hand_size}
        
        for fraction in self.fractions:
            data[fraction] = []
            for token in self.hand[fraction]:
                data[fraction].append(token)
        return data
    
    def print_hand(self):
        print(self.to_dict())