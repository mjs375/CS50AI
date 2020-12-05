X = "X"
O = "O"
EMPTY = None

board = [[EMPTY, O, EMPTY],
        [X, X, EMPTY],
        [O, EMPTY, X]]

action = (i,j)

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]]
    return board


moves = result(board)
print(moves)
