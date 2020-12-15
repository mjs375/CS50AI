import itertools
import random
from copy import deepcopy



class Minesweeper():
    """
    Minesweeper game representation. Handles gameplay.
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height # X (i, )
        self.width = width   # Y (, j)
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines








class Sentence():
    """
    Logical statement about a Minesweeper game.
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        """ Initializes an object-instance of the class Sentence. """
        #--subset of Cells:
        self.cells = set(cells)
        #--Count of how many are mines:
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    #
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        #-- e.g. {E, F, H} = 3  i.e. all cells are mines:
        if self.count == len(self.cells):
            return self.cells
        else: #--we don't know exactly which are mines yet... e.g. {E, F, H} = 2
            return set() #--?
    #
    def known_safes(self):
        """
        Returns the set of all cells in self.cells (specific check-instance) known to be safe.
        """
        # if cell in self.cells: # CHECK!
        #--All cells are known absolutely to be safe:
        if self.count == 0:
            return self.cells
        else: #--we don't know exactly which are safe yet...
            return set() #--?
    #
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that a cell is known to be a mine.
        """
        if cell in self.cells:
            #--Remove known mine from cells subset:
            self.cells.remove(cell)
            #--Subtract 1 mine-count from count so Sentence logic is still correct
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that a cell is known to be safe.
        """
        if cell in self.cells:
            #--Cell is known safe, remove from subset (no count adjust):
            self.cells.remove(cell)
            #--No need to adjust self.count, as self.count only counts MINES













class MinesweeperAI():
    """
    Minesweeper game player, infers moves to make based on Knowledge Base.
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known (100% sure) to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = [] # KNOWLEDGE BASE

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)











    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #--Add cell to moves_made set:
        self.moves_made.add(cell)


        #--Mark cell (the one just chosen now as move) as safe:
        self.mark_safe(cell)


        #--Get touching cells:
        cells = self.get_touching_cells(cell)
        #
        #--Remove neighbors cells which are already known safe/mines:
        mine_tally = count
        already_known = set()
        for cell in cells:
            if cell in self.safes:
                already_known.add(cell)
            if cell in self.mines:
                already_known.add(cell)
                mine_tally -= 1
        #--Remove already_known cells sublist from cells list:
        cells -= already_known


        #--Make a new Sentence object:
        new_knowledge = Sentence(cells, mine_tally)
        #--Add knowledge to KB:
        self.knowledge.append(new_knowledge)


        #--Mark any additional cells as safes/mines, based on KB:
        added_mines = set()
        added_safes = set()
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                added_mines.add(mine)
            for safe in sentence.known_safes():
                added_safes.add(safe)
        for mine in added_mines:
            self.mark_mine(mine) # Mark cell as a mine.
        for safe in added_safes:
            self.mark_safe(safe) # Mark cell as a safe.


        #--Remove any KB sentences that are empty:
        empties = []
        for sentence in self.knowledge:
            if sentence.cells == set():
                empties.append(sentence)
        for empty in empties:
            self.knowledge.remove(empty)


        #--Find new inferences from existing sentences:
        inferences = []
        for sentence in self.knowledge: # loop each sentence in Knowledge Base:
            if len(new_knowledge.cells) > len(sentence.cells):
                set1 = new_knowledge
                subset2 = sentence
            elif len(sentence.cells) > len(new_knowledge.cells):
                set1 = sentence
                subset2 = new_knowledge
            else: #--if equal length, a subset cannot exist...
                break #--break
            if subset2.cells.issubset(set1.cells):
                #-- {A,B,C,D,E}(3) / {A,B,C}(1) => {D,E}(2)
                inf_cell = set(cell for cell in set1.cells if cell not in subset2.cells)
                #----Get the count of the new set (new sentence):
                inf_count = set1.count - subset2.count
                #--Create new inference Sentence instance:
                inference = Sentence(inf_cell, inf_count)
                #--Add to list_to_add_to_KB (outside loop):
                inferences.append(inference)
        #--Add collected inferences (new sentences) to KB:
        for inference in inferences:
            if inference not in self.knowledge:
                self.knowledge.append(inference)

        print("Number of sentences in KB:",len(self.knowledge))
        for sentence in self.knowledge:
            print(sentence.cells, "=", sentence.count)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #










    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("Safe moves:", self.safes)
        for move in self.safes: # self.safes is a set(), so random
            if move not in self.moves_made:
                print("Safe move chosen:", move)
                return move
        return None # if no safe moves available



    def make_random_move(self):
        """ Returns a random move known if no possible safe moves remain (chosen cell *could* be a mine or a safe, not guaranteed). """
        x, y = range(self.height), range(self.width) # Bounds of gameboard (0-7)
        a = itertools.product(x, y) # Make all tuples of possible moves
        total_moves = set(a) # Turn into a set
        random_moves = total_moves.difference(self.moves_made)
        random_moves = list(random_moves.difference(self.mines))
        if not random_moves:
            return None
        else:
            print("Totally random move...")
            return random.choice(random_moves)





    def get_touching_cells(self, cell):
        """
        Returns a set of all neighboring cells for cell (i, j).
        • • •       0,0   0,1  0,2
        • C •       1,0   1,1  1,2
        • • •       2,0   2,1  2,2
                C (i,j)
                i: vertical
                j: horizontal
        """
        #--Info:
        neighbors = set()
        i, j = cell[0], cell[1]
        #
        #--Touching cells above
        if (i - 1 >= 0) and (i < self.height): # TOP neighbor
            neighbors.add( (i-1, j) )
            if (j - 1 >= 0): # TOP-LEFT neighbor
                neighbors.add( (i-1, j-1) )
            if (j + 1 <= self.width - 1): # TOP-RIGHT neighbor
                neighbors.add( (i-1, j+1) )
        #
        #--Touching cells flanking
        if (j - 1 >= 0) and (j < self.width) :
            neighbors.add( (i, j-1) ) # LEFT neighbor
        if (j + 1 <= self.width - 1) and (j < self.width):
            neighbors.add( (i, j+1) ) # RIGHT neighbor
        #
        #--Touching cells below
        if (i + 1 <= self.height - 1) and ( i < self.height): # BOTTOM neighbor
            neighbors.add( (i+1, j) )
            if (j - 1 >= 0): # BOTTOM-LEFT neighbor
                neighbors.add( (i+1, j-1) )
            if (j + 1 <= self.width - 1): # BOTTOM-RIGHT neighbor
                neighbors.add( (i+1, j+1) )
        #
        #
        return neighbors #--a set of touching cells


        def get_neighbors(self, cell):
            """ """
            #--a better, dynamic version of get_touching_cells
            cells = set()
            i, j = cell[0], cell[1]
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    if x <= self.width and y <= self.height and x >= 0 and y >= 0:
                        if (x,y) != (i,j): #--Not the cell itself
                            cells.add((x,y))
            return cells














""" T E S T I N G :

• Test: MinesweeperAI()  .get_touching_cells()
    $ python3
    >>> from minesweeper import *
    >>> demo  = MinesweeperAI()
    >>> cell = (i, j)
    >>> demo.get_touching_cells(cell)
    >>>    [check solution]


"""


#
