from dataclasses import dataclass
from enum import StrEnum

Hex = tuple[int, int]

class WorkflowSource(StrEnum):
    HAND = "hand"
    BOARD = "board"
    

@dataclass
class WorkflowData:
    unit_pos : Hex | None = None
    target_pos : Hex | None = None
    destination : Hex | None = None
    source : WorkflowSource | None = None
    current_step_index : int = 0

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def to_dict(self):
        return 