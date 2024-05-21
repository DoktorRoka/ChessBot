# Python chess bot

This bot uses image prediction and mathematical equations to interpret the state of a chess game. It then passes this 
information to Stockfish, to determine the best moves.

# Source code installation:
1) Clone the project into your directory.
2) Create virtual environment and activate it
3) Install requirements:
```pip install -r requirements.txt```
4) Run:
  ```python misc/download_stockfish.py```
5) Run ```main.py``` and follow the instructions it gives

The ```stockfish_init.py``` file contains necessary functions and settings for interacting with the Stockfish engine.
You can use it to play chess against Stockfish by entering moves via the keyboard (e.g., ```e2e4```).

# Installation with gui:
Details on how to install the GUI version of this project will be provided soon.

# How to train your own model and how I trained mine:
Instructions on how to train your own model, as well as details on how I trained mine, will be provided in a separate 
branch. Please stay tuned for updates. I plan to upload this information after finishing school in a week.
