import sys

sys.path.append("./training")

from training.fen_generator import *
from stockfish_init import ChessEngine

import pyautogui
import time


def normalize_fen(fen):
    fen_parts = fen.split(' ')
    rows = fen_parts[0].split('/')
    normalized_rows = [row[::-1] for row in rows[::-1]]
    normalized_fen_parts = ["/".join(normalized_rows)]
    normalized_fen_parts.extend(fen_parts[1:])
    return " ".join(normalized_fen_parts)


engine = ChessEngine("./stockfish/stockfish-windows-x86-64-avx2.exe")

previous_fen = None
current_player = 'w'

player_side = str(input('Enter your side: '))

# Define the coordinates of the chessboard's top-left and bottom-right corners
# top_left_x, top_left_y = 325, 158
# bottom_right_x, bottom_right_y = 1135, 969  # make sure that you pick the right corners
# TODO: make it automatically finds corners

top_left_x, top_left_y = 557, 220
bottom_right_x, bottom_right_y = 1303, 964  # lichess

# Define the size of a square on the chessboard
square_size = (bottom_right_x - top_left_x) / 8

while True:

    screenshot = pyautogui.screenshot(
        region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    screenshot.save("training/screenshot.png")
    # Call start_detection with the screenshot file
    new_fen = start_detection(filepath="training/screenshot.png", active=player_side)
    if player_side == 'b':
        new_fen = normalize_fen(new_fen)
    if previous_fen != new_fen:  # detects changed.
        print("The FEN has changed.")
        if current_player == 'w':
            best_move = engine.get_best_move(new_fen)
            print(best_move)

            # Convert the move to screen coordinates (do not change numbers, they are working for every chessboard)
            start_square, end_square = best_move[:2], best_move[2:]
            if player_side == 'w':  # the numbers below for white side. DO NOT CHANGE
                start_x, start_y = top_left_x + square_size * (
                        ord(start_square[0]) - ord('a')) + square_size / 2, top_left_y + square_size * (
                                           8 - int(start_square[1])) + square_size / 2
                end_x, end_y = top_left_x + square_size * (
                        ord(end_square[0]) - ord('a')) + square_size / 2, top_left_y + square_size * (
                                       8 - int(end_square[1])) + square_size / 2
            else:  # the numbers below for black side. DO NOT CHANGE
                start_x, start_y = top_left_x + square_size * (
                        7 - (ord(start_square[0]) - ord('a'))) + square_size / 2, top_left_y + square_size * (
                                           int(start_square[1]) - 1) + square_size / 2
                end_x, end_y = top_left_x + square_size * (
                        7 - (ord(end_square[0]) - ord('a'))) + square_size / 2, top_left_y + square_size * (
                                       int(end_square[1]) - 1) + square_size / 2

            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragTo(end_x, end_y, button='left')
            current_player = 'b'
        elif current_player == 'b':
            if previous_fen == new_fen:
                continue
            else:
                current_player = 'w'

        previous_fen = new_fen
    time.sleep(0.1)  # do not make it any smaller. ITS A MINIMUM
