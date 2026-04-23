from main.flows.flows import EndTurnEvent
from main.flows.flows import BeginTurnEvent
from main.flows.flows import StartBattleEvent

class FlowProcessor():
    def __init__(self):
        self.handler = {
            EndTurnEvent : self.end_turn,
            BeginTurnEvent : self.begin_turn,
            StartBattleEvent : self.start_battle 
        }

    def process_events(self, ctx):
        while ctx.state.flow_queue:
            event = ctx.state.flow_queue.pop(0)
            function = self.handler.get(event)
            if function:
                function(ctx)
            else:
                raise ValueError("No such event\n")

    def end_turn(self, ctx):
        pass

    def begin_turn(self, ctx):
        pass

    def start_battle(self, ctx):
        pass