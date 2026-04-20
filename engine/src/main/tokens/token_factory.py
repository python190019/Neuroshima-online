from main.tokens.board_token import BoardToken
from main.tokens.instant_token import InstantToken
import main.frakcje.wszystkie_frakcje as allfractions
from main.utils.variable import *

class TokenFactory():
    @staticmethod
    def create(name, fraction, data={}):
        stats = allfractions.frakcje.get(fraction, {}).get(name, {})
        token_type = stats.get(TokenKey.TYPE)
        if(token_type == TokenType.INSTANT):
            return InstantToken(name, fraction)
        elif(token_type == TokenType.BOARD):
            return BoardToken(name, fraction, data)
        return None