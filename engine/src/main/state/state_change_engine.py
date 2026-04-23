class StateChangeEngine:
    def __init__(self):
        pass

    def process(self, ctx, changes):
        for change in changes:
            change.apply(ctx)