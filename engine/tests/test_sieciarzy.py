from collections import defaultdict
from main.core.plansza import Board
from main.utils.variable import *
from main.actions.akcje_na_planszy import AkcjeNaPlanszy

# from plansza import Board

def print_printy(board):
    print("Plansza:")
    board.print_board()

    print("\nTestowanie kwestii sieciarzy...")
    anp = AkcjeNaPlanszy(board)
    anp.kwestia_sieciarzy()
    sieciarze = anp.sieciarze

    print("\nGraf sieciarzy:")
    for k, v in sieciarze.graf_sieciarzy.items():
        print(f"{k} -> {v}")

    print("\nOdwrócony graf:")
    for k, v in sieciarze.odwr_sieciarzy.items():
        print(f"{k} -> {v}")

    print("\nKolory SCC:")
    for siec, kolor in sieciarze.kolory.items():
        print(f"{siec} -> kolor {kolor}")

    print("\nSieciarze w kolorach:")
    for kolor, sieci in sieciarze.sieci_w_kolorze.items():
        print(f"Kolor {kolor}: {sieci}")

    print("\nGraf między SCC:")
    for k, v in sieciarze.graf_scc.items():
        print(f"SCC {k} -> {v}")

    print("----------------------------------\n")


def test_scc():
    board = Board()

    # [0, 5]
    board.postaw_zeton((2, 4), { 
        Token.FRACTION: "moloch",
        Token.NAME: "sieciarz",
        Token.ROTATION: 1,
        Token.DAMAGE: 0
    })

    board.postaw_zeton((0, 4), { 
        Token.FRACTION: "moloch",
        Token.NAME: "sieciarz",
        Token.ROTATION: 3,
        Token.DAMAGE: 0
    })

    # [0]
    board.postaw_zeton((1, 3), {
        Token.FRACTION: "testowa",
        Token.NAME: "sieciarz",
        Token.ROTATION: 2,
        Token.DAMAGE: 0
    })

    board.postaw_zeton((2, 6), {
        Token.FRACTION: "testowa",
        Token.NAME: "sieciarz",
        Token.ROTATION: 0,
        Token.DAMAGE: 0
    })

    board.postaw_zeton((1, 5), {
        Token.FRACTION: "testowa",
        Token.NAME: "sieciarz",
        Token.ROTATION: 5,
        Token.DAMAGE: 0
    })

    pop = defaultdict(int, {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2})
    
    anp = AkcjeNaPlanszy(board)
    anp.kwestia_sieciarzy()

    data = anp.sieciarze.status_sieciarzy

    # print(data)
    # print(data == pop)
    # print_printy(board)

    assert (data == pop)

    board.postaw_zeton((1, 1), { 
        Token.FRACTION: "moloch",
        Token.NAME: "sieciarz",
        Token.ROTATION: 1,
        Token.DAMAGE: 0
    })

    pop = defaultdict(int, {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2})
    
    anp = AkcjeNaPlanszy(board)
    anp.kwestia_sieciarzy()

    data = anp.sieciarze.status_sieciarzy

    # print(data)
    # print(data == pop)
    # print_printy(board)

    assert (data == pop)

if __name__ == "__main__":
    test_scc()
