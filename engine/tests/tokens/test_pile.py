import pytest
from main.tokens.pile import Pile
from main.utils.variable import *

class Test_Pile:
    
    def test_remove_token(self):
        pile = Pile("moloch")
        pile.from_list(["klaun", InstantType.MOVE, "sztab"])

        pile.remove_token("klaun")
        assert(pile.to_list() == [InstantType.MOVE, "sztab"])

    def test_draw_token(self):
        pile = Pile("moloch")
        pile.from_list(["klaun", InstantType.MOVE, "sztab"])
        token = pile.draw_token()
        assert token.name == "sztab"
        assert (pile.to_list() == ["klaun", InstantType.MOVE])

    def test_is_empty(self):
        pile = Pile("moloch")
        pile.from_list([])
        assert pile.is_empty()