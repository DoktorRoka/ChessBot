import sys
import time
import pyautogui
import keyboard

sys.path.append("./training")

from training.fen_generator import start_detection, ChessboardPredictor
from stockfish_init import ChessEngine
from training.helper_functions import get_mouse_coords

engine = ChessEngine("./stockfish/stockfish-windows-x86-64-avx2.exe")

previous_fen = None
current_player = 'us'

player_side = str(input('Enter your side (w for white, b for black): '))

print("Enable instruct mode? This mode will show you best moves if you press letter E. It will not play for you.")
instruct_mode = input("Enable: ").strip().lower() == 'y'

get_corners = False

if get_corners:
    print("Click on borders of chessboard (top left, bottom right")
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = get_mouse_coords()
else:
    top_left_x, top_left_y = 509, 219
    bottom_right_x, bottom_right_y = 1349, 1061  # lichess if drag to maximum

# Define the size of a square on the chessboard
square_size = (bottom_right_x - top_left_x) / 8

# Initialize the predictor once
predictor = ChessboardPredictor()

try:

    if instruct_mode:
        print("Instruct mode is active. Press E to scan the chessboard and get best move.")
    else:
        print("Automate mode is active. Destroying enemy.")

    while True:
        if instruct_mode:
            if keyboard.is_pressed("e"):  # Manual mode (press E to scan)
                print("Scanning board...")

                screenshot = pyautogui.screenshot(
                    region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
                screenshot.save("training/screenshot.png")

                new_fen, certainty = start_detection(
                    predictor, filepath="training/screenshot.png", active=player_side, unflip=(player_side == 'b'))

                if certainty < 0.99:
                    print(f"Certainty too low ({certainty * 100:.1f}%), rescanning...")
                    time.sleep(0.5)
                    continue

                if new_fen == previous_fen:
                    print("No changes detected on the board.")
                else:
                    best_move = engine.get_best_move(new_fen)
                    if best_move:
                        print(f"Best move: {best_move}")
                        previous_fen = new_fen
                    else:
                        print("No valid move found.")

                time.sleep(0.5)  # Prevent multiple detections from a single key press

        else:  # Auto Mode (your original script)
            screenshot = pyautogui.screenshot(
                region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
            screenshot.save("training/screenshot.png")

            new_fen, certainty = start_detection(
                predictor, filepath="training/screenshot.png", active=player_side, unflip=(player_side == 'b'))

            if certainty < 0.99:
                print(f"Certainty too low ({certainty * 100:.1f}%), rescanning...")
                continue

            if previous_fen != new_fen:  # Detects board change
                print("The FEN has changed.")

                if current_player == 'us':
                    best_move = engine.get_best_move(new_fen)
                    if best_move is None:
                        print('Best move is none, rescanning...')
                        continue
                    print(best_move)

                    # Convert move to screen coordinates
                    start_square, end_square = best_move[:2], best_move[2:]
                    if player_side == 'w':  # White's perspective
                        start_x, start_y = top_left_x + square_size * (
                                ord(start_square[0]) - ord('a')) + square_size / 2, top_left_y + square_size * (
                                                   8 - int(start_square[1])) + square_size / 2
                        end_x, end_y = top_left_x + square_size * (
                                ord(end_square[0]) - ord('a')) + square_size / 2, top_left_y + square_size * (
                                               8 - int(end_square[1])) + square_size / 2
                    else:  # Black's perspective
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

            time.sleep(0.1)  # Minimum delay

finally:
    predictor.close()

# TODO: clean code to make more readable. OOP!!!