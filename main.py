import sys
sys.path.append("./training")

from training.fen_generator import *

import pyautogui
import time

previous_fen = None

while True:
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Save the screenshot
    screenshot.save("training/screenshot.png")
    # Call start_detection with the screenshot file
    new_fen = start_detection(filepath="training/screenshot.png")
    # If the FEN has changed, print a message
    if previous_fen != new_fen:
        print("The FEN has changed.")
        previous_fen = new_fen
    # Wait for three seconds
    time.sleep(3)
