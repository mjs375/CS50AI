# MINIMAX AI TIC TAC TOE
- Matthew James Spitzer
- CS50: Introduction to Artificial Intelligence with Python

- **Setup:**
   - ```$ pip3 install -r requirements.txt```
- **Run Program:**
  - ```$ python3 runner.py```
    - Plays against AI. (Since Tic-Tac-Toe is a tie given optimal play by both sides, you should never be able to win, though you can lose.)
- **Run TicTacToe tests:**
  - ```$ python3 test.py```
    - *Complete suite of tests for all file functions.*

#### Files
- requirements.txt: *installs pygame*
- runner.py: *code to run the graphical interface for the game (provided with distribution code).*
- **tictactoe.py**: *my minimax AI Tic-Tac-Toe program.*
- **tests.py**: *unittest-ing for the program.*



#### Minimax vs. Minimax + Alpha-Beta Pruning
- ```tictactoeMINIMAX.py``` contains the base, Minimax algorithm.
- ```tictactoe.py``` contains the Alpha-Beta optimized version.
