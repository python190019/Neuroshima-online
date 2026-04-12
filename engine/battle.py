class Battle:
    def __init__(self, game):
        self.game = game
        self.actions = game.actions
        game.board.bitwa()
        self.actions.koniec_tury(game)
        self.actions.poczatek_tury(game)
        # return True