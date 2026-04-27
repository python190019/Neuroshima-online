class FlowEvent:
    pass

class EndTurnEvent(FlowEvent):
    pass

class BeginTurnEvent(FlowEvent):
    pass

class StartBattleEvent(FlowEvent):
    def __init__(self, attacker, defender):
        super().__init__()
        self.attacker = attacker
        self.defender = defender
    pass

class SetupBattleEvent(FlowEvent):
    pass

class SwapPlayerEvent(FlowEvent):
    pass