class StateChangesEngine:
    def __init__(self):
        pass

    def apply(self, ctx, changes):
        for change in changes:
            change.apply(ctx)