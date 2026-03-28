from copy import deepcopy
import moloch
import borgo
import json

frakcje = {
    "moloch": deepcopy(moloch.wlasciwosci),
    "borgo": deepcopy(borgo.wlasciwosci),
    # "hegemonia": hegemonia.wlasciwosci,
    # "posterunek": posterunek.wlasciwosci,
}

roza = {
    0: [-1, 1],
    1: [0, 2],
    2: [1, 1],
    3: [1, -1],
    4: [0, -2],
    5: [-1, -1]
}


class Zeton:
    def __init__(self,x, y, frakcja, nazwa, rotacja):
        self.frakcja = frakcja
        self.nazwa = nazwa
        self.rotacja = rotacja
        self.x = x
        self.y = y
        
        self.wlasciwosci = frakcje.get(frakcja, {}).get(nazwa, {})

    def __getitem__(self, key):
        # pozwala robis self["xd"] zamiast self.wlasciwosci["xd"]
        return self.wlasciwosci.get(key)
    
    def czy_w_planszy(self, x, y):
        return (0 <= x < 5 and 0 <= y < 9)

    def postaw_na_plansze(self, x, y):
        self.board[x][y] = self

    def dostan_rane(self, obrazenia, kierunek, jaki_atak):
        # kierunek -> skad przychodzi atak
        kierunek2 = (kierunek - self.rotacja + 6) % 6

        if "pancerz" in self.wlasciwosci and kierunek2 in self["pancerz"] and jaki_atak == "strzal":
            obrazenia -= 1

        self.wlasciwosci["hp"] -= obrazenia

    def koniec_inicjatywy(self):
        if self["hp"] <= 0:
            # wywolaj_medyka()
            board[self.x][self.y] = None

    
    def aktywuj(self, nr_inicjatywy):
        if "inicjatywa" in self.wlasciwosci and nr_inicjatywy in self["inicjatywa"]:
            if ("atak" in self.wlasciwosci):
                # print(self.frakcja, self.nazwa, nr_inicjatywy)

                for atak, sila in self["atak"]:
                    atak_obr = (atak + self.rotacja) % 6
                    nowyx = self.x + roza[atak_obr][0]
                    nowyy = self.y + roza[atak_obr][1]
                    
                    if self.czy_w_planszy(nowyx, nowyy) and board[nowyx][nowyy] is not None:
                        # print("nowyx, nowyy: ", nowyx, nowyy)
                        if board[nowyx][nowyy].frakcja != self.frakcja:
                            board[nowyx][nowyy].dostan_rane(sila, (atak_obr + 3) % 6, "atak")

            if ("strzal" in self.wlasciwosci):
                # print(self.frakcja, self.nazwa, nr_inicjatywy)

                for strzal, sila in self["strzal"]:
                    strzal_obr = (strzal + self.rotacja) % 6
                    nowyx = self.x + roza[strzal_obr][0]
                    nowyy = self.y + roza[strzal_obr][1]
                    
                    while self.czy_w_planszy(nowyx, nowyy):
                        # print("nowyx, nowyy: ", nowyx, nowyy)

                        if board[nowyx][nowyy] is not None:
                            if board[nowyx][nowyy].frakcja != self.frakcja:
                                board[nowyx][nowyy].dostan_rane(sila, (strzal_obr + 3) % 6, "strzal")
                                break
                        nowyx += roza[strzal_obr][0]
                        nowyy += roza[strzal_obr][1]

length = 9
width = 5
board = [[None] * length for i in range(width)]
user_actions = []

def import_data(data):

    for x in width:
        for y in length:
            board[x][y] = data["board"]["x"]["y"]

    user_actions = data["user_actions"]


def board_to_json():
    json_board = [[None] * length for i in range(width)]
    for i in range(width):
        for j in range(length):
            if board[i][j] is not None:
                json_board[i][j] = {
                    "frakcja": board[i][j].frakcja,
                    "nazwa": board[i][j].nazwa,
                    "rotacja": board[i][j].rotacja,
                    "hp": board[i][j]["hp"]
                    # "wlasciwosci": board[i][j].wlasciwosci
                }
    return json_board

def export_game_state():
    data = {"board" : board_to_json(), "user_actions" : user_actions}
    return data