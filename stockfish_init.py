from stockfish import Stockfish


class ChessEngine:
    def __init__(self, stockfish_path):
        self.stockfish = self._initialize_stockfish(stockfish_path)
        # if self.is_fen_valid(board_fen):
        #     self.board = chess.Board(board_fen)
        #     self.stockfish.set_fen_position(self.board.fen())
        # else:
        #     print('Invalid FEN')
        #     self.board = None

    def _initialize_stockfish(self, path):
        stockfish = Stockfish(path)
        stockfish.update_engine_parameters({

            "Threads": 16,
            # The number of threads (processor cores) that the engine will use.
            # Don't use all threads or it will quickly crash

            "Hash": 2048,
            # The size of the hash table in megabytes. Don't set it very high. 2048 will do

            "MultiPV": 1,
            # Determines how many best moves the engine will show in the analysis.
            # This always should be set to 1, because engine always plays for best result

            "Skill Level": 20,
            # The engine's level of play. The higher the value, the stronger the play.
            # 0 - weak, 20 - super strong

            "Move Overhead": 10,
            # The time (in milliseconds) that the engine leaves for processing before making a move.

            "UCI_LimitStrength": False,
            # Limits the strength of the engine to a given Elo level. False to make it strong

            "Ponder": True,
            # whether the engine will analyse during the opponent's move. (AKA Predicting)

            "Contempt": 10,
            # Determines how much the engine prefers a draw over the risk of defeat.
            # (Higher value = more aggressive, negative value = plays for a draw. Zero = plays neutral)
            # Max and min values are: 10, -10

            "Slow Mover": 100,
            # Controls the engine's thinking speed in proportion to the available time.
            # Should be based around the given time, but 100 will do for every type of game

        })
        print(f"playing with this parameters: {stockfish.get_parameters()}")
        return stockfish

    def is_fen_valid(self, fen):
        return self.stockfish.is_fen_valid(fen)

    # def make_move(self):
    #     if self.board is not None:
    #         self.stockfish.set_fen_position(self.board.fen())
    #         current_move = self.stockfish.get_best_move()
    #         print(f'Bot has chosen: {current_move}')
    #         print('Bot is making move')
    #         self.board.push_san(current_move)
    #         self.stockfish.set_fen_position(self.board.fen())
    #         self.print_board()
    #         if self.board.is_check():
    #             print('Check!')
    #         if self.board.is_checkmate():
    #             print('Checkmate!')
    #     else:
    #         print('Cannot make move: Invalid board')
    #
    # def user_move(self, move):
    #     if self.board is not None:
    #         try:
    #             self.board.push_san(move)
    #             self.stockfish.set_fen_position(self.board.fen())
    #             print(f'User has made move: {move}')
    #             self.print_board()
    #             if self.board.is_check():
    #                 print('Check!')
    #             if self.board.is_checkmate():
    #                 print('Checkmate!')
    #         except:
    #             print('Invalid move')
    #     else:
    #         print('Cannot make move: Invalid board')

    def get_best_move(self, fen):
        if self.is_fen_valid(fen):
            self.stockfish.set_fen_position(fen)
            best_move = self.stockfish.get_best_move()
            return best_move
        else:
            print('Invalid fen')
            return None

    def print_board(self):
        print(self.stockfish.get_board_visual())


# if __name__ == "__main__":
#     board_fen = input("Enter a FEN string or press enter for the default position: ")
#     if board_fen == "":
#         board_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#     engine = ChessEngine(stockfish_path="stockfish/stockfish-windows-x86-64-avx2.exe", board_fen=board_fen)
#     if engine.board is not None:
#         user_side = input("Choose your side (white/black): ")
#         engine.print_board()
#         while not engine.board.is_checkmate():
#             if (engine.board.turn == chess.WHITE and user_side == 'white') or (engine.board.turn == chess.BLACK and user_side == 'black'):
#                 user_move = input("Enter your move: ")
#                 engine.user_move(user_move)
#             else:
#                 engine.make_move()

