import pytest
from main.tokens.hand import Hand
from main.tokens.pile import Pile
from main.utils.variable import *


class Test_hand:
    def setup_hand(self, fraction, tokens=None, active=None):
        data = {
            Hand.TOKENS_KEY : tokens or [],
            Hand.ACTIVE_TOKEN_KEY : active
        }
        hand = Hand(fraction)
        hand.from_dict(data)

        return hand
    
    def get_left_tokens(self, hand):
        return hand.to_dict().get(Hand.TOKENS_KEY, [])

    def test_from_dict(self):
        hand =self.setup_hand(
            "moloch", 
            ["sieciarz", "bloker", "klaun"],
            active=1
            )
        
        output = hand.to_dict()
        tokens = output[Hand.TOKENS_KEY]
        assert tokens == ["sieciarz", "bloker", "klaun"]
        assert output[Hand.ACTIVE_TOKEN_KEY] == 1

    def test_draw_tokens(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz"]})
        pile = Pile("moloch")
        pile.from_list(["ruch", "klaun", "bloker"])
        hand.draw_tokens(pile, Turn.Type.STANDARD)

        left_tokens = hand.to_dict().get(Hand.TOKENS_KEY, None)
        assert left_tokens == ["sieciarz", "bloker", "klaun"]
        assert pile.tokens == ["ruch"]

    # def test_draw_tokens2(self):
    #     hand = Hand("moloch")
    #     hand.from_dict({Hand.TOKENS_KEY : ["sieciarz"]})
    #     pile = Pile("moloch")
    #     pile.from_list(["ruch", "klaun", "bloker"])
    #     hand.draw_tokens(pile, Turn.Type.SECOND)

    #     assert hand.tokens == ["sieciarz", "bloker"]
    #     assert pile.tokens == ["ruch", "klaun"]

    def test_get_token(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz", "bloker", "klaun"]})
        token = hand.get_token(1)
        assert(token.name == "bloker")
        assert(hand.active_token == 1)

        token = hand.get_active_token()
        assert(token.name == "bloker")
        assert(hand.active_token == 1)

    def test_discard_active_token(self):
        hand = Hand("moloch")
        hand.from_dict({Hand.TOKENS_KEY : ["sieciarz", "bloker", "klaun"]})
        hand.get_token(1)
        hand.discard_active_token()
        left_tokens = hand.to_dict().get(Hand.TOKENS_KEY, None)
        assert (left_tokens == ["sieciarz", "klaun"])
        assert (hand.active_token == None)