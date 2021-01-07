# Usage: python generate.py structure words [output]
    # $ python3 generate.py data/structure1.txt data/words1.txt

import copy
import os
import sys
# pip3 install Pillow

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        print("\nNode consistency ENFORCED!\n")
        self.ac3()
        print("\nAC3 COMPLETE!\n")
        return self.backtrack(dict())


















# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent (consistent with unary constraints, aka word length).
            => Step 1: each spot [domain] in the crossword can be filled in with any of the possible words in the wordbank right now. Check each spot/domain's length and simply remove all words for that spot if the lengths don't match.

        - self.domains is a dict mapping vars to sets of values: call `self.domains[v].remove(x)` to remove var x from domain of var `v`.

        # for v in self.domains.values():
        # for d, v in self.domains.items():
        """
        #
        #--Loop over each Domain/Variable (blank-space in puzzle):
        for d in self.domains:
            rm = [] #--Don't modify list while iterating

            #--Loop over each possible value for domain (contains ALL words to start):
            for word in self.domains[d]:
                #--If potential word is NOT same length as domain, remove from domain (add):
                if len(word) != d.length:
                    rm.append(word) #--Add value for removal to temp list

            #--Now, modify the actual domain's values:
            for badword in rm:
                #--Remove value from domain 'd's values:
                self.domains[d].remove(badword)
        #
        #
        """ * Update function, no return * """


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #--Gives back intersection pt between x & y (if):
        overlap = self.crossword.overlaps[x,y]
        #--Words to remove from X's domain
        Xrm = set()

        #--If an overlap...
        if overlap:
            for Xword in self.domains[x]:
                #--Get overlapping char in X [i] (eg 's'ix):
                xletter = Xword[overlap[0]]
                #--Get possible Y values [j], can a conflict be avoided?:
                yletters = {Yword[overlap[1]] for Yword in self.domains[y]}
                #--Check if X has no possible matches in Ys, remove if so:
                if xletter not in yletters:
                    Xrm.add(Xword)
        #--Remove words from X's domains:
        if Xrm:
            self.domains[x] -= Xrm
            revised = True
        #
        #
        #
        return revised # T/F is revisions were done....


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        #--Queue all arcs/edges (x/y's) in constraint-satisfaction problem:
        if not arcs:
            #--Make queue from scratch: all neighboring vars (edges/arcs)
            queue = []
            for x in self.domains:
                neighbors = self.crossword.neighbors(x)
                for y in neighbors:
                    queue.append( (x,y) )
        else:
            #--Given arcs/edges
            queue = arcs

        #--While queue non-empty:
        while queue:
            #--(X,Y) = DEQUEUE(queue)
            XY = queue.pop(0) # the arc/edge itself
            x = XY[0]
            y = XY[1]


            #--if REVISE(csp,X,Y):
            if self.revise(x, y):

                #--if size of X.domain == 0: (domain empty, prob can't be solved)
                if not self.domains[x]:
                    return False

                #--for each Z in (X.neighbors - {Y}):
                for z in (self.crossword.neighbors(x) - {y}):
                    #if (z,x) not in queue:
                        #--ENQUEUE(Z,X)
                    queue.append( (z,x) )

        #--Successfully ran and emptied Queue (and didn't fail):
        return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each crossword variable); return False otherwise.
            - assignment is a dict():
                - keys = Variable objects
                - values = strings (words)
        """
        #--Assignment is COMPLETE if each variable is assigned a value (regardless of actual value):
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def consistent(self, assignment):
        """
        Return True if [partial] `assignment` is consistent (i.e., words fit in crossword puzzle without conflicting characters); return False otherwise.
            - all values distinct
            - every value is correct length
            - no conflicts with neighboring variables
        """

        for var, vord in assignment.items():
            #
            #print("var, vord", var, vord)
            #--CHECK if word matches variable length:
            if var.length != len(vord):
                return False
            #
            #
            for yar, yord in assignment.items():
                #--Don't look at itself...
                if var != yar:
                    #--CHECK if dupe words:
                    if vord == yord:
                        return False
                    #
                    #
                    #--Check if no conflicts with neighboring variables (overwritten letters...):
                    overlap = self.crossword.overlaps[var, yar]
                    if overlap:
                        i, j = overlap[0], overlap[1]
                        if vord[i] != yord[j]:
                            return False # e.g. [six] != [e]ight
        #
        #
        #
        return True # assignment is COMPLETE as is


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by the number of values they rule out for neighboring variables. The first value in the list, for example, should be the one that rules out the fewest values among the neighbors of `var`.
        -> LEAST-CONSTRAINING VALUES HEURISTIC


        temp = []
        for var_word in self.domains[var]:
            temp.append(var_word)
        return temp
