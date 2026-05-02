from dataclasses import dataclass
from enum import Enum

Hex = tuple[int, int]

class WorkflowSource(Enum):
    HAND = "hand"
    BOARD = "board"

@dataclass
class WorkflowData:
    unit_pos : Hex | None = None
    target_pos : Hex | None = None
    destination : Hex | None = None
    source : WorkflowSource | None = None