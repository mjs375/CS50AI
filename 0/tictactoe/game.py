# # # # # # # # # # # # # # # # #
# # # T I C - T A C - T O E # # #
# # # # # # # # # # # # # # # # #

"""
Usage: $ python3 tictactoe.py [num_of_players]
    - [x] Version 1.0: 2-player mode.
    - [x] Version 1.1: Added (dumb) AI 1-player mode, improved efficiency of check_win f(x)
    - [x] Version 1.2: Improved console printout of board. Added 'cheat'. Xs/0s are now emoji
    - [ ] Version TODO: Game isn't called as a Tie until board is full, even if no wins are possible.
"""

import re           # re.search, re.sub
import time         # time.sleep
import sys          # sys.exit, sys.argv
import random       # random.choice
#
players = {1:"💩", -1:"👺"} # dict of turn/players(piece)
AI_moves = ['7','8','9','4','5','6','1','2','3'] # for 1-player




def game_mode(mode):
    if mode == "1" or mode == "2":
        print("mode is good!")
        return mode
    while mode != "1" and mode != "2":
        time.sleep(0.3)
        mode = input("Enter 1 or 2 (player) as game mode: ")
    return mode
#
#
#
# # # Display the gameboard in the console:
def print_board(board):
    time.sleep(0.5)
    #print("", board[:3], "\n", board[3:6], "\n", board[6:])
    print(" ",board[0]," | ", board[1]," | ",board[2])
    print("-------------------")
    print(" ",board[3]," | ", board[4]," | ",board[5])
    print("-------------------")
    print(" ",board[6]," | ", board[7]," | ",board[8])
    time.sleep(0.5)
#
#
#
# # # Which player, which move?
def get_move(player, turn, board, move):
    ### Check if legal move (for re-try):
    if move != "%":
        if move in board and move != "X" and move != "0":
            AI_moves.remove(move) # remove move from AI's next possible moves
            return move
    ### Prompt for move
    move = input(f"What is your move, {player}?\n>>> ")
    ### Check if legal move (first time):
    if move == "r": # player(s) can resign(/call a draw) by declaring 'r' move
        sys.exit(f"Player {player} resigned.")
    if move == "cheat":
        sys.exit(f"Player {player} cheated! They win!")
    if move in board and move != "X" and move != "0":
        AI_moves.remove(move) # remove move from AI's next possible moves
        return move
    else: #re-prompt for move recursively if invalid (until OK)
        time.sleep(0.5)
        print("That move isn't allowed!")
        time.sleep(0.5)
        print_board(board) # print board again
        move = get_move(player, turn, board, move) # recursive until legal move...
        return move
#
#
# # #
def AI_move():
    print("Dumb AI is thinking...")
    time.sleep(0.3)
    move = random.choice(AI_moves)
    AI_moves.remove(move) # remove move from AI's next possible moves
    return move
#
#
#
# # # Draw valid move on the board
def draw_move(move, board, turn):
    ### Which player, X or 0?:
    board = board.replace(move, players.get(turn)) # replace board num with X/0
    return board
#
#
#
# # # Did the latest move score the win?
def win_check(board, turn):
    ### Winning conditions:
    wins = [ # only looking at X OR 0; not the both or blanks
        "ooo......", #Horizontal win, top
        "...ooo...", #Horizontal win, mid
        "......ooo", #Horizontal win, bottom
        "o...o...o", #Diagonal win, L-R
        "..o.o.o..", #Diagonal win, R-L
        "o..o..o..", #Vertical win, L
        ".o..o..o.", #Vertical win, mid
        "..o..o..o", #Vertical win, R
    ]
    ### Only run tests for player who just went:
    piece = players.get(turn) # active player piece (e.g. X)
    other = players.get(turn*-1) # opponent (e.g. 0)
    check = board.replace(piece,"o").replace(other,".")
    check = re.sub("[1-9]", ".", check)
    ### Check each possible win condition against the latest player's 'board':
    win = ""
    for win in wins: # loop over all possible win conditions
        winReg = str(win.replace(".", "[o\.]{1}"))
        checked = re.search(str(winReg), str(check))
        if checked: #checkRegEx:
            return piece

    return ""
#
#
#
# # # Each step in game, looped until game-over:
def game():
    # # # Starting variables:
    turn = -1 # global variable
    board = "789456123"
    # # # # # LOOP:
    for i in range(9):
        ### Show players the current board:
        if i == 0: # first turn
            print_board(board)
        ### Get active player's move:
        turn *= -1 # toggle the turn
        player = players.get(turn)
        if mode == "1" and turn == -1: # AI is
            move = AI_move()
        else:
            move = "%"
            move = get_move(player, turn, board, move)
        ### Edit board:
        board = draw_move(move, board, turn)
        print_board(board)
        time.sleep(0.5)
        ### Check for win conditions:
        winner = win_check(board, turn)
        ### Check for winner:
        if winner == players.get(1) or winner == players.get(-1):
            print(f"The winner is {winner}!")
            sys.exit()
        ### Rinse & Repeat!
    sys.exit("It's a draw!") # All turns over...
#
#
#
#
#
#
#
#
#
#
#
# # # Get game mode:
try:
    mode = game_mode(sys.argv[1])
except:
    mode = ""
    mode = game_mode(mode)
#
#
# # # Start!
mode = mode # global variable

print(f"Game-mode: {mode}-player.")
time.sleep(0.3)
print("Start!")
time.sleep(0.3)


game() #_>--RUN THE GAME--<_#


"""
TESTER:
    $ python3 -m pdb game.py
- Next line of code: press 'n'
- Check full code: press 'l'
- Check variable value: press 'p' + 'variable_name'
"""
