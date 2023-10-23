import numpy as np

rows = 6  # to customize your own game,
colums = 7  # ''


def create_baord():  # funcion to create the board
    board = np.zeros((rows, colums))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[rows-1][col] == 0


def get_next_open_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_moce(board, piece):
    # check hori
    for c in range(colums-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # check verti
    for c in range(colums):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # positive slopes
    for c in range(colums-3):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c+1] and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # negatibe slopes
    for c in range(colums-3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r-1][c+1] and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


# calls the function and creates the board connecting it to the varialbe board
board = create_baord()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # Ask for PLayer 1 input
    if turn == 0:
        col = int(input("Player 1 Make your Selection (0-6) "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if winning_moce(board, 1):
                print("Player 1 Wins")
                game_over = True

    # Ask for Player 2 input
    else:
        col = int(input("Player 2 Make your Selection (0-6) "))
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_moce(board, 2):
                print("Player 2 Wins")
                game_over = True
    print_board(board)
    turn += 1
    turn = turn % 20
# 26:55
