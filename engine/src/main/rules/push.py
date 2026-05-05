import main.rules.predicates as pr
from main.state.contex import ActionContext
from main.board.board_query import BoardQuery

class PushRules:

    @staticmethod
    def can_be_pushed(ctx : ActionContext, pusher_pos, target_pos):
        if pr.is_wired_at(ctx, target_pos):
            return False
        if not pr.is_enemy_at(ctx, target_pos):
            return False

        candidates = BoardQuery([
            pr.is_enemy_at,
            pr.adjacent_to(target_pos),
            pr.NOT(pr.adjacent_to(pusher_pos))
        ]).apply(ctx)
        return len(candidates) >= 1
            
    @staticmethod
    def can_push(ctx, pos):
        for hex in ctx.board.adjacent_hexes(pos):
            if PushRules.can_be_pushed(ctx, pos, hex):
                return True
        return False
    
    def get_available_sources(self, ctx : ActionContext):
        candidates = BoardQuery([
            pr.is_ally_at,
            pr.NOT(pr.is_wired_at),
        ]).apply(ctx)
        return [pos for pos in candidates if self.can_push(ctx, pos)]
    
    def get_available_targets(self, ctx : ActionContext):
        pusher_pos = ctx.workflow_data.unit_pos
        candidates = BoardQuery([
            pr.is_enemy_at,
            pr.adjacent_to(pusher_pos),
            pr.NOT(pr.is_wired_at)
        ]).apply(ctx)
        return [pos for pos in candidates 
                if self.can_be_pushed_by(ctx, pusher_pos, pos)]

    def get_available_destinations(self, ctx : ActionContext):
        pusher_pos = ctx.workflow_data.unit_pos
        target_pos = ctx.workflow_data.target_pos
        return BoardQuery([
            pr.is_empty_at,
            pr.adjacent_to(target_pos),
            pr.NOT(pr.adjacent_to(pusher_pos))
        ]).apply(ctx)