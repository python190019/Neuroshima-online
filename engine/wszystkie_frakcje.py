from importlib import import_module
from copy import deepcopy

dostepne_frakcje = ["moloch", "borgo"]
frakcje = {}

for frakcja in dostepne_frakcje:
    lib = import_module(frakcja)
    frakcje[frakcja] = deepcopy(lib.wlasciwosci)