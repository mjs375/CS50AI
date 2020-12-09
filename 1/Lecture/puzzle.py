from logic import *

#--not yet Propositional Symbols: we need HoraceGryf, HoraceHuff, HoraceRaven, HoraceSly...
people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

#--Propositional Symbols
symbols = []

knowledge = And()

for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

#--Adding our Propositional Symbols:
# Each person belongs to a house.
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))
"""
MinervaGryffindor OR MinervaHufflePuff
OR MinervaSlytherin OR MinervaRavenclaw
"""

#--Only one house per person:
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )

# Only one person per house.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}")))
                    # IF person1 belongs to house1, person2 does NOT belong to house1
                )

# print(knowledge.formula)
# we have 16 variables (Prop Symbols), so this is a HUGE list!


#-- Adding some information/clues to our Knowledge Base:
#--Clue 1: Gilderoy is Gryffindor OR Ravenclaw:
knowledge.add(
    Or(Symbol("GilderoyGryffindor"), Symbol("GilderoyRavenclaw"))
)
#--Clue 2: Pomona is NOT Slytherin
knowledge.add(
    Not(Symbol("PomonaSlytherin"))
)
#--Clue 3: Minerva is in Gryffindor
knowledge.add(
    Symbol("MinervaGryffindor")
)


#--Loop over each symbol
for symbol in symbols:
    #--Checks if knowledge entails that symbol, and if its true...
    if model_check(knowledge, symbol):
        print(symbol)
