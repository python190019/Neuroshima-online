from objekt import *
def rhand(self, g, frakcja, hand, bok):
    for i in range(-1, 2, 1):
        if(frakcja == "inne"):
            if(hand[i+1] != "None"):
                ter = obj(g*4.3*bok*1.1*self.getAspectRatio(), (3/2)*bok*math.sqrt(3)*i*1.1, frakcja + "/podswietl" + ".png", bok*2*math.sqrt(3)/2, bok*2, 1, 30, hand[i+1], self, 0.3, "hex", bok)
                ter.wyswietl(True)
        else:
            if(hand[i+1] != "None"):
                ter = obj(g*4.3*bok*1.1*self.getAspectRatio(), (3/2)*bok*math.sqrt(3)*i*1.1, frakcja + "/" + hand[i+1]["nazwa"] + ".png", bok*2*math.sqrt(3)/2, bok*2, 1, 30, hand[i+1]["nazwa"], self, 1, "hex", bok)
                ter.wyswietl(True)