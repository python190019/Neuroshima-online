import pytest
from main.tokens.hand import Hand

# from hand import Hand
# from pile import Pile
from main.utils.variable import *


class Test_hand:

    # def test_draw_tokens(self):
    #     hand = Hand("moloch")
    #     hand.from_dict({Hand.TOKENS_KEY : ["sieciarz"]})
    #     pile = Pile("moloch")
    #     pile.from_list(["ruch", "klaun", "bloker"])
    #     hand.draw_tokens(pile, "normal")

    #     assert hand.tokens == ["sieciarz", "bloker", "klaun"]
    #     assert pile.tokens == ["ruch"]

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

    # def test_odrzuc(self):
    #     game = DummyGame()
    #     actions = Actions(game)
    #     hand = ["a", "b"]
    #     actions.odrzuc(hand, "a")
    #     assert hand == ["b"]
