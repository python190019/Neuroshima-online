import pytest
from akcje import Actions
from main import Game

class test_board:
    def test_start(self):
        data = {
            "faza": "newgame",
            "frakcje": {
                "player1": "borgo",
                "player2": "moloch"
            }
        }

        data = Game(data)

        poprawne = {'faza': 'sztaby', 'next_turns': [{'frakcja': 'borgo', 'typ': 'wystaw_sztab'}, {'frakcja': 'moloch', 'typ': 'wystaw_sztab'}, {'frakcja': 'bitwa', 'typ': 'ostatnia'}], 'current_frakcja': 'borgo', 'user_actions': [], 'board': [[None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None]], 'pile': {'borgo': [], 'moloch': ['bloker', 'hybryda', 'dzialkogaussa', 'juggernaut', 'klaun', 'lowca', 'obronca', 'opancerzonylowca', 'opancerzonywartownik', 'szerszeń', 'sieciarz', 'sztab', 'szturmowiec', 'wartownik']}, 'hand': {'borgo': ['sztab', None, None], 'moloch': [None, None, None]}, 'available_actions': {'hand': {'borgo': [True, False, False], 'moloch': [False, False, False]}, 'board': [[False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False], [False, False, False, False, False, False, False, False, False]], 'bottoms': {'koniec tury': False, 'kosz': False, 'użyj': False, 'cancel': False, 'tak': False, 'nie': False}}}
        # trzeba nanosic kazda zmiane, bo moga zmieniac poprawne z zmiana koncepji

        self.data = data
        assert ((data["board"] != poprawne["board"]) and data["current_frakcja"] == "borgo")

    def test_wstawianie(self):
        data = Game(data)

        #nwm jak ma wygladac komunikacja z frontendem, gdzie dodac clik