# Context-Free Grammar

import nltk # Natural Language Toolkit



# Grammar Rules:
grammar1 = nltk.CFG.fromstring("""
    S -> NP VP

    NP -> D N | N
    VP -> V | V NP

    D -> "the" | "a"
    N -> "she" | "city" | "car"
    V -> "saw" | "walked"
""")



grammar = nltk.CFG.fromstring("""
    S -> NP V

    NP -> N | NP

    A -> "small" | "white"
    N -> "cats" | "trees"
    V -> "climb" | "run"
""")



#--Parse the grammar:
parser = nltk.ChartParser(grammar)

#--Prompts for a sentence, splits up
sentence = input("Sentence: ").split()
#--Try to parse the new sentence:
try:
    for tree in parser.parse(sentence):
        tree.pretty_print()
        tree.draw() #--Draw grammar tree
except ValueError:
    print("No parse tree possible.")
