from objekt import *
from string import *
def zamien(x, y, frakcja, nazwa, warstwa, rotacja, px, py, app, trans, rany):
    male = app.bok*0.8
    if(rany == 1):
        ter = obj(x, y, "podswietl.png", male, male, warstwa+1, 0, "rana", app, 1, "nic", male)
        ter.wyswietl(True)
    if(rany == 2):
        ter = obj(x+(app.bok/4), y, "pole.png", male, male, warstwa+1, 0, "rana", app, 1, "nic", male)
        ter.wyswietl(True)
        ter = obj(x-(app.bok/4), y, "podswietl.png", male, male, warstwa+2, 0, "rana", app, 1, "nic", male)
        ter.wyswietl(True)
    return obj(x, y, frakcja + "/" + nazwa + ".png", app.bok*math.sqrt(3), app.bok*2, warstwa, rotacja, str(px) + " " + str(py), app, trans, "hex", app.bok)