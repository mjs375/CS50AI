from termcolor import colored

import os
import sys
import time


"""
Plays '21' version of 'Nim'.
"""


class Game():
    #
    #
    #--Initialize game variables:
    def __init__(self, pile=21):
        #--Number of sticks in single pile:
        self.pile = pile
        #--Whose turn:
        self.turn = -1
        #--Winner (TBD):
        self.winner = None
        self.players = {1:"Player 1", -1:"Player 2"}
    #
    def dwindle(self, num):
        """
        Removes current player's chosen number of sticks from the pile.
        """
        #--Check if acceptable move:
        if self.winner is not None:
            raise Exception("Game already won.")
        elif self.pile < 0 or self.pile < num:
            raise Exception("Invalid number of sticks remaining.")
        #--Update pile
        self.pile -= num
        #--
    #
    def turner(self):
        """Toggles current player. P1 is 1, P2 is -1. P1 plays first."""
        self.turn *= -1
    #
    def move(self):
        print(f"")
        print(f"The pile has {self.pile} sticks remaining. Pick up 1, 2, or 3 sticks?")
        move = 0
        #--Loop until a valid move is entered (1, 2, 3)
        while move == 0:
            grab = input(">>> ")
            if grab.isdigit():
                grab = int(grab)
                if grab < 4 and grab > 0:
                    move = grab
                else:
                    print("Please enter '1', '2', or '3'.")
            else:
                if grab == "slaughter":
                    killer = self.players[self.turn]
                    sys.exit(f"{killer} butchered their opponent. Total bloodbath. The soul weeps at such violence.\nBut they technically win the game.")
                print("Please enter a number between 1 & 3.")
        self.dwindle(move)
    #
    def win(self):
        """
        Check to see if game is won (pile has 0 sticks remaining, aka whoever took the last stick (1).) """
        if self.pile == 0:
            return True
        elif self.pile > 0:
            return False
    #
    def print(self):
        print(f"The pile has {self.pile} sticks remaining.")
        current_player = self.players[self.turn]
        print(f"It's {current_player}'s turn.")


def play(n, players):
    """
    Runs the Nim game, using OOP.
    """
    print(n, players)
    #--Create instance of class Game
    game = Game(n)
    #--Assign players:
    game.players[1] = players[0]
    game.players[-1] = players[1]

    #--Game ongoing variable:
    playing = True
    while playing:
        os.system('clear')
        #--Toggle whose turn it is:
        game.turner()
        #--Print the 'board'/which player is up:
        game.print()
        #--Get current player's move:
        game.move()
        #--Check if a winner:
        check = game.win()
        if check == True:
             #--Other player won if you took last stick:
            game.turner()
            other = game.turn
            winner = game.players[other]
            print(f"{winner} won the game!")
            playing = False


def yes_no():
    ask = True
    while ask:
        ans = input("Yes or no?\n")
        #
        print("?", ans[0])
        print(ans[0].lower, ans[0].lower == "y")
        if ans[0].lower() == "y":
            ask = False
            return True
        elif ans[0].lower() == "n":
            ask = False
            return False
        else:
            print("Please answer 'yes' or 'no' only.")




def main():

    #--Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 mininim.py [pile_size]")
    #--
    n = sys.argv[1]
    if not n.isdigit() and n < 10 and n > 100:
        sys.exit("Please enter a valid game size between 10 and 100.")
    else:
        n = int(n)

    
    p1 = input("> Player 1's name: ")
    p2 = input("> Player 2's name: ")
    players = (p1, p2)



    playing = True
    while playing:
        play(n, players)
        #--
        print("Would you like to play again?")
        again = yes_no()
        if again == False:
            playing = False

    sys.exit("Thanks for playing!")



# # # # # # # # # # # # # # # #
                              #
if __name__ == "__main__":    #
    os.system('reset')        #
    main()                    #
                              #
# # # # # # # # # # # # # # # #
