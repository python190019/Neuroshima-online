from main.utils.variable import State

class MoveEffect():
    def __init__(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def apply(self, ctx):
        ctx.board.move(self.from_pos, self.to_pos)


class DiscardEffect():
    def __init__(self):
        pass

    def apply(self, ctx):
        ctx.player.hand.discard_active_token()
    
# class ChangeStateEffect():
#     def __init__(self, new_state=State.NO_SELECTION):
#         self.new_state = new_state

#     def apply(self, ctx):
#         ctx.state.state = self.new_state

# class SetSelectedEffect():
#     def __init__(self, new_selected=None):
#         self.new_selected = new_selected or {}
    
#     def apply(self, ctx):
#         ctx.state.selected = self.new_selected

class DamageProfile:
    def __init__(
        self,
        can_hit_hq=True,
        ignore_armor=False
    ):
        self.can_hit_hq = can_hit_hq
        self.ignore_armor = ignore_armor

class DamageEffect():
    def __init__(self, pos, power, profile=None):
        self.pos = pos,
        self.power = power
        self.profile = profile or DamageProfile()
    
    def apply(self, ctx):
        ctx.board.deal_damage_effect(self.pos, self.power, self.profile)

class RotateEffect():
    def __init__(self, pos, rotation):
        self.pos = pos
        self.rotation = rotation
    
    def apply(self, ctx):
        ctx.board.rotate(self.pos, self.rotation)