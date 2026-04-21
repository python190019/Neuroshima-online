
class EffectEngine():
    def __init__(self):
        self.handlers = {}

    def register(self, effect_type, handler):
        self.handlers[effect_type] = handler

    def apply(self, ctx, effect):
        effect_type = type(effect)
        handler = self.handlers.get(effect_type)
        if handler:
            handler(ctx, effect)