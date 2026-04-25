from abc import ABC, abstractmethod
from main.rules.game_rules import GameRules

class Token(ABC):
    def __init__(self, rules: GameRules, name, fraction, token_type):
        self.rules: GameRules = rules
        self.name = name
        self.fraction = fraction
        self.token_type = token_type

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        
        if isinstance(other, Token):
            return (
                self.name == other.name
                and self.fraction == other.fraction
                and self.token_type == other.token_type
            )
        