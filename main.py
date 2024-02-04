import chess
from stockfish import Stockfish


class ChessEngine:
    def __init__(self, stockfish_path, board_fen):
        self.stockfish = self._initialize_stockfish(stockfish_path)
        if self.is_fen_valid(board_fen):
            self.board = chess.Board(board_fen)
        else:
            print('Invalid FEN')
            self.board = None

    def _initialize_stockfish(self, path):
        stockfish = Stockfish(path)
        stockfish.update_engine_parameters({
            "Threads": 16,
            "Hash": 2048,
            "MultiPV": 3,
            "Skill Level": 20,
            "Move Overhead": 10000000,
            "UCI_LimitStrength": False,
        })
        return stockfish

    def is_fen_valid(self, fen):
        return self.stockfish.is_fen_valid(fen)

    def make_move(self):
        if self.board is not None:
            current_move = self.stockfish.get_best_move()
            print(f'I have chosen: {current_move}')
            print('Doing move')
            self.board.push_san(current_move)
            print(self.board)
        else:
            print('Cannot make move: Invalid board')


if __name__ == "__main__":
    board_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    engine = ChessEngine(stockfish_path="stockfish/stockfish-windows-x86-64-avx2.exe", board_fen=board_fen)
    if engine.board is not None:
        print(engine.board)
        engine.make_move()
