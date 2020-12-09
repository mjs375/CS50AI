import termcolor

from logic import *

# # # PROPOSITIONAL SYMBOLS:
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]
#
ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]
#
knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]
# # #
symbols = characters + rooms + weapons


def check_knowledge(knowledge):
    for symbol in symbols:
        #--If sure symbol is true:
        if model_check(knowledge, symbol):
            termcolor.cprint(f"{symbol}: YES", "green")
        #--If you don't know for sure symbol is true (or false):
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")

#--START OF GAME:
knowledge = And( #--There must be a person, room, and weapon:
    Or(mustard, plum, scarlet), #--one killer
    Or(ballroom, kitchen, library), #--one crime scene
    Or(knife, revolver, wrench) #--one weapon
)
#--My knowledge base at this point:
# print(knowledge.formula)

#--Some clues are gleaned from gameplay...
knowledge.add(And( #--Initial cards we know are FALSE:
    Not(mustard), Not(kitchen), Not(revolver)
))

# Further gameplay: an unknown card
knowledge.add(Or( #--1 (at minimum) is False
    Not(scarlet), Not(library), Not(wrench)
))

# Further facts gained: known [false] cards
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))

#--Looks over all symbols to draw conclusions about them:
check_knowledge(knowledge)
    #--With the above facts added to the KB, we know that the killer is MsScarlet, in the library, with the knife.
