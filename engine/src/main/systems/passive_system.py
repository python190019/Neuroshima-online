from main.systems.sieciarze import Sieciarze

class PassiveSystem():
    def __init__(self, rules):
        self.rules = rules

    def compute(ctx):
        Sieciarze.compute(ctx.board)