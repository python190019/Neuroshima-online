from copy import deepcopy
from plansza import Board
import wszystkie_frakcje
import akcje

class Game:
    def __init__(self, data):
        self.board = Board()
        if(data["current_player"] == "poczatek"):
            self.start_game(data["frakcje"][0], data["frakcje"][1])

        else:
            self.current_player = data["current_player"]
            self.user_actions = data["user_actions"]
            self.board.import_board(data["board"])
            self.pile = data["pile"]
            self.hand = data["hand"]

    def start_game(self, frakcja1, frakcja2):
        self.current_player = 0
        self.user_actions = []
        self.armie = [frakcja1, frakcja2]
        self.pile = {
                    frakcja1 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja1, {})], 
                     frakcja2 : [nazwa for nazwa in wszystkie_frakcje.frakcje.get(frakcja2, {})]
                    }
        self.hand = {frakcja1 : [], frakcja2 : []}
        akcje.dobierz(self.hand, self.pile, frakcja1, "sztab")
        akcje.dobierz(self.hand, self.pile, frakcja2, "sztab")
        self.current_player = 0

    def postaw_zeton(self, zeton):
        self.board.postaw_zeton(zeton["x"], zeton["y"], zeton)

    def export_game_state(self):
        data = {
                "current_player" : self.current_player,
                "user_actions" : self.user_actions,
                "board" : self.board.board_to_json(), 
                "pile" : self.pile,
                "hand" : self.hand,
                }
        return data
