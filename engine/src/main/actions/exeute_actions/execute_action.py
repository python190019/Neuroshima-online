from copy import deepcopy

from main.utils.variable import *
from main.actions.exeute_actions.action_result import ActionResult
from main.effects.effects import DiscardActiveTokenEffect, RotateEffect, PlaceEffect
from main.state.changes import ResetInteraction
from main.flows.flows import EndTurnEvent, BeginTurnEvent

class Actions:
    def __init__(self, rules):
        self.rules = rules
        self.bottom_handlers = {
            Bottom.END_TURN : self.handle_end_turn,
            Bottom.DISCARD : self.handle_discard,
            Bottom.CANCEL : self.handle_cancel,
            Bottom.USE : self.handle_use
        }
        self.action_handlers = {
            Action.Type.BOARD : self.handle_board,
            Action.Type.HAND : self.handle_hand,
            Action.Type.ROTATE : self.handle_rotate,
            Action.Type.BOTTOM : self.handle_bottom,
        }
    #############################################################################
    #   Bottoms functions      
    #############################################################################
    def handle_end_turn(self, ctx, action):
        return ActionResult(
            flow_events=[
                EndTurnEvent(),
                BeginTurnEvent(),
            ]
        )

    def handle_cancel(self, ctx, action):
        return ActionResult(
            interaction_state_changes=[ResetInteraction()]
        )

    def handle_use(self, ctx, action):
        return ctx.active_token.execute(ctx, action)

    def handle_discard(self, ctx, action):
        return ActionResult(
            effects=[DiscardActiveTokenEffect()],
            interaction_state_changes=[ResetInteraction()]
        )

    #############################################################################
    #   Handler functions      
    #############################################################################
    def handle_bottom(self, ctx, action):
        name = action[Action.Key.BOTTOM]
        function = self.bottom_handlers.get(name)
        return function(ctx, action)
        
    def handle_rotate(self, ctx, action):
        return ActionResult(
            effects=[
                RotateEffect(
                pos=ctx.selected.unit_position, 
                rotation=action[Action.Key.ROTATION]
                )
            ],
            interaction_state_changes=[ResetInteraction()]
        )

    def handle_board(self, ctx, action):
        pos = action[Action.Key.POS]
        if ctx.board.is_empty(pos):
            return ctx.active_token.execute(ctx, action)
        
        return ctx.board.get_tile(pos).execute(ctx, action)

        
    def handle_hand(self, ctx, action):
        token = ctx.player.hand.get_token(action[Action.Key.SLOT])
        return token.execute(ctx, action)

    def execute_action(self, ctx, action):
        if(action is None):
            return ActionResult()
        
        # print("USER ACTION:", action)
        function = self.action_handlers.get(action[Action.Key.TYPE], None)
        return function(ctx, action)
