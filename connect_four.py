import numpy as np
import random
import constants as cns


def generate_board():
    board = np.zeros((cns.ROWS, cns.COLUMNS))
    return board


def print_board(board):
    print(board)


def get_human_player_move():
    col = int(input("Give me the column you want to move on(0-6): "))
    return col


def get_player2_column(board, player2):
    if player2 is cns.PLAYER_TWO:
        col = get_human_player_move()
        return col
    elif player2 is cns.AI_EASY:
        # this the ai in random mode (he chooses a piece at random)
        col = random.randint(0, cns.COLUMNS-1)
        return col
    elif player2 is cns.AI_MEDIUM:
        # this is the ai in medium mode ( he knows how to do defence, he attacks randmonly)
        board_copy = board.copy()
        for c in range(cns.COLUMNS):
            row = find_row_for_column(board, c)
            board_copy[row][c] = 1
            if check_game_over(board_copy, row, c, 1):
                return c
        col = random.randint(0, cns.COLUMNS-1)
        return col
    elif player2 is cns.AI_HARD:
        # this is the ai in the hard mode
        # he will go in full defemnce mode and also will chosee the best poition to play based on the score (the biggest array of tiles till in order to get 4 (chooses randomly one of the options if there are more of them))
        pass


def is_valid_position(board, col):
    return board[0][col] == 0


def place_piece(board, row, col, piece):
    board[row][col] = piece


def find_row_for_column(board, col):
    for row in range(cns.ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row


def check_game_over(board, row, col, piece):
    # check horizontaly
    depth_row = cns.ROWS - 3
    depth_col = cns.COLUMNS - 3
    for top in range(row, -1, -1):
        row_top = row - top
        row_bottom = row_top + 3
        if row_top < depth_row:
            count = 0
            for r in range(row_top, row_bottom+1):
                if board[r][col] == piece:
                    count += 1
            if count == 4:
                return True

    # check vertically
    for top in range(col, -1, -1):
        col_top = col - top
        col_bottom = col_top + 3
        if col_bottom <= depth_col:
            count = 0
            for c in range(col_top, col_bottom+1):
                if board[row][c] == piece:
                    count += 1
            if count == 4:
                return True

    # check diagionals
        for c in range(cns.COLUMNS-3):
            for r in range(cns.ROWS-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        for c in range(cns.COLUMNS-3):
            for r in range(3, cns.ROWS):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    return False


def game(player2):
    board = generate_board()
    game_over = False
    turn = 1
    while not game_over:
        # player 1
        if turn == 1:
            placed_piece = False
            print("PLayer 1:")
            col = get_human_player_move()

            # make move
            row = find_row_for_column(board, col)
            if is_valid_position(board, col):
                place_piece(board, row, col, 1)
                placed_piece = True

            # check to see if this player won
            if check_game_over(board, row, col, 1):
                print("Player 1 won")
                game_over = True
                break

            if placed_piece:
                turn = 2

        # player 2
        if turn == 2:
            placed_piece = False
            if player2 is cns.PLAYER_TWO:
                print("PLayer 2:")
            col = get_player2_column(board, player2)

            # make move
            row = find_row_for_column(board, col)
            if is_valid_position(board, col):
                place_piece(board, row, col, 2)
                placed_piece = True

            # check to see if this player won
            if check_game_over(board, row, col, 2):
                print("Player 2 won")
                game_over = True
                break

            if placed_piece:
                turn = 1

        print_board(board)


game(cns.AI_MEDIUM)
