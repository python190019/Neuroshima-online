json = dict()
json["aktualna frakcja"] = "borgo"
json["druga frakcja"] = "moloch"
ham1 = {
    "frakcja" : "borgo",
    "nazwa" : "medyk",
    "rotacja" : 2,
    "rany" : 0
}
ham2 = {
    "frakcja" : "borgo",
    "nazwa" : "mutek",
    "rotacja" : 0,
    "rany" : 1
}
ham3 = {
    "frakcja" : "moloch",
    "nazwa" : "bloker",
    "rotacja" : 0,
    "rany" : 2
}
board = [
        ["None", "None", ham1, "None", "None", "None", "None", "None", "None"],
        ["None", "None", "None", "None", "None", "None", "None", "None", "None"],
        [ham1, "None", ham3, "None", ham2, "None", "None", "None", "None"],
        ["None", "None", "None", "None", "None", "None", "None", "None", "None"],
        ["None", "None", "None", "None", "None", "None", "None", "None", "None"]
                ]
hand = {
    "borgo" : [ham1, "None", "None"],
    "moloch" : [ham3, "None", "None"]
}
json["board"]  = board
json["hand"] = hand

board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
hand = {
    "borgo" : [1, 0, 0],
    "moloch" : [0, 0, 0]
}
czyklikalne = {
    "board" : board,
    "hand" : hand
}
json["czyklikalne"] = czyklikalne