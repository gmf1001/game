from flask import Flask, request, jsonify
import game

app = Flask(__name__)


@app.route("/load", methods=["POST"])
def load():
    # 污点源：用户可控 filename
    filename = request.form.get("filename", "default.pkl")

    # 跨文件调用：未校验 filename 就传给 game.load_game
    board = game.load_game(filename)

    return jsonify(board)


@app.route("/save", methods=["POST"])
def save():
    filename = request.form.get("filename", "default.pkl")
    board = request.get_json()
    game.save_game(filename, board)
    return {"ok": True}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)