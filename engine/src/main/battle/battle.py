from main.actions.akcje_na_planszy import AkcjeNaPlanszy

class Battle:
    def __init__(self, game):
        self.game = game
        self.actions = game.actions
        self.board = game.board
        self.anp = AkcjeNaPlanszy(self.board)

        self.run()

        self.actions.koniec_tury(game)
        self.actions.poczatek_tury(game)

    def run_initiative(self, inicjatywa):
        self.anp.reset_all()
        self.anp.kwestia_sieciarzy()
        self.anp.boost_all()
        self.anp.aktywacja(inicjatywa)
        self.anp.zdejmij_trupy()

    def run(self):
        for inicjatywa in range(self.board.max_inicjatywa, -1, -1):
            self.run_initiative(inicjatywa)
