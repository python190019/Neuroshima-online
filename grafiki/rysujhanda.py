import math
from objekt import *
def rhand(self, gracz, tura, hand, bok):
    g = -1
    if(gracz == tura):
        g = 1
    for i in range(-1, 2, 1):
        ter = obj(g*4*bok*1.1*self.getAspectRatio(), (3/2)*bok*math.sqrt(3)*i*1.1, hand[i+1], bok*2*math.sqrt(3)/2, bok*2, 1, 30, hand[i+1], self, 1, "hex", bok)
        ter.wyswietl(True)
        self.przesuwalne.append(ter)
        self.podswietlone[ter] = self.pusty