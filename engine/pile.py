from token_manager import TokenManager
from wszystkie_frakcje import wszystkie_frakcje
from random import shuffle
from variable import *

class Pile(TokenManager):
    def __init__(self, fractions):
        self.pile = {fraction : [] for fraction in fractions}

    def create_pile(self, fraction):
        for nazwa in wszystkie_frakcje.frakcje.get(fraction, {}):
            for _ in range(wszystkie_frakcje.frakcje[fraction][nazwa][Token.UNIT_COUNT]):
                self.pile[fraction].append(nazwa)
        shuffle(self.pile[fraction])

    def create_piles(self):
        for fraction in self.fractions:
            self.create_pile(fraction)

    def from_dict(self, pile_data):
        for fraction in self.fractions:
            self.pile[fraction] = pile_data.get(fraction, [])

    def to_dict(self):
        return self.pile
    
    @property
    def active_pile(self):
        return self.pile.get(self.current_fraction, None)

    def remove_token(self, name):
        if self.active_pile is None:
            print("No active pile to remove token from.")
            return False
        self.active_pile.remove(name)

    def draw_token(self):
        if self.active_pile is None:
            print("No active pile to draw token from.")
            return None
        if len(self.active_pile) == 0:
            print("Active pile is empty, cannot draw token.")
            return None
        return self.active_pile.pop()