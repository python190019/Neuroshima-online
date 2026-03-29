def dobierz(hand, pile, frakcja, nazwa):
    # print("dobierz: ", frakcja, nazwa)
    hand[frakcja].append(nazwa)
    pile[frakcja].remove(nazwa)

def dociag(hand, pile, frakcja):
    while(len(hand[frakcja]) <= 3 and len(pile) > 0):
            dobierz(hand, pile, frakcja, pile[-1])