from copy import deepcopy

def dobierz(hand, pile, frakcja, nazwa):
    hand.append(nazwa)
    pile.remove(nazwa)

def odrzuc(hand, zeton):
    hand.remove(zeton)

def dociag(hand, pile, frakcja):
    while(len(hand) < 3 and len(pile) > 0):
            dobierz(hand, pile, frakcja, pile[-1])

# def bitwa(board):

#     for inicjatywa in range(9, -1, -1):
#         for i in range(5):
#             for j in range(9):
#                 if board[i][j] is not None:
#                     board[i][j].aktywuj(inicjatywa)

#         for i in range(5):
#             for j in range(9):
#                 if board[i][j] is not None:
#                     board[i][j].koniec_inicjatywy()
def get_from_hand(hand, click):
    if(not isinstance(click, int)):
        return None

    if(len(hand) <= click):
        return None

    return hand[click]

def invalid_move(user_actions):
    print("INVALID MOVE")
    user_actions.clear()
   
def poczatek_tury(game):
    if(game.current_frakcja != None):
        return
    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    # if(frakcja == "bitwa"):
    #     bitwa()
    #     return

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
    if(actions is None or len(actions) == 0):
        return None
    
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

def wstawianie(user_actions, board, hand, action, zeton, frakcja):
    x = get_first(action)
    y = get_first(action)
    
    if(not board.on_board(x, y)):
        return False

    if(not board.is_empty(x, y)):
        return False
    
    postaw_zeton(board, hand, frakcja, zeton, x, y)
    user_actions.clear()
    user_actions.append(["rotate", x, y])
    return True

def from_hand(game, action, zeton):
    hand = game.hand[game.current_frakcja]
    if(zeton is None):
        return False

    click = get_first(action)
    
    if(click == "board"):
        status = wstawianie(game.user_actions, game.board, hand, action, zeton, game.current_frakcja)
        return status

    elif(click == "odrzuc"):
        odrzuc(hand, zeton)
        game.user_actions.clear()
        return True
    
    else:
        return False
    
def co_zrobic(game):
    actions = deepcopy(game.user_actions)
    action = get_first(actions)
    click = get_first(action)

    if(click is None):
        return

    if(click == "done"):
        koniec_tury(game)
        poczatek_tury(game)
        return
    
    elif(click == "rotate"):
        x = get_first(action)
        y = get_first(action)
    
        response = obracanie(actions, game.board, x, y)
        game.user_actions.clear()
        if(response != "done"):
            game.user_actions.append(["rotate", x, y])
        

    elif(click == "hand"):
        hand = game.hand[game.current_frakcja]
        zeton = get_from_hand(hand, get_first(action))
        action = get_first(actions)
        if(action is None):
            return
        
        status = from_hand(game, action, zeton)
        if(status == False):
            invalid_move(game.user_actions)
            return
        
    else:
        invalid_move(game.user_actions)
        return