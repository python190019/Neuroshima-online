from objekt import *
def zadajrany(app, x, z, ile, bok):
    mbok = 0.5*bok
    if(ile == 1):
        ter = obj(x, z, "inne/rana.png", mbok, mbok, 2, 0, "rana", app, 1, "inne", mbok)
        ter.wyswietl(True)
    if(ile == 2):
        ter = obj(x-mbok/4, z, "inne/rana.png", mbok, mbok, 2, 0, "rana", app, 1, "inne", mbok)
        ter.wyswietl(True)
        ter = obj(x+mbok/4, z, "inne/rana.png", mbok, mbok, 3, 0, "rana", app, 1, "inne", mbok)
        ter.wyswietl(True)