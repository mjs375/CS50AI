"""
Tic Tac Toe Player
- MJ Spitzer, Dec. _ 2020
- CS50: Intro to Artificial Intelligence w/ Python
"""
from copy import deepcopy
import math
import re

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    #--board: a list of 3 lists, each cell being 'X', 'O', or 'EMPTY'.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #--Flatten the list:
    flat_board = [cell for row in board for cell in row]
    #--Check if Xs/Os are NOT on the board: X goes first:
    Xs, Os = 0, 0
    if X not in flat_board and O not in flat_board:
        return X #--Game start, X goes first.
    for cell in flat_board:
        if 'X' == cell:
            Xs += 1
        elif 'O' == cell:
            Os +=1
        else: # Cell is EMPTY.
            pass
    if Xs > Os:
        return O
    else: # Os >= Xs:
        return X

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #--Create empty set to store current legal available moves.
    moves = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if board[i][j] != "X" and board[i][j] != "O":
                #--Create tuple of [EMPTY] cell:
                move = (i, j)
                #--Add move-tuple to moves-set:
                moves.add(move)
    return moves

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #--Check legal moves:
    legal_moves = actions(board)
    if action not in legal_moves:
        raise Exception("Move is not legal")
    #--Determine whose turn it is:
    mark = player(board)
    #--Create a deepcopy of the board:
    board_copy = deepcopy(board)
    #--Apply the mark to the board_copy:
    board_copy[action[0]][action[1]] = mark
    return board_copy

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    """
    An easier (for horizontal... ) check would be like:
    for i, row in enumerate(board):
        if len(set(row)) == 1 and row[1] != EMPTY:
            # easy!
    """
    #--All Possible win conditions (for either piece)
        #--Notice win conditions ignore a) adversary's pieces and b) your own irrelevant pieces (".")
    wins = [
        "ooo......", #Horizontal win, top
        "...ooo...", #Horizontal win, mid
        "......ooo", #Horizontal win, bottom
        "o...o...o", #Diagonal win, L-R
        "..o.o.o..", #Diagonal win, R-L
        "o..o..o..", #Vertical win, L
        ".o..o..o.", #Vertical win, mid
        "..o..o..o", #Vertical win, R
    ]
    #--Flatten the board to a string:
    fboard = [cell for row in board for cell in row]
    fboard = [x if x != EMPTY else "." for x in fboard]
    fboard = "".join(fboard)
    #--Construct checkboards for X & O:
    X_check = fboard.replace(X,"o").replace(O,".")
    O_check = fboard.replace(O,"o").replace(X,".")
    winner = ""
    for win in wins:
        X_winReg = str(win.replace(".", "[o\.]{1}"))
        O_winReg = str(win.replace(".", "[o\.]{1}"))
        #
        Xwin = re.search(str(X_winReg), str(X_check))
        Owin = re.search(str(O_winReg), str(O_check))
        if Xwin:
            return X
        if Owin:
            return O
    # Tie/game still going:
    return EMPTY









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def terminal(board):
    """
    Returns True if game is over (winner or tie), False otherwise.
    """
    #--Has the game been won?
    check = winner(board)
    if check == X or check == O:
        return True
    #--Check if remaining cells (if not, a tie, game over):
        #--TODO (better): simply call actions(board) and if returned set is empty...
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False # Game goes on!
    return True #--All cells are occupied, it's a tie.


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 for tie. Only called when terminal(board) is True (game over).
    """
    champ = winner(board)
    if champ == X:
        return 1
    elif champ == O:
        return -1
    else: #--Tie:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
