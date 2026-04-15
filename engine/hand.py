from variable import *

class Hand:
    MAX_HAND_SIZE = 3
    CURRENT_MAX_HAND_SIZE_KEY = "current_max_hand_size"
    def __init__(self, fractions, current_fraction = None):
        self.hand = {fraction : [] for fraction in fractions}
        self.current_fraction = current_fraction
        self.fractions = fractions
        self.current_max_hand_size = 1

    @property
    def active_hand(self):
        return self.hand.get(self.current_fraction, None)
    
    def set_current_fraction(self, fraction):
        if(fraction not in self.fractions):
            self.current_fraction = None
        else:
            self.current_fraction = fraction

    def add_token(self, token):
        if(self.current_fraction is None):
            return False
        if(len(self.active_hand) >= self.current_max_hand_size):
            return False
        self.active_hand.append(token)
        return True

    def discard_token(self, token):
        if(self.current_fraction is None):
            return False
        if(token in self.active_hand):
            self.active_hand.remove(token)
            return True
        return False

    def draw_tokens(self, pile):
        if(self.current_fractions is None):
            return False
        
        while(len(self.active_hand) < self.current_max_hand_size and len(pile) > 0):
            drawn_token = pile.pop()
            self.add_token(drawn_token)

    def get_token(self, place):
        if(self.current_fraction is None):
            return None
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

    def next_turn(self, current_fraction, pile, turn_type):
        if(current_fraction not in self.fractions):
            return False
        self.set_current_fraction(current_fraction)
        self.update_current_max_hand_size(turn_type)
        self.draw_tokens(pile)
        return True
        

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