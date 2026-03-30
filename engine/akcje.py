from copy import deepcopy

def dobierz(hand, pile, frakcja, nazwa):
    hand.append(nazwa)
    pile.remove(nazwa)

def odrzuc(hand, zeton):
    hand.remove(zeton)

def dociag(hand, pile, frakcja):
    while(len(hand) < 3 and len(pile) > 0):
            dobierz(hand, pile, frakcja, pile[-1])

def bitwa(board):

    for inicjatywa in range(9, -1, -1):
        for i in range(5):
            for j in range(9):
                if board[i][j] is not None:
                    board[i][j].aktywuj(inicjatywa)

        for i in range(5):
            for j in range(9):
                if board[i][j] is not None:
                    board[i][j].koniec_inicjatywy()


def invalid_move(user_actions):
    print("INVALID MOVE")
    user_actions.clear()
   
def poczatek_tury(game):
    if(game.current_frakcja != None):
        return
    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    if(frakcja == "bitwa"):
        bitwa()
        return

    game.current_frakcja = frakcja
    if(typ == "wystaw_sztab"):
        dobierz(game.hand[frakcja], game.pile[frakcja], frakcja, "sztab")

    else:
        dociag(game.hand[frakcja], game.pile[frakcja], frakcja)

    if(len(game.pile[frakcja]) == 0):
        game.next_turns.append({"frakcja" : "bitwa", "typ" : "ostatnia"})

def koniec_tury(game):

    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    if((typ == "wystaw_sztab") and (len(game.hand[frakcja]) > 0)):
        invalid_move(game.user_actions)
        return

    if(frakcja == "bitwa"):
        game.user_actions.clear()
        game.next_turns.pop(0)
        if(typ == "ostatnia"):
            game.game_over = 1
            return
    
    if(len(game.hand[frakcja]) == 3):
        invalid_move(game.user_actions)
        return
    
    game.user_actions.clear()
    game.next_turns.pop(0)
    game.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
    game.current_frakcja = None

def postaw_zeton(board, hand, frakcja, nazwa, x, y):
    odrzuc(hand, nazwa)
    zeton = {"nazwa" : nazwa, "frakcja" : frakcja, "rany" : 0, "rotacja" : 0}
    board.postaw_zeton(x, y, zeton)

def get_first(actions):
    if(len(actions) == 0):
        return "empty"
    action = actions[0]
    actions.pop(0)
    return action

def obracanie(actions, board, x, y):
    # print("obracanie")
    action = get_first(actions)
    if(action == "empty"):
        return
    
    click = get_first(action)
    if(click == "empty"):
        return

    if(click == "left"):
        board.rotate(x, y, -1)
        return

    elif(click == "right"):
        board.rotate(x, y, 1)
        return

    else:
        return "done"

def co_zrobic(game):
    actions = deepcopy(game.user_actions)
    
    action = get_first(actions)

    if(action == "empty"):
        return

    click = get_first(action)
    
    if(click == "done"):
        koniec_tury(game)
        poczatek_tury(game)
        return
    
    elif(click == "rotate"):
        x = get_first(action)
        y = get_first(action)

        if(not game.board.on_board(x, y)):
            invalid_move(game.user_actions)
            return

        if(len(action) != 0):
            invalid_move(game.user_actions)
            return
    
        response = obracanie(actions, game.board, x, y)
        if(response == "done"):
            game.user_actions.clear()
            return

        else:
            game.user_actions.clear()
            game.user_actions.append(["rotate", x, y])
            return
        

    elif(click == "hand"):
        click = get_first(action)

        if(not isinstance(click, int)):
            invalid_move(game.user_actions)
            return

        hand = game.hand[game.current_frakcja]
        if(len(hand) <= click):
            invalid_move(game.user_actions)
            return

        zeton = hand[click]
        action = get_first(actions)

        if(action == "empty"):
            return
        
        click = get_first(action)

        if(click == "board"):
            x = get_first(action)
            y = get_first(action)
            
            if((not isinstance(x, int)) or (not isinstance(y, int))):
                invalid_move(game.user_actions)
                return

            if(not game.board.is_empty(x, y)):
                invalid_move(game.user_actions)
                return
            
            postaw_zeton(game.board, hand, game.current_frakcja, zeton, x, y)
            # game.faza = "rotate"
            game.user_actions.clear()
            game.user_actions.append(["rotate", x, y])
            return

        elif(click == "odrzuc"):
            odrzuc(hand, zeton)
            game.user_actions.clear()
            return
        
        else:
            invalid_move(game.user_actions)
            return
        
    else:
        invalid_move(game.user_actions)
        return