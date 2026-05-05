from abc import ABC, abstractmethod
from main.workflows.data import WorkflowData
from main.workflows.data import WorkflowSource
from main.state.contex import ActionContext
from enum import Enum

class Workflow(ABC):
    def __init__(self, rules):
        super().__init__()
        self.rules = rules


    @classmethod
    @abstractmethod
    def start(cls, 
              ctx : ActionContext, 
              workflow_source : WorkflowSource | None =  None
        ):
        pass

    @abstractmethod
    def finish(self, ctx : ActionContext): 
        pass
   
    @abstractmethod
    def advance(self, ctx : ActionContext):
        pass

    @abstractmethod
    def get_current_step(self, ctx : ActionContext):
        pass

class WorkflowName(Enum):
    MOVE = "move"
    PUSH = "Push"
    ROTATE = "rotate"
    BOMB = "bomb"
    GRENADE = "grenade"
    SNIPER = "sniper"
    BATTLE = "battle"
    CHOOSING_ACTION = "choosing_action"


class WorkflowFactory:
    WORKFLOWS = {
        WorkflowName.MOVE : 
    }
    @classmethod
    def create(cls, workflow_data : WorkflowData):
