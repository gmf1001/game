"""A terminal 2048 game with an intentionally tamperable local high score."""

import json
import random
from pathlib import Path


SIZE = 4
SCORE_FILE = Path(__file__).with_name("highscore.json")


def load_high_score():
    """Load the local high score (intentionally trusted for the security demo)."""
    try:
        data = json.loads(SCORE_FILE.read_text(encoding="utf-8"))
        return int(data.get("high_score", 0))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_high_score(score):
    SCORE_FILE.write_text(
        json.dumps({"high_score": score}, indent=2), encoding="utf-8"
    )


def add_random_tile(board):
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty:
        row, col = random.choice(empty)
        board[row][col] = 4 if random.random() < 0.1 else 2


def slide_row(row):
    values = [value for value in row if value]
    merged = []
    gained = 0
    index = 0
    while index < len(values):
        if index + 1 < len(values) and values[index] == values[index + 1]:
            value = values[index] * 2
            merged.append(value)
            gained += value
            index += 2
        else:
            merged.append(values[index])
            index += 1
    return merged + [0] * (SIZE - len(merged)), gained


def move(board, direction):
    """Move tiles in w/a/s/d direction; return the score gained."""
    gained = 0
    for index in range(SIZE):
        if direction in ("a", "d"):
            row = board[index][:]
            reverse = direction == "d"
            if reverse:
                row.reverse()
            row, row_score = slide_row(row)
            if reverse:
                row.reverse()
            board[index] = row
        else:
            row = [board[row_index][index] for row_index in range(SIZE)]
            reverse = direction == "s"
            if reverse:
                row.reverse()
            row, row_score = slide_row(row)
            if reverse:
                row.reverse()
            for row_index in range(SIZE):
                board[row_index][index] = row[row_index]
        gained += row_score
    return gained


def can_move(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                return True
            if col + 1 < SIZE and board[row][col] == board[row][col + 1]:
                return True
            if row + 1 < SIZE and board[row][col] == board[row + 1][col]:
                return True
    return False


def draw(board, score, high_score):
    print("\n" * 2)
    print("2048  |  分数: {}  |  最高分: {}".format(score, high_score))
    print("+------+------+------+------+")
    for row in board:
        print("|" + "|".join("{:^6}".format(value or "") for value in row) + "|")
        print("+------+------+------+------+")
    print("W/A/S/D 移动，Q 退出")


def play():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_random_tile(board)
    add_random_tile(board)
    score = 0
    high_score = load_high_score()

    while True:
        draw(board, score, high_score)
        if not can_move(board):
            print("游戏结束！最终分数：{}".format(score))
            return

        command = input("> ").strip().lower()
        if command == "q":
            return
        if command not in ("w", "a", "s", "d"):
            continue

        before = [row[:] for row in board]
        score += move(board, command)
        if board != before:
            add_random_tile(board)
        if score > high_score:
            high_score = score
            save_high_score(high_score)


if __name__ == "__main__":
    play()