"""

        #--dict() of words:num to tally choices ruled out (least-constraining values)
        heuristics = { word: 0 for word in self.domains[var] } # { k:v for k in ____ }

        #--If only 1 word possible, no need to get heuristics:
        if len(self.domains[var]) == 1:
            word = self.domains[var].pop()
            return [word]

        #--Get neighbors [domains] of current variable [domain]:
        neighbors = self.crossword.neighbors(var)

        for var_word in self.domains[var]:
            #--Loop neighbor domains:
            for neighbor in neighbors:
                #--Ignore all neighbors already assigned:
                if neighbor not in assignment.keys():
                    #--Get overlapping cell between VAR and neighbor:
                    overlap = self.crossword.overlaps[var, neighbor]
                    i = overlap[0]
                    j = overlap[1]

                    #--Loop thru each word in neighbor's domain:
                    for neigh_word in self.domains[neighbor]:
                        #--Check if a conflict between VAR_word and NEIGH_word: if so, tally +1 (a constraining value):
                        if var_word[i] != neigh_word[j]:
                            heuristics[var_word] += 1
        #--Sort and return a list, low to high (least to most constraining):
        sortedheuristics = sorted((value, key) for (key, value) in heuristics.items())
        ordered = []
        for i in sortedheuristics:
            ordered.append(i[1]) # [1] index is word
        return ordered


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`. Choose the variable with the MINIMUM NUMBER of REMAINING VALUES in its domain. If there is a tie, choose the variable with the highest degree. If there is a tie, any of the tied variables are acceptable return values.

        # # # Random version # # #
        #--Loop all possible variables:
        for var in self.crossword.variables:
            #--Choose one (randomly) to use/try next:
            if var not in assignment:
                #--Return an unassigned variable:
                return var
        """
        # # # MINIMUM REMAINING VALUES Heuristics (most neighbors) version

        #--Get all UNassigned variables (all - assigned):
        unassigned = self.crossword.variables - assignment.keys()
        if len(unassigned) == 1: # if only 1, just return it
            return unassigned.pop() # return first/only set var

        #--Remaining num of values in each unassigned var's domain:
        remainder = { var:len(self.domains[var]) for var in unassigned }

        #--Make a list of tuples, sort by value
        sortedR = [ (val,var) for (var,val) in remainder.items() ]
        sortedR.sort(key=lambda x:x[0])

        ### Choose the one with the least remaining values (or...) ###
        #--If no tie, return var w/ minimum num of remaining values in unassigned:
        if sortedR[0][0] != sortedR[1][0]: # compare tallies
            return sortedR[0][1] # var w/ least remaining values

        #--if tied, return var w/ most degrees(2nd heuristic, most neighbors):
        else:
            tied = []
            tied.append(sortedR[0][1])
            tied.append(sortedR[1][1])
            degrees = { var:0 for var in tied }
            for tie in tied:
                neighbors = self.crossword.neighbors(tie)
                degrees[tie] = len(neighbors)
            #--Turn dict() into list of tuples (tally, variable)
            sortedR = [ (val, var) for (var, val) in degrees.items() ]
            #--Sort to find MOST degrees of the tied vars (rev sort):
            sortedR.sort(key=lambda x:x[0], reverse=True)
            #--Return var w/ least remaining values AND highest degree (most neighbors):
            return sortedR[0][1]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the crossword and return a complete assignment if possible to do so.
        - `assignment` is a mapping from variables (keys) to words (values).
            - If no assignment is possible, return None.
        """

        #--if assignment complete (puzzle done):
        if self.assignment_complete(assignment):
            return assignment #--Solved!

        #--Select Unassigned Variable(ass., csp)
        var = self.select_unassigned_variable(assignment)

        #--Consider all values in variable's domain: return an ordered list of values to try as possible vals...
        for val in self.order_domain_values(var, assignment):
            #--Create a copy of assignment:
            asgn = copy.deepcopy(assignment) # if later fails...

            #--Add {var: val} k-p to dict() since consistent:
            asgn[var] = val

            #--If val consistent with assignment:
            if self.consistent(asgn):


                ##--inferences = Inferences(assignment)
                #pre_inferences = copy.deepcopy(asgn)
                #inference_check = self.ac3()
                ##--if inferences != failure:
                #if inference_check == True:
                    #pass
                    #--inferences are already added to
                    #--the asgn (assignment) ((?))
                    ##--add inferences to assignment


                #--Recursively call backtrack:
                result = self.backtrack(asgn)
                #--If result doesn't fail:
                if result:
                    return result
                #--Remove {var: val} (result was a failure))
                del asgn[var] #redundant with the below...:
                ##--Remove inferences from asgn:
                #asgn = pre_inferences


        #
        #
        #--No satisfying assignment with vars/vals, return Failure:
        return None













# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def main():

    #--Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    #--Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    #--Generate crossword
    crossword = Crossword(structure, words)
    #--
    creator = CrosswordCreator(crossword)
    #--
    #--Solve crossword:
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    os.system('reset')
    main()
