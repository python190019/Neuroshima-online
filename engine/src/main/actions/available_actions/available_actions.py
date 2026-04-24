from main.utils.variable import State, Selected, Phase, Bottom
from main.board.board_query import BoardQuery
# from main.state.contex import ActionContext
from main.actions.available_actions.available_action_result import AvailableActionResult
from main.actions.available_actions.available_structure import AvailableStructure

class AvailableActions():
    def __init__(self, rules):
        self.rules = rules
        self.available = None
        self.state_handlers = {
            # State.SELECTED_HAND : self.hand_available_actions,
            State.NO_SELECTION : self.default_available_actions,
            # State.MOVING : InstantToken(Token.Type.Instant.MOVE).available_actions,
            State.ROTATE : self.rotate_available_actions,
            # State.PLACING : self.placing_available_actions,
            # State.SELECTED_PUSHer : InstantToken(Token.Type.Instant.PUSH).available_actions,
        }
        
    def default_available_actions(self, ctx):
        if(self.ctx.rules.can_end_turn()):
            return AvailableActionResult(
                bottoms=[Bottom.END_TURN] 
                        if self.rules.can_use_bottom(Bottom.END_TURN)
                        else [],
                        
                hand={
                    fraction : self.rules.get_available_from_hand()
                    for fraction in ctx.state.fractions
                }
            )
        #     self.enable(Bottom.END_TURN)
        
        # self.update_hand_availability(True)

    def rotate_available_actions(self, ctx):
        return AvailableActionResult(
            positions=ctx.selected.unit_position
        )
        # self.update_board_availability([self.state.seleced[Selected.POS]])   
    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def get_available_actions(self, ctx):
        self.available = AvailableStructure.build(ctx)
        token = self.ctx.active_token

        if token:
            actions = token.get_available_actions(ctx, self.rules)

        else:

            function = self.state_handlers.get(ctx.state, None)
            if function:
                actions = function(ctx)

        self.available.apply(actions)
        return self.available.to_dict()