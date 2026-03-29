from main import Game
# from plansza import board_
import flask
import json

# ten program uodstepnia 2 funkcje - GET /api/neuroshima/get_board - zwraca aktualny stan planszy w formacie JSON
# POST /api/neuroshima/postaw - przyjmuje dane o żetonie i go stawia

app = flask.Flask(__name__)

# @app.route('/api/neuroshima/get_board', methods=['GET'])
# def get_board():
#     return json.dumps(board_to_json())

@app.route('/api/neuroshima/get_state', methods=['POST'])
def get_state():
    data = flask.request.get_json()
    print(data)
    game = Game(data)
    return json.dumps(game.export_game_state())

@app.route('/api/neuroshima/postaw', methods=['POST'])
def postaw_zeton():
    data = flask.request.get_json()
    print(data)
    game = Game(data)
    # import_data(data)
    zeton = data["zeton"]
    zeton["rany"] = 0
    game.postaw_zeton(zeton)
    # Zeton(pole["x"], pole["y"], pole["frakcja"], pole["nazwa"], pole["rotacja"], pole["rany"])
    # board[data['x']][data['y']] = Zeton(data['x'], data['y'], data['frakcja'], data['nazwa'], data['rotacja'])
    # return json.dumps(board_to_json());
    return json.dumps(game.export_game_state())

# @app.route('/api/neuroshima/click', methods=['POST'])
# def click():
#     data = flask.request.get_json()
#     import_data(data)

# @app.route('/api/neuroshima/bitwa', methods=['POST'])
# def bitwa():

    # for inicjatywa in range(9, -1, -1):
    #     for i in range(5):
    #         for j in range(9):
    #             # print(inicjatywa, i, j)
    #             if board[i][j] is not None:
    #                 board[i][j].aktywuj(inicjatywa)

    #     for i in range(5):
    #         for j in range(9):
    #             if board[i][j] is not None:
    #                 board[i][j].koniec_inicjatywy()
    
    # return json.dumps(game.export_game_state())

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()