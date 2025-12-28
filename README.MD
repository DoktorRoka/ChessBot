# Python chess bot
I recommend to switch [ModelTraining branch](https://github.com/DoktorRoka/ChessBot/tree/ModelTraining),
because it contains more instructions and actually shows how model works.

This bot uses image prediction and mathematical equations to interpret the state of a chess game. It then passes this 
information to Stockfish, to determine the best moves.

Short video showcase: https://youtu.be/8K0O75Rlnnk

# Source code installation:
1) Clone the project into your directory.
2) Create virtual environment and activate it
3) Install requirements:
```pip install -r requirements.txt```
4) Run:
  ```python misc/download_stockfish.py```
4.1) (if a new version of stockfish came out, you can change the link in download_stockfish.py to newest, and it will still work fine)
5) Run ```main.py``` and follow the instructions it gives

The ```stockfish_init.py``` file contains necessary functions and settings for interacting with the Stockfish engine.
You can use it to play chess against Stockfish by entering moves via the keyboard (e.g., ```e2e4```).


# How to train your own model and how I trained mine:
Guide how model works and how to train your own model contained here: 
https://github.com/DoktorRoka/ChessBot/tree/ModelTraining