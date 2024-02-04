import chess
from stockfish import Stockfish

board = chess.Board()

stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-avx2.exe")

stockfish.update_engine_parameters({
    "Threads": 16,
    "Hash": 2048,
    "MultiPV": 3,
    "Skill Level": 20,
    "Move Overhead": 10000000,
    "UCI_LimitStrength": False,
})

print(board)


print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))

current_move = stockfish.get_best_move()

print(f'I have chosen: {current_move}')

print('Doing move')

board.push_san(current_move)

print(board)