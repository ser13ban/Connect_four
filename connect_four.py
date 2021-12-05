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
            if check_game_over_for_n(board_copy, 1, 4):
                return c
        col = random.randint(0, cns.COLUMNS-1)
        return col
    elif player2 is cns.AI_HARD:
        # this is the ai in the hard mode
        # he will go in full defemnce mode and also will chosee the best poition to play based on the score (the biggest array of tiles till in order to get 4 (chooses randomly one of the options if there are more of them))
        board_copy = board.copy()
        threes_in_row = []
        for c in range(cns.COLUMNS):
            row = find_row_for_column(board, c)
            board_copy[row][c] = 2
            if check_game_over_for_n(board_copy, 2, 4):
                return c
            if check_game_over_for_n(board_copy, 2, 3):
                threes_in_row.append(c)
            board_copy[row][c] = 1
            if check_game_over_for_n(board_copy, 1, 4):
                return c
            # if there was no return so far we need to check if we have 3 in a row
            board_copy[row][c] = 0

        if threes_in_row:
            return random.choice(threes_in_row)

        return random.randint(0, cns.COLUMNS-1)


def is_valid_position(board, col):
    return board[0][col] == 0


def place_piece(board, row, col, piece):
    board[row][col] = piece


def find_row_for_column(board, col):
    for row in range(cns.ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row


def check_game_over_for_n(board, piece, n):
    for c in range(cns.COLUMNS-(n-1)):
        for r in range(cns.ROWS):
            count = 0
            for i in range(0, n):
                if board[r][c+i] == piece:
                    count += 1
            if count == n:
                return True
    for c in range(cns.COLUMNS):
        for r in range(cns.ROWS-(n-1)):
            count = 0
            for i in range(0, n):
                if board[r+i][c] == piece:
                    count += 1
            if count == n:
                return True

    for c in range(cns.COLUMNS - n - 1):
        for r in range(cns.ROWS-n-1):
            count = 0
            for i in range(0, n):
                if board[r+i][c+i] == piece:
                    count += 1
            if count == n:
                return True

    for c in range(cns.COLUMNS-n-1):
        for r in range(n-1, cns.ROWS):
            count = 0
            for i in range(0, n):
                if board[r-i][c+i] == piece:
                    count += 1
            if count == n:
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
            if check_game_over_for_n(board, 1, 4):
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
            if check_game_over_for_n(board, 2, 4):
                print("Player 2 won")
                game_over = True
                break

            if placed_piece:
                turn = 1

        print_board(board)


game(cns.AI_HARD)
