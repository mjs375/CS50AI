# Usage: $ python3 parser.py

import nltk
import os
import re
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | VP NP

AdjP -> Adj | Adj AdjP

NP -> N | Det AdjP N | Det N |  AdjP NP | NP PP

PP -> P NP

VP -> V | V NP | V PP | Adv VP | VP Adv
"""





grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))





def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #--Converts sentence-string into LIST of word-strings / periods & commas:
    tokens = nltk.word_tokenize(sentence)
    #--Lowercase the list of tokens:
    #tokens = [word.lower() for word in tokens]
    #--Remove any word that doesn't have at least 1 alphabetic character:
    words = []
    for token in tokens:
        alpha = bool(re.match("(?=.*[a-z])", token.lower()))
        if alpha:
            words.append(token.lower())
    #
    return words






def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase chunk is defined as any subtree of the sentence whose label is "NP" that does not itself contain any other noun phrases as subtrees.

    chonks = []
    for subtree in tree.subtrees():
        if subtree.label() == "N":
            #print(subtree)
            chonks.append(subtree)
    return chonks
"""

    #--Convert tree into ParentedTree instance:
    chunks = []
    tree = nltk.tree.ParentedTree.convert(tree)
    #
    for sub in tree.subtrees():
        #print(sub, "|",sub.label())
        if sub.label() == "N":
            #print(sub, sub.parents())
            chunks.append(sub.parent())
    return chunks




if __name__ == "__main__":
    #os.system('reset')
    main()
