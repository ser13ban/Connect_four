import numpy as np
import random
import pygame
import sys
import math
import constants as cns


def generate_board():
    """
    Generates the playing board filled with zeros using the numpy library 

    Parameters
    ----------
    none

    Returns
    --------
    DataFrame:
        A dataframe Wiht n rows and m collums
    """
    board = np.zeros((cns.ROWS, cns.COLUMNS))
    return board


def print_board(board):
    """
    Prints the dataframe to the console

    Parameters
    ----------
    none

    Returns
    --------
    none
    """
    print(board)




def get_human_player_move_from_interface(event):
    """
    Returns the move a human player wants to make

    Parameters
    ----------
    the MOUSECLICK event 

    Returns
    --------
    Integer:
        A integer that repersents the collumn number thtat the player has chosen
    """
    posx = event.pos[0]
    col = int(math.floor(posx / cns.TILE_SIZE))
    return col



def get_player2_column(board, player2, event):
    """
    Returns the move the second player (either human or ai)

    Parameters
    ----------
    board - the playing board
    player2 - the type of the player2 (AI hard, medium or easy)
    event- the MOUSECLICK event

    Returns
    --------
    Integer:
        A integer that repersents the collumn that the ai or the human 2 had made
    """
    if player2 is cns.PLAYER_TWO:
        col = get_human_player_move_from_interface(event)
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
            if row:
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
            if row:
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
    """
    Returns true if the move is valid false otherwise

    Parameters
    ----------
    board - the data frae that keeps the game state
    col - the columbn that was seletcet for a piece drop 

    Returns
    --------
    Boolean:
        A boolean that repersents if that position is avaliable or not
    """
    return board[0][col] == 0


def place_piece(board, row, col, piece):
    """
    Places a piece on the board

    Parameters
    ----------
    board - the datgrame taht holds the game state
    row - the row index
    col - the collum index
    piece - 1 for player 1 two for palyer 2

    Returns
    --------
    none
    """
    board[row][col] = piece


def find_row_for_column(board, col):
    """
    Returns the row for a given collum

    Parameters
    ----------
    board - the dataframe holing the game state
    col - the collumn that was chosen 

    Returns
    --------
    Integer:
        A integer that repersents the first free row for a given collumn
    """
    for row in range(cns.ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row


def check_game_over_for_n(board, piece, n):
    """ 
    Returns whete the state of the game reached the end

    Parameters
    ----------
    board - the dataframe that holds the game state
    piece - the piece for which we check the game over 1 or 2
    n - the number of pieces that needed to be connected in order to have game over

    Returns
    --------
    Boolean:
        A boolean that represents wehter the game is over for that piece
    """
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

    for c in range(cns.COLUMNS - n + 1):
        for r in range(cns.ROWS-n-1):
            count = 0
            for i in range(0, n):
                if board[r+i][c+i] == piece:
                    count += 1
            if count == n:
                return True

    for c in range(cns.COLUMNS-n + 1):
        for r in range(n-1, cns.ROWS):
            count = 0
            for i in range(0, n):
                if board[r-i][c+i] == piece:
                    count += 1
            if count == n:
                return True

    for c in range(cns.COLUMNS-3):
        for r in range(cns.ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

	# Check negatively sloped diaganols
    for c in range(cns.COLUMNS-3):
	    for r in range(3, cns.ROWS):
		    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
			    return True

    return False



def draw_interface(board, screen):
    """
    Displays the board and the pieces to the players

    Parameters
    ----------
    board - the dataframe holding the current game state
    screen - the place where the data will be displayed

    Returns
    --------
    none
    """
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


def game(player2, first_player):
    """
    Holds the game loop, logic and the display of the interface, connects and calls all of the functions

    Parameters
    ----------
    player2 - the type of the opponent
    first_player - which player makes the frist move 

    Returns
    --------
    none
    """
    board = generate_board()
    game_over = False
    turn = first_player

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
                elif turn == 2 and player2 == cns.PLAYER_TWO:
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
                    if is_valid_position(board, col) and row >= 0:
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
                        if(player2 == cns.PLAYER_TWO):
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



def get_args():
    """
    Get and validate the arguments from the console and starts the game accordingly

    Parameters
    ----------
    none

    Returns
    --------
    none
    """
    if len(sys.argv) != 5:
        print("ERR, wrong number of arguments, try to follow: ")
        print("python connect_four.py <tip adversar> <celule_axa_x> <celule_axa_y> <First Player>")
        return

    player2 = sys.argv[1]
    if player2 == "human":
        player2 = cns.PLAYER_TWO
    elif player2 == "computer_easy":
        player2 = cns.AI_EASY
    elif player2 == "computer_medium":
        player2 = cns.AI_MEDIUM
    elif player2 == "computer_hard":
        player2 = cns.AI_HARD
    else:
        print("The oponent can be one of the followings")
        print("human \tcomputer_easy \tcomputer_medium \tcomputer_hard")
        return

    try:
        cns.COLUMNS = int(sys.argv[2])
    except:
        print("ERR, the number of collums must be an integer")
        return

    if(cns.COLUMNS < 4):
        print("The number of collums must be at leat four")
        return

    try:
        cns.ROWS = int(sys.argv[3])
    except:
        print("ERR, the number of rows must be an integer")
        return

    if(cns.ROWS < 4):
        print("The number of rows must be at leat four")
        return

    first_player = sys.argv[4]
    if first_player == "computer":
        first_player = 2
    elif first_player == "human":
        first_player = 1
    else:
        print("The first player can be either human or computer")
        return

    game(player2, first_player)


get_args()