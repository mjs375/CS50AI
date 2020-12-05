import unittest
import os

from tictactoe import player, actions, result, winner, terminal, utility, minimax

""" TESTS for Tic-Tac-Toe AI Game:

- PlayerTestCase: tests for which player's turn it is– player().
- ActionsTestCase: tests for which moves are legal and available– actions().
– ResultTestCase: tests for legal (new board returned) and illegal moves(exception raised).
– WinnerTestCase: TODO

"""



#
# #
#
class CommonTest(unittest.TestCase):
    def setUp(self): #-- setUp runs its code before every single test:
        """ Context for the Player Tests. """
        self.X = "X" # instance attribute
        self.O = "O"
        self.EMPTY = None
    def tearDown(self):
        pass #-- (Runs after every single test...)
    # # #
    def create_board(self, str_board): # NOT a test!
        """ Helper f(x) to create a 3x3 board matrix, accepts a string and returns a list of lists that is var 'board' (e.g. str_board  = "XX..OO..X"). """
        board = []
        c = 0
        for i in range(3):
            board.append([])
            for j in range(3):
                if str_board[c] == ".":
                    board[i].append(self.EMPTY)
                elif str_board[c] == "X":
                    board[i].append(self.X)
                elif str_board[c] == "O":
                    board[i].append(self.O)
                c += 1
        return board





#
# #
#
class PlayerTestCase(CommonTest):
    """ Tests player(board), which determines which player's turn it is currently. """
    #

    # # #
    def test_X_turn(self):
        """Os & Xs have equal marks, X goes."""
        """ board = [[self.X, self.X, self.EMPTY],
                    [self.EMPTY, self.O, self.EMPTY],
                    [self.EMPTY, self.EMPTY, self.O]] """
        board = self.create_board(".XX....OO")
        self.assertEqual(player(board), self.X, "Os and Xs have equal marks, X goes!")
    # # #
    def test_O_turn(self):
        """Xs have 1 more mark, O goes."""
        board = self.create_board("X.X.O....")
        self.assertEqual(player(board), self.O, "X has more marks, O goes!")
    # # #
    def test_game_start(self):
        """No marks at all, X goes first."""
        board = self.create_board(".........")
        self.assertEqual(player(board), self.X, "X should go first!")





#
# #
#
class ActionsTestCase(CommonTest):
    """ Tests actions(board), which determines ALL possible legal moves from the current state and returns a set of tuples representing available board cells (i, j). """
    #
    def test_all_moves_legal(self):
        """ No moves yet made, entire board is open. """
        board = self.create_board(".........")
        self.assertEqual(actions(board),  {(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)}, "Game start, all moves legal (set of 9 tuples).")
    #
    def test_no_legal_moves(self):
        """ Board is full, no legal moves at all. """
        board = self.create_board("XXOOOXXXO")
        self.assertEqual(actions(board), set(), "Gameboard full, no legal moves (empty set).")
    #
    def test_four_legal_moves(self):
        board = self.create_board(".XXOO...X")
        self.assertEqual(actions(board), {(0,0),(1,2),(2,0),(2,1)}, "Four legal moves.")

    #
    def test_seven_legal_moves(self):
        board = self.create_board("..X.....O")
        self.assertEqual(actions(board),{(0,0),(0,1),(1,0),(1,1),(1,2),(2,0),(2,1)}, "Seven legal moves.")



class ResultTestCase(CommonTest):
    """ Applies a legal move to a board and returns consequent board. """
    #
    def test_legal_move(self):
        board = self.create_board(".........")
        action = (0,0)
        self.assertEqual(result(board, action), self.create_board("X........."), "Legal move placed in upper-left corner on empty board.")
    #
    def test_raise_exception(self):
        board = self.create_board("XO.......")
        action = (0,0)
        self.assertRaises(Exception, result, board, action, "Check that Exception is raised when a player attempts to play on an occupied cell.")





class WinnerTestCase(CommonTest):
    def test_X_wins_toprow(self):
        board = self.create_board("XXX...X.O")
        self.assertEqual(winner(board), self.X, "X wins across top row.")
    def test_X_wins_diagonal(self):
        board = self.create_board("X.O.XOX.X")
        self.assertEqual(winner(board), self.X, "X wins diagonal top-left to bottom-right.")
    def test_O_wins_bottomrow(self):
        board = self.create_board("XO.X..OOO")
        self.assertEqual(winner(board), self.O, "X wins across top row.")
    def test_O_wins_diagonal(self):
        pass
    def test_no_winner_yet(self):
        board = self.create_board(".........")
        self.assertEqual(winner(board), self.EMPTY, "New board, no winner yet.")




class TerminalTestCase():
    pass
class UtilityTestCase():
    pass
class MinimaxTestCase():
    pass













#
#
#--Run all the above tests:
if __name__ == "__main__":
    os.system('reset')
    unittest.main()
