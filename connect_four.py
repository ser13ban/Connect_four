import numpy as np
import random
import pygame
import sys
import math
import constants as cns


def generate_board():
    board = np.zeros((cns.ROWS, cns.COLUMNS))
    return board


def print_board(board):
    print(board)


def get_human_player_move():
    col = int(input("Give me the column you want to move on(0-6): "))
    return col


def get_human_player_move_from_interface(event):
    posx = event.pos[0]
    col = int(math.floor(posx / cns.TILE_SIZE))
    return col


def get_human_player2_move_from_interface(event):
    posx = event.pos[0]
    col = int(math.floor(posx / cns.TILE_SIZE))
    return col


def get_player2_column(board, player2, event):
    if player2 is cns.PLAYER_TWO:
        col = get_human_player2_move_from_interface(event)
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
        twos_in_row = []
        for c in range(cns.COLUMNS):
            row = find_row_for_column(board, c)
            board_copy[row][c] = 2
            if check_game_over_for_n(board_copy, 2, 4):
                return c
            if check_game_over_for_n(board_copy, 2, 3):
                threes_in_row.append(c)
            if check_game_over_for_n(board_copy, 2, 2):
                twos_in_row.append(c)
            board_copy[row][c] = 1
            if check_game_over_for_n(board_copy, 1, 4):
                return c

            # if there was no return so far we need to check if we have 3 in a row
            board_copy[row][c] = 0

        if threes_in_row:
            return random.choice(threes_in_row)

        if twos_in_row:
            return random.choice(twos_in_row)

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


def draw_interface(board, screen):
    for c in range(cns.COLUMNS):
        for r in range(cns.ROWS):
            pygame.draw.rect(screen, cns.BLUE, (c * cns.TILE_SIZE,
                             r * cns.TILE_SIZE + cns.TILE_SIZE, cns.TILE_SIZE, cns.TILE_SIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, cns.BLACK, (int(c * cns.TILE_SIZE + cns.TILE_SIZE/2),
                                                       int(r * cns.TILE_SIZE + cns.TILE_SIZE + cns.TILE_SIZE/2)), cns.RADIUS)
            if board[r][c] == 1:
                pygame.draw.circle(screen, cns.RED, (int(c * cns.TILE_SIZE + cns.TILE_SIZE/2),
                                                     int(r * cns.TILE_SIZE + cns.TILE_SIZE + cns.TILE_SIZE/2)), cns.RADIUS)
            if board[r][c] == 2:
                pygame.draw.circle(screen, cns.GREEN, (int(c * cns.TILE_SIZE + cns.TILE_SIZE/2),
                                                       int(r * cns.TILE_SIZE + cns.TILE_SIZE + cns.TILE_SIZE/2)), cns.RADIUS)
    pygame.display.update()


def game(player2):
    board = generate_board()
    game_over = False
    turn = 1

    pygame.init()
    screen_width = cns.COLUMNS * cns.TILE_SIZE
    screen_height = (cns.ROWS+1) * cns.TILE_SIZE
    size = (screen_width, screen_height)

    screen = pygame.display.set_mode(size)
    draw_interface(board, screen)
    winner_font = pygame.font.SysFont("monospace", 75)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, cns.BLACK,
                                 (0, 0, screen_width, cns.TILE_SIZE))
                posx = event.pos[0]
                if turn == 1:
                    pygame.draw.circle(
                        screen, cns.RED, (posx, int(cns.TILE_SIZE/2)), cns.RADIUS)
                else:
                    pygame.draw.circle(
                        screen, cns.GREEN, (posx, int(cns.TILE_SIZE/2)), cns.RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, cns.BLACK,
                                 (0, 0, screen_width, cns.TILE_SIZE))
                # player 1
                if turn == 1:
                    placed_piece = False
                    print("PLayer 1:")
                    col = get_human_player_move_from_interface(event)
                    print("COL ROM PLYER 1: ", col)

                    # make move
                    row = find_row_for_column(board, col)
                    if is_valid_position(board, col):
                        place_piece(board, row, col, 1)
                        placed_piece = True

                    # check to see if this player won
                    if check_game_over_for_n(board, 1, 4):
                        print("Player 1 won")
                        label = winner_font.render(
                            "PLAYER ONE WON!", 1, cns.RED)
                        screen.blit(label, (40, 10))
                        draw_interface(board, screen)
                        draw_interface(board, screen)
                        pygame.time.wait(3000)
                        game_over = True
                        break

                    if placed_piece:
                        turn = 2
                        draw_interface(board, screen)
                        continue

                # player 2
                if turn == 2:
                    placed_piece = False
                    if player2 is cns.PLAYER_TWO:
                        print("PLayer 2:")
                    col = get_player2_column(board, player2, event)
                    print("COL fROM player TWO: ", col)
                    # make move
                    row = find_row_for_column(board, col)
                    if is_valid_position(board, col):
                        place_piece(board, row, col, 2)
                        placed_piece = True

                    # check to see if this player won
                    if check_game_over_for_n(board, 2, 4):
                        print("Player 2 won")
                        label = winner_font.render(
                            "PLAYER TWO WON!", 1, cns.GREEN)
                        screen.blit(label, (40, 10))
                        draw_interface(board, screen)
                        pygame.time.wait(3000)
                        game_over = True
                        break

                    if placed_piece:
                        turn = 1

                print_board(board)
                draw_interface(board, screen)


game(cns.PLAYER_TWO)
