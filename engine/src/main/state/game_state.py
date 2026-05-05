from dataclasses import dataclass, fields, field, MISSING
from main.utils.variable import *
from main.state.player_state import PlayerState
from main.board.board import Board
from main.state.selection import Selected
from main.effects.flow_effects import FlowEvent
from collections import deque
from main.workflows.data import WorkflowData
from main.state.serialization import convert_value, auto_to_dict

def print_obj(obj, deepth):
    base_s = "\n" + "   " * deepth
    pre_s = "\n" + "   " * (deepth - 1)
    # print("PRINTING: ", obj, "deepth: ", deepth)
    if(isinstance(obj, dict)):
        if(deepth > 0):
            print(pre_s + "--->", end='')
        for k, v in obj.items():
            print(base_s, k, end='', sep='')
            print_obj(v, deepth + 1)
        
        if(deepth > 0):
            print(pre_s + "#####",end='')
        return True
    
    if(isinstance(obj, list)):
        if(deepth > 0):
            print(pre_s + "||||", end='')
        for v in obj:
            status = print_obj(v, deepth + 1)
            print(',', end=('\n' if status else ''))
        
        if(deepth > 0):
            print(pre_s + "////",end='')
        
        return True

    
    
    print(" ", obj, end='')
    return False

@dataclass
class GameState:
    phase : str
    fractions           : list[str]
    interaction_state   : str = State.NO_SELECTION
    selected            : Selected = field(default_factory=Selected)
    active_action       : dict = field(default_factory=dict)
    current_fraction    : str = ""
    next_turns          : list[dict] = field(default_factory=list)
    players             : dict[str, PlayerState] = field(default_factory=dict)
    board               : Board = field(default_factory=Board)
    flow_queue          : deque[FlowEvent] = field(default_factory=deque)
    workflow_data       : WorkflowData = field(default_factory=WorkflowData)

    @classmethod
    def from_dict(cls, data):
        values = {}
        for f in fields(cls):
            if(f.name in data):
                value = data.get(f.name)
                values[f.name] = convert_value(value, f.type)

            else:
                if f.default is not MISSING or f.default_factory is not MISSING:
                    continue
                raise ValueError(f"Missing required field: {f.name}")
            
        return cls(**values)
    
    def to_dict(self):
        return {
            f.name : auto_to_dict(getattr(self, f.name))
            for f in fields(self)
        }

    def print_game_state(self):
        print_obj(self.to_dict(), 0)

    def add_player(self, fraction):
        player = PlayerState(fraction)
        player.new_game()
        self.players[fraction] = player