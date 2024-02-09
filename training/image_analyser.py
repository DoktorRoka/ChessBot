import cv2
import numpy as np

# loading pics of board and pieces.
# TODO: make it better
img_board = cv2.imread('train_data/set_1.png')
img_piece_pawn_white = cv2.imread('train_data/white_pawn.png', cv2.IMREAD_UNCHANGED)
img_piece_pawn_black = cv2.imread('train_data/black_pawn.png', cv2.IMREAD_UNCHANGED)

# making it gray scale, probably not needed because they have solid color. Need to change
img_board_readable = cv2.cvtColor(img_board, cv2.COLOR_BGR2GRAY)
img_piece_pawn_white_readable = cv2.cvtColor(img_piece_pawn_white, cv2.COLOR_BGR2GRAY)
img_piece_pawn_black_readable = cv2.cvtColor(img_piece_pawn_black, cv2.COLOR_BGR2GRAY)

# setting bound boxes to our pictures
h_white, w_white = img_piece_pawn_white_readable.shape
h_black, w_black = img_piece_pawn_black_readable.shape

# searching for white pawn
res_white = cv2.matchTemplate(img_board_readable, img_piece_pawn_white_readable, cv2.TM_CCOEFF_NORMED)
threshold_white = 0.8
loc_white = np.where(res_white >= threshold_white)

for pt in zip(*loc_white[::-1]):
    cv2.rectangle(img_board, pt, (pt[0] + w_white, pt[1] + h_white), (0, 0, 255), 2)

# searching for black pawn
res_black = cv2.matchTemplate(img_board_readable, img_piece_pawn_black_readable, cv2.TM_CCOEFF_NORMED)
threshold_black = 0.8
loc_black = np.where(res_black >= threshold_black)

for pt in zip(*loc_black[::-1]):
    cv2.rectangle(img_board, pt, (pt[0] + w_black, pt[1] + h_black), (255, 0, 0), 2)

cv2.imwrite('res.png', img_board)
