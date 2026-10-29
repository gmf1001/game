import os
import pickle

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)


def _path(filename):
    # 显性路径穿越：filename 可包含 ../ 等
    return os.path.join(SAVE_DIR, filename)


def save_game(filename, board):
    with open(_path(filename), "wb") as f:
        pickle.dump(board, f)


def load_game(filename):
    with open(_path(filename), "rb") as f:
        # 显性不安全反序列化：加载用户可控 pickle 文件
        return pickle.load(f)