from main.tokens.board_token import BoardToken
from main.tokens.instant_token import InstantToken
import main.frakcje.wszystkie_frakcje as allfractions
from main.utils.variable import *

class TokenFactory():
    @staticmethod
    def create(rules, name, fraction, data={}):
        # cos = allfractions.frakcje.get("moloch", {})
        # print("cos:", cos)
        # print("name:", name)
        stats = allfractions.frakcje.get(fraction, {}).get(name, {})
        # print(stats)
        token_type = stats.get(TokenKey.TYPE)
        if(token_type == TokenType.INSTANT):
            return InstantToken(rules, name, fraction)
        elif(token_type == TokenType.BOARD):
            return BoardToken(rules, name, fraction, data)
        # print("")
        raise ValueError(f"nie znaleziono żetonu o nazwie {name} z frakcji {fraction}")