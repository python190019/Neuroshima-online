import pytest
import os
import sys
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from akcje import Actions
from main import Game
from variable import *

width = 5
length = 9
available_actions__structure = {
                          UI.HAND: {'moloch': [False, False, False], 'borgo': [False, False, False]}, 
                          UI.BOARD: [[False for _ in range(length)] for _ in range(width)], 
                          UI.BOTTOM: {
                              'end_turn': False, 
                              'discard': False, 
                              'use': False, 
                              'cancel': False, 
                              'yes': False, 
                              'no': False}
                              }
default_game_state = {'faza': 'tura', 'state': 'no_selection', 'selected': None, 'current_frakcja': 'moloch', 
                      'next_turns': [{'frakcja': 'moloch', 'typ': 'tura'}, {'frakcja': 'borgo', 'typ': 'tura'}], 
                      'board': [[None for _ in range(length)] for _ in range(width)], 
                      'pile': {"moloch" : [], 'borgo': []}, 
                      'hand': {'moloch': [], 'borgo': []}, 
                      'available_actions': available_actions__structure
                    }

def test_bitwa_selected():
    data = default_game_state
    data["hand"]["moloch"].append("bitwa")
    data["action"] = {Action.Key.TYPE : UI.HAND, Action.Key.SLOT : 0}
    game = Game(data)

    assert(game.state == State.SELECTED_HAND)
    assert(game.selected[Action.Key.SLOT] == 0)

    correct_actions = deepcopy(available_actions__structure)
    correct_actions[UI.BOTTOM][Bottom.CANCEL] = True
    correct_actions[UI.BOTTOM][Bottom.USE] = True

def test_bitwa_use():
    data = default_game_state
    data["hand"]["moloch"].append("bitwa")
    data["action"] = {Action.Key.TYPE : UI.BOTTOM, Action.Key.BOTTOM : Bottom.USE}
    data["state"] = State.SELECTED_HAND
    data["selected"] = {Selected.SLOT : 0, Selected.NAME : Token.Type.Instant.BITWA}
    data["available_actions"][UI.BOTTOM][Bottom.USE] = True
    data["next_turns"] = [{Turn.FRACTION : "moloch", Turn.TYPE : Turn.Type.STANDARD}, {Turn.FRACTION : "borgo", Turn.TYPE : Turn.Type.STANDARD}]
    game = Game(data)

    assert(game.state == State.NO_SELECTION)
    assert(game.selected == None)
    assert(game.current_frakcja == "borgo")

# def test_ruch_selected()