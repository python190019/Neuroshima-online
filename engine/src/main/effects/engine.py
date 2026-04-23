
class EffectEngine():
    def __init__(self):
        pass
    
    def apply(self, ctx, effects):
        for effect in effects:
            effect.apply(ctx)