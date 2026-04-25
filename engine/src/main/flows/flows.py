class FlowEvent:
    pass

class EndTurnEvent(FlowEvent):
    pass

class BeginTurnEvent(FlowEvent):
    pass

class StartBattleEvent(FlowEvent):
    pass

class SetupBattleEvent(FlowEvent):
    pass

class SwapPlayerEvent(FlowEvent):
    pass