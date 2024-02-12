import sys
sys.path.append("./training")

from training.fen_generator import *
from stockfish_init import ChessEngine

import pyautogui
import time


engine = ChessEngine("./stockfish/stockfish-windows-x86-64-avx2.exe")

previous_fen = None

while True:
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Save the screenshot
    screenshot.save("training/screenshot.png")
    # Call start_detection with the screenshot file
    new_fen = start_detection(filepath="training/screenshot.png")
    # If the FEN has changed, print a message
    print(f'STOCKFISH CHECK {new_fen}')
    if previous_fen != new_fen:
        print("The FEN has changed.")
        best_move = engine.get_best_move(new_fen)
        print(best_move)
        previous_fen = new_fen
    # Wait for three seconds
    time.sleep(3)
