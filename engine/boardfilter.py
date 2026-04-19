
class BoardFilter():
    def __init__(self, positions=None, predicate=None):
        self.positions = positions or []
        self.predicate = predicate or (lambda ctx, hex : True)

    def matches(self, contex, hex):
        if self.positions and hex not in self.positions:
            return False
        return self.predicate(contex, hex)