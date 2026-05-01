from abc import ABC, abstractmethod
from main.rules.game_rules import GameRules

class Token(ABC):
    def __init__(self, rules: GameRules, name, fraction, token_type):
        self.name = name
        self.fraction = fraction
        self.token_type = token_type