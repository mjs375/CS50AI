"""
A Knights & Knaves logic puzzle solver. The puzzles themselves are hard-coded into the program.

Rules:
    - Each character is either a Knight or a Knave.
    - Knights always tell the truth.
    - Knaves always lie.
Based on the KB of each problem, what type if each speaker?
"""


from logic import *
import os

# # # Propositional Symbols:
AKnight = Symbol("A is a Knight")    # either
AKnave = Symbol("A is a Knave")      # /or
#
BKnight = Symbol("B is a Knight")    # either
BKnave = Symbol("B is a Knave")      # /or
#
CKnight = Symbol("C is a Knight")    # either
CKnave = Symbol("C is a Knave")      # /or


"""
For each KB, encode the following:
    1. info about the problem itself (i.e. a Knight is truthful, a Knave lies, each character is either/or).
    2. what the characters said.
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Puzzle 0
# A says "I am both a knight and a knave."
    # Solution: (AKnight)
knowledge0 = And(
#--Problem definition:
    Or(AKnight, AKnave), # Either Knight or Knave
    Biconditional(AKnight, Not(AKnave)), # If a knight, not a knave (vice-versa too!)
#--KNOWLEDGE BASE:
    #--if a Knight, both a Knight & a Knave
    Implication(AKnight, And(AKnight, AKnave)),
    #--if a Knave, NOT both a Knight and a Knave
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
    # Solution: (AKnave, BKnight)
knowledge1 = And(
#--Problem definition:
    Or(AKnight, AKnave), # Either Knight or Knave (A)
    Or(BKnight, BKnave), # Either Knight or Knave (B)
    Biconditional(AKnight, Not(AKnave)), # If (A)=knight, (A)!=knave
    Biconditional(BKnight, Not(BKnave)), # If (B)=knight, (B)!=knave
#--KNOWLEDGE BASE:
    #--If what A says is a lie (both knaves), A is a Knave:
    Implication(Not(And(AKnave, BKnave)),AKnave),
    #--If AKnight exists, based on his known lie above, BKnight exists...
    Implication(AKnave,BKnight)
)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
    # Solution: (AKnave, BKnight)
knowledge2 = And(
#--Problem definition:
    Or(AKnight, AKnave), # Either Knight or Knave (A)
    Or(BKnight, BKnave), # Either Knight or Knave (B)
    Biconditional(AKnight, Not(AKnave)), # If (A)=knight, (A)!=knave
    Biconditional(BKnight, Not(BKnave)), # If (B)=knight, (B)!=knave
#--KNOWLEDGE BASE:
    #--If A lies (prove by contradiction), A is a Knave.
    Implication(Not(And(AKnight, BKnight)), AKnave),
    #--If A is truthful, and A/B are both Knights or Knaves, it entails that both are Knaves, and A is a Knave
    Implication(Or(And(AKnave, BKnave),And(AKnight, BKnight)), And(And(AKnave, BKnave),AKnave)),
    #--If B lies (not diff kinds), B is a Knight.
    Implication(Not(And(AKnight, BKnave)), BKnight),
    #--If B is truthful
    Implication(And(AKnave, BKnight), And(And(AKnave, BKnight),BKnight))



)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
#--Problem definition:
    Or(AKnight, AKnave), # Either Knight or Knave (A)
    Or(BKnight, BKnave), # Either Knight or Knave (B)
    Or(CKnight, CKnave), # Either Knight or Knave (C)
    Biconditional(AKnight, Not(AKnave)), # If (A)=knight, (A)!=knave
    Biconditional(BKnight, Not(BKnave)), # If (B)=knight, (B)!=knave
    Biconditional(CKnight, Not(CKnave)), # If (C)=knight, (C)!=knave
#--KNOWLEDGE BASE:
    #--If C is honest, then A is a Knight and C is a Knight:
    Implication(AKnight,
        And(AKnight, CKnight)),
    #--If C is dishonest, then C is a Knave and A is not a Knight: (some redundancy)...
    Implication(Not(AKnight),
        And(Not(AKnight), CKnave)),
    #--If B is honest, then C is a Knave, and B is a Knight:
    Implication(CKnave,
        And(CKnave, BKnight)),
    #--If B is dishonest, then C is a Knight and B is a Knave: (ditto)...
    Implication(Not(CKnave),
        And(Not(CKnave), BKnave)),
    #--If b is honest, And A said I am a knave, then B is a Knight and A is a Knave:
    Implication(And(Implication(AKnave,Not(AKnave)),BKnight),
        And(AKnave, BKnight)),
    #--If A is a Knave, then what he [whatever] he said is false:
    Implication(AKnave,
        Not(Or(AKnight, AKnave)))
)








# # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        #--Print the KB of each puzzle:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            #--Please provide the Knowledge Base(s)!
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    #os.system('reset')
    main()
