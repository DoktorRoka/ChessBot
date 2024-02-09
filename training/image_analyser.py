import cv2
import numpy as np


def detect_pieces(board, pieces):
    for piece in pieces:
        img_piece_clr = cv2.imread(piece, cv2.IMREAD_UNCHANGED)

        img_piece_clr_readable = cv2.cvtColor(img_piece_clr, cv2.COLOR_BGR2GRAY)

        h, w = img_piece_clr_readable.shape

        res = cv2.matchTemplate(img_board_readable, img_piece_clr_readable, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(board, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    return board


# load board and piece images
img_board = cv2.imread('train_data/set_1.png')
img_board_readable = cv2.cvtColor(img_board, cv2.COLOR_BGR2GRAY)

pieces_white = {
    'Pawn': 'train_data/usual_chess/white_pawn.png',
    'King': 'train_data/usual_chess/white_king.png',
    'Queen': 'train_data/usual_chess/white_queen.png',
    'Rook': 'train_data/usual_chess/white_rook.png',
    'Bishop': 'train_data/usual_chess/white_bishop.png',
    'Knight': 'train_data/usual_chess/white_knight.png'
}

pieces_black = {
    'Pawn': 'train_data/usual_chess/black_pawn.png',
    'King': 'train_data/usual_chess/black_king.png',
    'Queen': 'train_data/usual_chess/black_queen.png',
    'Rook': 'train_data/usual_chess/black_rook.png',
    'Bishop': 'train_data/usual_chess/black_bishop.png',
    'Knight': 'train_data/usual_chess/black_knight.png'
}

img_board = detect_pieces(img_board, pieces_white.values())
img_board = detect_pieces(img_board, pieces_black.values())

cv2.imwrite('res.png', img_board)