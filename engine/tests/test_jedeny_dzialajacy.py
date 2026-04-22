from main.core.plansza import Board
from main.actions.akcje_na_planszy import AkcjeNaPlanszy
from main.utils.variable import *

def test_sieciarze():
    board = Board()

    board.postaw_zeton((2, 4), { 
        Token.FRACTION: "moloch",
        Token.NAME: "sieciarz",
        Token.ROTATION: 1,
        Token.DAMAGE: 0
    })

    board.postaw_zeton((0, 4), { 
        Token.FRACTION: "sieciarz",
        Token.NAME: "sieciarz",
        Token.ROTATION: 3,
        Token.DAMAGE: 0
    })

    anp = AkcjeNaPlanszy(board)
    anp.kwestia_sieciarzy()

    board.print_board()
