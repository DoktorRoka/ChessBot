import sys
import time
import pyautogui
import keyboard
import cv2
import numpy as np

sys.path.append("./training")

from training.fen_generator import start_detection, ChessboardPredictor
from stockfish_init import ChessEngine
from training.helper_functions import get_mouse_coords

engine = ChessEngine("./stockfish/stockfish-windows-x86-64-avx2.exe")

player_side = str(input('Enter your side (w/b): ')).lower()
get_corners = True

instruct_mode = input("Enable instruct mode?: ").strip().lower() == 'y'
show_arrows = False

if get_corners:
    print("Click on borders of chessboard (top left, bottom right)")
    top_left_x, top_left_y, bottom_right_x, bottom_right_y = get_mouse_coords()
else:
    top_left_x, top_left_y = 509, 219
    bottom_right_x, bottom_right_y = 1349, 1061

square_size = (bottom_right_x - top_left_x) / 8
predictor = ChessboardPredictor()

# Game state variables
previous_fen = None
current_player = 'us'


def calculate_coordinates(move, player_side):
    """Calculate screen coordinates for a move, handling board orientation"""
    start_square, end_square = move[:2], move[2:]

    if player_side == 'w':
        # White perspective (a1 bottom-left)
        start_x = top_left_x + square_size * (ord(start_square[0]) - ord('a')) + square_size / 2
        start_y = top_left_y + square_size * (8 - int(start_square[1])) + square_size / 2
        end_x = top_left_x + square_size * (ord(end_square[0]) - ord('a')) + square_size / 2
        end_y = top_left_y + square_size * (8 - int(end_square[1])) + square_size / 2
    else:
        # Black perspective (a8 top-left)
        start_x = top_left_x + square_size * (7 - (ord(start_square[0]) - ord('a'))) + square_size / 2
        start_y = top_left_y + square_size * (int(start_square[1]) - 1) + square_size / 2
        end_x = top_left_x + square_size * (7 - (ord(end_square[0]) - ord('a'))) + square_size / 2
        end_y = top_left_y + square_size * (int(end_square[1]) - 1) + square_size / 2

    return (start_x, start_y), (end_x, end_y)


def draw_arrow(start, end):
    """Draw semi-transparent arrow that auto-closes properly"""
    try:
        screen = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        overlay = img.copy()

        cv2.arrowedLine(overlay,
                        tuple(map(int, start)),
                        tuple(map(int, end)),
                        (0, 255, 0), 5, tipLength=0.3)

        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        cv2.imshow("Move Suggestion", img)
        cv2.waitKey(800)  # Reduced display time
    finally:
        cv2.destroyAllWindows()


def handle_instruct_mode():
    """Process manual move requests"""
    global previous_fen

    screenshot = pyautogui.screenshot(
        region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    screenshot.save("training/screenshot.png")

    new_fen, certainty = start_detection(
        predictor, "training/screenshot.png",
        active=player_side,
        unflip=(player_side == 'b')
    )

    if certainty < 0.95:
        print(f"Low confidence: {certainty * 100:.1f}%")
        return

    if new_fen == previous_fen:
        print("Position unchanged")
        return

    best_move = engine.get_best_move(new_fen)
    if not best_move:
        print("No valid move found")
        return

    print(f"Best: {best_move} | FEN: {new_fen}")
    start_pos, end_pos = calculate_coordinates(best_move, player_side)

    if show_arrows:
        draw_arrow(start_pos, end_pos)

    previous_fen = new_fen


def handle_auto_mode():
    """Handle automatic move detection and execution"""
    global previous_fen, current_player

    screenshot = pyautogui.screenshot(
        region=(top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y))
    screenshot.save("training/screenshot.png")

    new_fen, certainty = start_detection(
        predictor, "training/screenshot.png",
        active=player_side,
        unflip=(player_side == 'b')
    )

    if certainty < 0.99 or new_fen == previous_fen:
        return

    print(f"New position: {new_fen}")

    if current_player == 'us':
        best_move = engine.get_best_move(new_fen)
        if not best_move:
            return

        start_pos, end_pos = calculate_coordinates(best_move, player_side)

        if show_arrows:
            draw_arrow(start_pos, end_pos)

        pyautogui.moveTo(start_pos)
        pyautogui.dragTo(end_pos, button='left')
        current_player = 'them'
    else:
        current_player = 'us'

    previous_fen = new_fen


try:
    print("Controls:")
    print("T - Toggle auto/instruct modes")
    print("E - Get move suggestion (instruct mode)")
    print("A - Toggle arrows")
    print("Q - Quit")

    while True:
        # Handle control keys
        if keyboard.is_pressed('t'):
            instruct_mode = not instruct_mode
            print(f"\n{'INSTRUCT' if instruct_mode else 'AUTO'} MODE")
            previous_fen = None  # Reset position memory
            time.sleep(0.3)

        if keyboard.is_pressed('a'):
            show_arrows = not show_arrows
            print(f"Arrows {'ON' if show_arrows else 'OFF'}")
            time.sleep(0.3)

        # Main processing
        if instruct_mode:
            if keyboard.is_pressed('e'):
                handle_instruct_mode()
                time.sleep(0.3)  # Debounce
        else:
            handle_auto_mode()
            time.sleep(0.1)  # Original scan interval

        if keyboard.is_pressed('q'):
            print("Exiting...")
            break

finally:
    cv2.destroyAllWindows()
    predictor.close()