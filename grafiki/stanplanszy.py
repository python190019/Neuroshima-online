from plansza import *
from rysujhanda import *
from tranform import *
def stanplanszy(self, json):
    self.bok = 0.18
    self.wszystko = []
    plansza(self)
    frakcja = jason["aktualnia frakcja"]
    for y in range(5):
        for x in range(9):
            if json[board][y][x] != "None":
                self.wszystko.append(transform(
                    (6-x)*((math.sqrt(3)/2) * a),
                    (j-2)*(2*a),
                    json[board][y][x]["frakcja"],
                    json[board][y][x]["nazwa"],
                    1,
                    json[board][y][x]["rotacja"]*60 + 30,
                    x,
                    y,
                    json[board][y][x]["rotacja"]
                    ))
    rysujhanda(self, json, )
    
