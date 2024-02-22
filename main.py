import sys

sys.path.append("./training")

from training.fen_generator import *
from stockfish_init import ChessEngine
from training.helper_functions import get_mouse_coords
import pyautogui
import time



engine = ChessEngine("./stockfish/stockfish-windows-x86-64-avx2.exe")

previous_fen = None
current_player = 'us'

player_side = str(input('Enter your side: '))

get_corners = False


if get_corners:
    print("Click on borders of chessboard (top left, bottom right")
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = get_mouse_coords()
else:
    top_left_x, top_left_y = 509, 219
    bottom_right_x, bottom_right_y = 1349, 1061  # lichess if drag to maximum

# Define the size of a square on the chessboard
square_size = (bottom_right_x - top_left_x) / 8

predictor = ChessboardPredictor()

tolerance = 0.1  # an analogue to the sanity check

while True:

    screenshot = pyautogui.screenshot(
        region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    screenshot.save("training/screenshot.png")
    # Call start_detection with the screenshot file
    certainty = 0
    while abs(certainty - 100.0):
        if player_side == 'b':
            new_fen, certainty = start_detection(predictor=predictor, filepath="training/screenshot.png", active=player_side, unflip=True)
        else:
            new_fen, certainty = start_detection(predictor=predictor, filepath="training/screenshot.png", active=player_side, unflip=False)
        if previous_fen != new_fen:  # detects changed.
            print("The FEN has changed.")

        if current_player == 'us':
            best_move = engine.get_best_move(new_fen)
            if best_move is None:
                print('Best move is none, rescanning...')
                continue
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
            current_player = 'them'
        elif current_player == 'them':
            if previous_fen == new_fen:
                continue
            else:
                current_player = 'us'

        previous_fen = new_fen
    time.sleep(3)  # do not make it any smaller. ITS A MINIMUM

predictor.close()

# TODO: clean code to make more readable. OOP!!!