#
# :::::::::::::::::::::::::::::::**++************%*++++++++++**********%#*********%*++%*****#********+++++++++++++#-::*#**+++**##=::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::-****************#*+++++***************%%%********#**=-=*#*****%***************++++++##+++++++++++++**=:::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::*****************#++*******************%%#*******#*+*----=*#****%%******************+++*#********+++++++#+:::::::::::::::::::::::::::
# :::::::::::::::::::::::::=%***************#*********************#%#*#******%+-+=-----=#****%%%********************+*#***********+++++%=:::::::::::::::::::::::::
# ::::::::::::::::::::::::*****************%***************##****#%**#******#=-=*-------=#***%+%#******#*************%%#*************++++#-:::::::::::::::::::::::
# ::::::::::::::::::::::-#****************%***************%#****##+=+*****#+---*---------+#****=%******#%************#%%##*************+++*+::::::::::::::::::::::
# :::::::::::::::::::::=%***************##***************%#****##+=-%****#=---==----------****#-=%******%%************%%%%%%%%#**********+++#:::::::::::::::::::::
# ::::::::::::::::::::=#***************##**************#%%****#*+=-*****#=----*=----------=#**#=-=#*****#%%***********#%%%%%%%%%%#*********++%-:::::::::::::::::::
# :::::::::::::::::::+#***************##*********##***%%%%***%*+=-=#****---===+------=-----+#**=--+%****#%%%*****#*****%%%%%%%%%%%%#********++*=::::::::::::::::::
# ::::::::::::::::::=#***************##*%#******#%***%%%#***#*+=--=****=-====*--------+===--***=--=+#***#%%%%****%%****%%%%%%%%%%%%%%#********+*+:::::::::::::::::
# :::::::::::::::::=%***************#####******#%#**%%%+%**%++=---+***=+=---=+-------------=+#*=---=+#***#%%%#***%%#***%%%%%%%%%%%%%%%%#*******+*+::::::::::::::::
# ::::::::::::::::-#****************%%**%*****#%%**%%%+*#*#*++==*#@@@#+====-==------------===##======+%**%*%%%#**%%%#**%%%%%%%%%%%%%%%%%%*******+**:::::::::::::::
# ::::::::::::::::%****************%#*%%%****#%%%*%%%+=**%**%@%*=::::::=#=-----------------=#%%#***#@@@%#%*#%%%**%%%%**%%%%%%%%%%%%%%%%%%%#******+*=::::::::::::::
# :::::::::::::::*****************%#%%%%%***#%%%##%%+=-*##@@+::=%@@@@@@=:-------------------::=*##*+-:-#@@*+#%%##%%%%#*%%%%%%%%%%%%%%%%%%%%%******+#=:::::::::::::
# ::::::::::::::=#***************#%%%%%%%***%%%%%%%+=--*@@*::-=::#@@@@@@*:-----------------:=@@@@@@@@%:::#@#*%%%%%%%%%*%%@%%%%%%%%%%%%%%%%%%%#*****+#-::::::::::::
# ::::::::::::::#***************#%%%%%%%%**%%%%%%%*+---#@=::=*::::@@@@@@@-:---------------:=+:::#@@@@@@=::=@%#%%%%%%%%%%%%@%%%%%%%%%%%%%%%%%%%#*****+*::::::::::::
# :::::::::::::=%*************#%%%%%%%%%%**%%%%%%**=--=@+:::@@#-=%@@@@@@@+:----------------%*::-%@@@@@@@-::+@*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%******+:::::::::::
# :::::::::::::#*************%%%%%%%%%%%%*#%*%%%%++=--#%:::+@@@@@@@@@@@@@*:--------------:=@@+*@@@@@@@@@*:::%@*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%****+#-::::::::::
# ::::::::::::-#***********#%%%%%%%%%%%%%*%#*%%%#*+=--@*:::#@@@@@@@@@@@@@*:--------------:#@@@@@@@@@@@@@%:::*@*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*****=::::::::::
# ::::::::::::=#**********#%%%%%%%%%%%%%%#%+=*%#++**--@*:::#@@%%%@@@@@%@@+---------------:%@@%%@@@@@%@@@%:::*@+%%%%#%%%%=#%%%%%%%%%%%%%%%%%%%%%%%%%****%::::::::::
# ::::::::::::***********%%%%%%%%%%%%%%%%%+=++#*+++*--#@:::+@@%%%@@%+=*@@=---------------:%@@%%@@@@%%%@@*:::%@+*%%%*%%%%*=%%%%%%%%%%%%%%%%%%%%%%%%%#***#=:::::::::
# ::::::::::::#*********%%%%%%%%%%%%%%%%:*==+++++++*--=%#:::%@::=%#-:::%%----------------:#@%*%%%*::=%@@:::=@#++%%%+%%%**-%%%%%%%%%%%%%%%%%%%%%%%%%%#***#:::::::::
# ::::::::::::%********%%%%%%%%%%%%%%%-::==-=+++++**------:::%#*%%%*::*@=-----------------=%::-##::::%@=::=++++*%%*+%%%*+-*=%%%%%%%%%%%%%%%%%%%%%%%%%***#-::::::::
# ::::::::::::%******#%%%%%%%%%%%%%%=:::::*--=+++*+*-------:::+@@@@@@@%--------------------#@@@@%*==#%-::---=++*#%++%%*=-+=::+%%%%%%%%%%%%%%%%%%%%%%%%**#-::::::::
# ::::::::::::%******%%%%%%%%%%%%%=:::::::==--=++***---------=*#*=-------------------------=+#%%%@@@=:------=+****++%*=-=+:::::+%%%%%%%%%%%%%%%%%%%%%%#*#=::::::::
# ::::::::::::#*****%%%%%%%%%%%%=::::::::::*=---=++#=-----------------------------------------------==------++*+**+++=--*::::::::-%%%%%%%%%%%%%%%%%%%%%*#=::::::::
# ::::::::::::*****%%%%%%%%%%#-:::::::::::::==----=+=-------------------------------------------------------++**+++==-==:::::::::::-*%%%%%%%%%%%%%%%%%%*#=::::::::
# ::::::::::::=#**#%%%%%%%%+:::::::::::::::::-*=----+-------------------------------------------------------+*+++==-=*-:::::::::::::::-*%%%%%%%%%%%%%%%##=::::::::
# ::::::::::::=#**%%%%%%*:::::::::::::::::::::::++==+----------------------------=-------------------------=+*+=--=*=:::::::::::::::::::::+%%%%%%%%%%%%##-::::::::
# :::::::::::::#*#%@#=::::::::::::::::::::::::::::::==-----------------------------------------------------=*=--*+::::::::::::::::::::::::::::=#@%%%%%%##:::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::+=---------------------------------------------------=+*+=::::::::::::::::::::::::::::::::::::-=+++-:::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::-+=------------------------------------------------=+*+:::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::=+---------------------------------------------=++*=::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::=*=--------------===============-----------=++**-:::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::-====----------------------------------=+++***=::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::+=:::::====-------------------------==++***+======::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::*--*::::::::::++=------------------==+**+=====+=-::+#=::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::+*=::*=:::::::::::==-+*=-------=+*=+++====+=+=-:::-*=-*::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::****+::++:::::::::::::-++++**++++++======+==-:::::++:+***=::::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::::*******-:-*=::::::::::::==+++++++++-==+===:::::::=*-=*****#-:::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::+***+*****::=*-::::::::::=**+=++++*-==-:::::::::=*--*****+***-::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::-#**********+::=*==****=:::=*******=:::-***=:::+*-=*****+*****+::::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::::***************=:--:==++::::******=::::=+-::=*+-=*****+*******#::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::-*******%#*******=-+***++:::::*****:::::==***=+*****************+:::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::=*******%%**-::+=-=****=:-+**==***-=+**=-=**=--=+::=******%******:::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::***+****%=::++:::=**=-=***+=-:-=*==--=**=++***=:::=*-***#%#***+**:::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::#***#*****=::-*=:::===**********++*****=-==-==:::++:::***#%******-::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::+*******+****:::=*-:::*=---+*****==*****+---*::::*=::-*****%**+***=::::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::::***+**********+:::+*:::-**==*****%%********=:::++:::=*************=::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::-*********+*****#+:::+*--=+****+**%%****=+*==:=*-:::+*****+******+*=::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::=*******+***+*****#*:::+**+=*****#%%******==+*=:::=****+************::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::**************+****#%%*+=+*#**+**%%%**+**++**+::=****+***+**+******#::::::::::::::::::::::::::::::::::::::::::::::
# ::::::::::::::::::::::::::::::::::::::::::::::#****+***+*********#%%%%##*******%%%*****#*+===##*************+*****+:::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::=#******+***+***+**#%%%%%%%#**+***%%%#**+*%%*#%%%#***+**+**+**********-::::::::::::::::::::::::::::::::::::::::::::
# :::::::::::::::::::::::::::::::::::::::::::::****+*********+***#%%%%%%%%%******%#%#****#%%%%%%%%**********+**+*****#::::::::::::::::::::::::::::::::::::::::::::
