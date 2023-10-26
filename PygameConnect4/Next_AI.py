import numpy as np
import random
import pygame
import sys
import math

rows = 6  # to customize your own game,
colums = 7  # ''
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
EMPTY = 0


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


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(colums-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(colums):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(colums-3):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(colums-3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def score_position(board, piece):
    # hori scores
    score = 0
    for r in range(rows):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(colums-3):
            window = row_array[c:c+WINDOW_LENGTH]
            if window.count(piece) == 4:
                score = 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # verti scores
    for c in range(colums):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rows - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            if window.count(piece) == 4:
                score = 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    return score
# 34;34


def get_valid_locations(board):
    valid_location = []
    for col in range(colums):
        if is_valid_location(board, col):
            valid_location.append(col)
    return valid_location


def pick_best_score(board, piece):

    valid_location = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_location)
    for col in valid_location:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(colums):
        for r in range(rows):
            pygame.draw.rect(screen, blue, (c*sqauresize, r *
                             sqauresize+sqauresize, sqauresize, sqauresize))
            pygame.draw.circle(screen, black, (int(c*sqauresize+sqauresize/2),
                                               int(r*sqauresize+sqauresize+sqauresize/2)), radius)
    for c in range(colums):
        for r in range(rows):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, red, (int(c*sqauresize+sqauresize/2),
                                                 height - int(r*sqauresize+sqauresize/2)), radius)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, yellow, (int(c*sqauresize+sqauresize/2),
                                                    height - int(r*sqauresize+sqauresize/2)), radius)
            pygame.display.update()


# calls the function and creates the board connecting it to the varialbe board
board = create_baord()

game_over = False
turn = 0

pygame.init()
sqauresize = 100
width = colums * sqauresize
height = rows * sqauresize

size = (width, height)

radius = int(sqauresize/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, sqauresize))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, red, (posx, int(
                    sqauresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, sqauresize))
            # print(event.pos)
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/sqauresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!", 1, red)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    draw_board(board)

    if turn == AI and not game_over:

        col = pick_best_score(board, AI_PIECE)

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!", 1, yellow)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)
            turn += 1
            turn = turn % 2
    if game_over:
        pygame.time.wait(3000)
        # print(turn)
