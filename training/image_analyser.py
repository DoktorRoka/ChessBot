import cv2
import numpy as np


# Define a function to convert the board state to FEN
def board_to_fen(board):
    empty = 0
    fen = ''
    for i in range(8):
        for j in range(8):
            if board[i][j] is None:
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += board[i][j]
        if empty > 0:
            fen += str(empty)
        if i < 7:
            fen += '/'
        empty = 0
    return fen


def detect_pieces(board, pieces, color):
    detections = []
    for piece_name, piece in pieces.items():
        img_piece_clr = cv2.imread(piece, cv2.IMREAD_UNCHANGED)
        img_piece_clr_readable = cv2.cvtColor(img_piece_clr, cv2.COLOR_BGR2GRAY)
        h, w = img_piece_clr_readable.shape
        res = cv2.matchTemplate(img_board_readable, img_piece_clr_readable, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detections.append((pt, piece_name, h, w))

    # Sort detections by y-coordinate
    detections.sort(key=lambda x: x[0][1])

    for pt, piece_name, h, w in detections:
        cv2.rectangle(board, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        # Update the board state
        row = pt[1] // h
        col = pt[0] // w
        if row < 8 and col < 8:
            if color == 'white':
                board_state[row][col] = piece_name[0].upper()
            else:
                board_state[row][col] = piece_name[0].lower()
    return board


# load board and piece images
img_board = cv2.imread('train_data/checker.png')
img_board_readable = cv2.cvtColor(img_board, cv2.COLOR_BGR2GRAY)

pieces_white = {
    'Pawn': 'train_data/usual_chess/white_pawn.png',
    'King': 'train_data/usual_chess/white_king.png',
    'Queen': 'train_data/usual_chess/white_queen.png',
    'Rook': 'train_data/usual_chess/white_rook.png',
    'Bishop': 'train_data/usual_chess/white_bishop.png',
    'Night': 'train_data/usual_chess/white_knight.png'
}

pieces_black = {
    'Pawn': 'train_data/usual_chess/black_pawn.png',
    'King': 'train_data/usual_chess/black_king.png',
    'Queen': 'train_data/usual_chess/black_queen.png',
    'Rook': 'train_data/usual_chess/black_rook.png',
    'Bishop': 'train_data/usual_chess/black_bishop.png',
    'Night': 'train_data/usual_chess/black_knight.png'
}

# Initialize an 8x8 board with None
board_state = [[None for _ in range(8)] for _ in range(8)]

img_board = detect_pieces(img_board, pieces_white, 'white')
img_board = detect_pieces(img_board, pieces_black, 'black')

# Convert the board state to FEN
fen = board_to_fen(board_state)
print(fen)

cv2.imwrite('res.png', img_board)
