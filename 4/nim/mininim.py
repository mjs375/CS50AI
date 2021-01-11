from termcolor import colored

import decimal
import os
import random
import sys
import time


"""
Plays '21' version of 'Nim'. Players take turns removing 1, 2, or 3 sticks from the pile. Person to remove the last stick loses.
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
                    sys.exit(f"{killer} butchered their opponent. Total bloodbath. The soul weeps at such (counting) violence.\n...But they technically win the game.")
                if grab == "random" or grab.lower() == "r":
                    move = random.randrange(1,4)
                print("Please enter a number between 1 & 3.")
        self.dwindle(move)
    #
    def AI_move(self):
        """
        If AI is P2, it has a guaranteed win by always selecting a multiple of four, thus resulting in forcing P1 to choose the last stick.
        If AI is P1, they will attempt to choose a multiple of four, but if unable, they will choose just 1 stick, so as to give human player as much opportunity to make an error and give them back a chance to remove sticks to give them a multiple of four again.
        """
        sticks = self.pile
        #--If human player has the advantage (THEY have the multiple of four), always pick 1 to give them an opportunity to mess up and return the advantage to you:
        if sticks == 4:
            move = 3
        elif sticks % 4 == 0:
            move = 1
        #--Calculate the next multiple of 4 after (less than) the current pile.
        else:
            next = sticks + (4 - sticks % 4) - 4
            move = sticks - next
        #
        #--Apply the actual move:
        self.dwindle(move)
        print(f"The pile has {self.pile} sticks remaining. Pick up 1, 2, or 3 sticks?")
        time.sleep(0.3)
        name = self.players[self.turn]
        print(f"{name} picks up {move} sticks.")
        time.sleep(2.5)

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


def play(n, players, AI):
    """
    Runs the Nim game, using OOP.
    """
    print(n, players)
    #--Create instance of class Game
    game = Game(n)
    #--Assign players:
    game.players[1] = players[0]
    game.players[-1] = players[1]
    #--AI on?
    if AI[0] == True:
        #--which player?
        AI_turn = AI[1]

    #--Game ongoing variable:
    playing = True
    while playing:
        os.system('clear')
        #--Toggle whose turn it is:
        game.turner()
        #--Print the 'board'/which player is up:
        game.print()
        #--Get current player's move OR AI's move
        if AI[0] == True and game.turn == AI_turn:
            move = game.AI_move()
        else:
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


def yes_no(question):
    ask = True
    while ask:
        print(question)
        ans = input("Yes or no?\n>>> ")
        #
        if ans[0].lower() == "y":
            ask = False
            return True
        elif ans[0].lower() == "n":
            ask = False
            return False
        else:
            print("Please answer 'yes' or 'no' only.")



def mechanical_typer(msg):
    for char in msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        x = random.randrange(0,15)
        x /= 100
        time.sleep(x)


def main():
    #--PRINTING THE RULES:
    n = 21
    #--
    msg = f"# Welcome to TWENTY-ONE, a stick-picking-up game.\n#I am a ROBOT entity in charge of ADMINISTERING the game and its rewards and/or PUNISHMENTS FOR LOSING.\n# Ahem.\n# The pile of sticks has {n} sticks to start.\n# Players take turns removing 1, 2 or 3 sticks.\n# The player who removes the last stick wins and the other player LOSES DREADFULLY AND MUST BE DEALT WITH.\n# Get stratergizing!\n"
    mechanical_typer(msg)
    time.sleep(1.5)
    #--PLAYER INPUTS:
    #--Play AI? (or human)
    question = "Play against AI? ('no' for 2-player)"
    AI = yes_no(question)
    #--Player (1)'s name:
    time.sleep(1)
    p1 = input("> Player 1's name: ")
    if AI == False:
        time.sleep(1)
        p2 = input("> Player 2's name: ")
    else:
        robot_names  = ["Experimental Annihilator Entity", "CODENAME ENDER", "David v3.2", "ORDINARY HUMAN", "M0THER", "NimBot", "Robbie"]
        p2 = random.choice(robot_names)
    #--Randomize players as P1/P2:
    shuffle = random.choice([True, False])
    if shuffle == True:
        players = (p1, p2)
        #--(AI mode is on, which player is AI):
        AItuple = (AI, -1)
    else:
        players = (p2, p1)
        AItuple = (AI, 1)
    #--Run the game(s):
    playing = True
    while playing:
        play(n, players, AItuple)
        #--Game over, play again?
        question = "Would you like to play again?"
        again = yes_no(question)
        if again == False:
            playing = False
    #
    sys.exit("Thanks for playing!")



# # # # # # # # # # # # # # # #
                              #
if __name__ == "__main__":    #
    os.system('reset')        #
    main()                    #
                              #
# # # # # # # # # # # # # # # #
