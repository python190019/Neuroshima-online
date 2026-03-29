from zeton import Zeton

class Board:
    def __init__(self):
        self.length = 9
        self.width = 5
        self.board = [[None] * self.length for i in range(self.width)]
        
        self.roza = {
            0: [-1, 1],
            1: [0, 2],
            2: [1, 1],
            3: [1, -1],
            4: [0, -2],
            5: [-1, -1]
        }

    def postaw_zeton(self, x, y, zeton):
        self.board[x][y] = Zeton(x, y, zeton["frakcja"], zeton["nazwa"], zeton["rotacja"], zeton["rany"])

    def import_board(self, data):
        for x in range(self.width):
            for y in range(self.length):
                pole = data[x][y]
                if(pole is None):
                    self.board[x][y] = None
                else:
                    self.postaw_zeton(x, y, pole)


    def board_to_json(self):
        json_board = [[None] * self.length for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.length):
                if self.board[i][j] is not None:
                    json_board[i][j] = {
                        "frakcja": self.board[i][j].frakcja,
                        "nazwa": self.board[i][j].nazwa,
                        "rotacja": self.board[i][j].rotacja,
                        "hp": self.board[i][j]["hp"]
                    }
        return json_board