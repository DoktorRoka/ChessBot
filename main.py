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
            self.stockfish.set_fen_position(self.board.fen())
            current_move = self.stockfish.get_best_move()
            print(f'Bot has chosen: {current_move}')
            print('Bot is making move')
            self.board.push_san(current_move)
            self.stockfish.set_fen_position(self.board.fen())
            self.print_board()
        else:
            print('Cannot make move: Invalid board')

    def user_move(self, move):
        if self.board is not None:
            try:
                self.board.push_san(move)
                self.stockfish.set_fen_position(self.board.fen())
                print(f'User has made move: {move}')
                self.print_board()
            except:
                print('Invalid move')
        else:
            print('Cannot make move: Invalid board')

    def print_board(self):
        print(self.stockfish.get_board_visual())


if __name__ == "__main__":
    board_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    engine = ChessEngine(stockfish_path="stockfish/stockfish-windows-x86-64-avx2.exe", board_fen=board_fen)
    if engine.board is not None:
        engine.print_board()
        while not engine.board.is_checkmate():
            engine.make_move()
            user_move = input("Enter your move: ")
            engine.user_move(user_move)
