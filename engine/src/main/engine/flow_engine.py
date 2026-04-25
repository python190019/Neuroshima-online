from main.flows.flows import EndTurnEvent
from main.flows.flows import BeginTurnEvent
from main.flows.flows import StartBattleEvent
from main.flows.flows import SetupBattleEvent
from main.utils.variable import Turn, Phase
from main.actions.exeute_actions.action_result import ActionResult
from main.state.changes import ResetInteraction
from main.battle.battle import Battle

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
            function = self.handler.get(type(event))
            if function:
                function(ctx)
            else:
                raise ValueError(f"No such event {event}\n")

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
        ctx.state.next_turns.append({
            Turn.FRACTION : fraction, 
            Turn.TYPE : Turn.Type.STANDARD
        })

        return ActionResult(interaction_state_changes=[ResetInteraction()])

    def begin_turn(self, ctx):
        fraction = ctx.state.next_turns[0][Turn.FRACTION]
        type = ctx.state.next_turns[0][Turn.TYPE]
        ctx.state.current_frakcja = fraction
        
        if(type == Turn.Type.HQ_PLACEMENT):
            ctx.state.phase = Phase.HQ_PLACEMENT
        else:
            ctx.state.phase = Phase.GAME

        ctx.player.draw_tokens(type)
        return ActionResult()

    def setup_battle(self, ctx):
        Battle().run()
        ctx.flow_queue.append(BeginTurnEvent())

    def start_battle(self, ctx):
        ctx.phase = Phase.BATTLE
        ctx.flow_queue.append(EndTurnEvent())
        ctx.flow_queue.append(SetupBattleEvent())
        
        