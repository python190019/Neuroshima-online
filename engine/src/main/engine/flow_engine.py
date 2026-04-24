from main.flows.flows import EndTurnEvent
from main.flows.flows import BeginTurnEvent
from main.flows.flows import StartBattleEvent
from main.utils.variable import Turn

class FlowProcessor():
    def __init__(self):
        self.handler = {
            EndTurnEvent : self.end_turn,
            BeginTurnEvent : self.begin_turn,
            StartBattleEvent : self.start_battle 
        }

    def process(self, ctx):
        while ctx.state.flow_queue:
            event = ctx.state.flow_queue.pop(0)
            function = self.handler.get(event)
            if function:
                function(ctx)
            else:
                raise ValueError("No such event\n")

     #############################################################################
    #   Turn functions       
    #############################################################################
    # def poczatek_tury(self, state):
    #     if(state.current_frakcja != None):
    #         return False
    #     fraction = state.next_turns[0][Turn.FRACTION]
    #     type = state.next_turns[0][Turn.TYPE]
    #     state.current_frakcja = fraction
        
    #     if(fraction == Turn.BITWA):
    #         Battle(state)
    #         return True

    #     if(type == Turn.Type.HQ_PLACEMENT):
    #         state.phase = Phase.HQ_PLACEMENT
    #         # self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

    #     else:
    #         state.phase = Phase.GAME
        
    #     player = state.current_player
    #     player.draw_tokens(type)

    #     if(player.pile.is_empty()):
    #         state.next_turns.append({Turn.FRACTION : Turn.BITWA, Turn.TYPE : Turn.Type.LAST})

    #     self.prepare_for_new_action(state)
    #     return True

    # def koniec_tury(self, state):
    #     # print("next turns:", game.next_turns)
    #     next_turn = state.next_turns[0]
    #     fraction = next_turn[Turn.FRACTION]
        
    #     state.next_turns.pop(0)
    #     state.next_turns.append({Turn.FRACTION : fraction, Turn.TYPE : Turn.Type.STANDARD})
    #     state.current_fraction = None

    def end_turn(self, ctx):
        next_turn = ctx.state.next_turns[0]
        fraction = next_turn[Turn.FRACTION]
        
        ctx.state.next_turns.pop(0)
        ctx.state.next_turns.append({Turn.FRACTION : fraction, Turn.TYPE : Turn.Type.STANDARD})

    def begin_turn(self, ctx):
        pass

    def start_battle(self, ctx):
        pass