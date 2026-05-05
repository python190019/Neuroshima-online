from main.workflows.base import Workflow
from main.state.contex import ActionContext

class MoveWorkflow(Workflow):
    def __init__(self, rules):
        super().__init__(rules)

    @classmethod
    def start(cls, ctx : ActionContext, workflow_source = None):
        ctx.workflow_data = 
        return cls.