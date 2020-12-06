import unittest
import os

from tictactoe import player, actions, result, winner, terminal, utility, minimax, max_value, min_value

""" TESTS for Tic-Tac-Toe AI Game:

- PlayerTestCase: tests for which player's turn it is– player().
- ActionsTestCase: tests for which moves are legal and available– actions().
– ResultTestCase: tests for legal (new board returned) and illegal moves(exception raised) –result().
– WinnerTestCase: tests who is winner of the game– winner().
- TerminalTestCase: tests whether game is won/tied, or still going– terminal().
- UtilityTestCase: tests game utility output (score)– utility().
– MinimaxTestCase: tests optimal move finder– minimax().


- To run all tests:
    $ python3 test.py

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

#
# #
#
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

#
# #
#
class WinnerTestCase(CommonTest):
    """ Tests winner(), which determines if either player X or player O has any of 8 total winning conditions (OR if the game is still going on/a tie.)"""
    #
    def test_X_wins_toprow(self):
        board = self.create_board("XXX...X.O")
        self.assertEqual(winner(board), self.X, "X wins across top row.")
    #
    def test_X_wins_diagonal(self):
        board = self.create_board("X.O.XOX.X")
        self.assertEqual(winner(board), self.X, "X wins diagonal top-left to bottom-right.")
    #
    def test_O_wins_bottomrow(self):
        board = self.create_board("XO.X..OOO")
        self.assertEqual(winner(board), self.O, "X wins across top row.")
    #
    def test_O_wins_diagonal(self):
        board = self.create_board("X.O.OOO..")
        self.assertEqual(winner(board), self.O, "O wins diagonal bottom-left to top-right.")
    #
    def test_O_wins_vertical_right(self):
        board = self.create_board("..O..O..O")
        self.assertEqual(winner(board), self.O, "O wins vertical right row.")
    #
    def test_no_winner_yet(self):
        board = self.create_board(".........")
        self.assertEqual(winner(board), self.EMPTY, "New board, no winner yet.")

#
# #
#
class TerminalTestCase(CommonTest):
    """ Terminal() checks board and returns a Boolean True if game is over (win/no cells left) or False (if game still in progress). """
    #
    def test_gameover_X_won(self):
        board = self.create_board("XXX.O.O.O")
        self.assertTrue(terminal(board))
    #
    def test_gameover_O_won(self):
        board = self.create_board(".X.OOOX.X")
        self.assertTrue(terminal(board))
    #
    def test_game_start(self):
        board = self.create_board(".........")
        self.assertFalse(terminal(board))
    #
    def test_game_ongoing(self):
        board = self.create_board("X.O.X...O")
        self.assertFalse(terminal(board))
    #
    def test_game_tie(self):
        board = self.create_board("XXOOOXXXO")
        self.assertTrue(terminal(board))

#
# #
#
class UtilityTestCase(CommonTest):
    """ Utility() returns the score of the game: +1 if X won, -1 if O won, and 0 otherwise. """
    #
    def test_X_won(self):
        board = self.create_board("O.O.O.XXX")
        self.assertEqual(utility(board), 1, "X won so utility of game is +1.")
    #
    def test_O_won(self):
        board = self.create_board("X.X.X.OOO")
        self.assertEqual(utility(board), -1, "O won so utility of game is -1.")
    #
    def test_tie_game(self):
        board = self.create_board("XXOOOXXXO")
        self.assertEqual(utility(board), 0, "Tie game so utility of game is 0.")

#
# #
#
class MinimaxTestCase(CommonTest):
    """ Minimax() returns the optimal action for the current player on the board in the form of a tuple (i,j). Various tests to check if AI blocks an adversary's winning move, seizes an opportunity to win immediately, or simply tie and end the game. """
    # Between equally 'valuable' moves, the AI now simply chooses the first one it registers.
    # 'Insta-kill' check was added so that the AI always chooses to win immediately rather than choose another move that results in a win (or tie!) later.
    #
    def test_X_win_move(self):
        board = self.create_board("XX.O.O...")
        self.assertEqual(minimax(board), (0,2), "X should play top-right to immediately win.")
    #
    def test_O_Win_move(self):
        board = self.create_board(".X.X.X.OO")
        self.assertEqual(minimax(board), (2,0), "O should play bottom-left to immediately win.")
    #
    def test_X_blocks_O_win(self):
        board = self.create_board("OO.X...X.")
        self.assertEqual(minimax(board), (0,2), "X should play to block O's next winning move.")
    #
    def test_O_wins_X_cant_sinch(self):
        board = self.create_board("XX.OO..X.")
        self.assertEqual(minimax(board), (1,2), "O plays to win immediately, ignoring X that would win on the next turn (if O hadn't won or otherwise blocked X).")
    #
    def test_tie_game_X_plays_last_move(self):
        board = self.create_board("XOXOXXO.O")
        self.assertEqual(minimax(board), (2,1), "X is last to go, has to play last available cell to simply tie.")




# # # # # # # # # # # # # # # # #
#                               #
#--Run all the above tests:     #
if __name__ == "__main__":      #
    os.system('reset')          #
    unittest.main()             #
#                               #
# # # # # # # # # # # # # # # # #
