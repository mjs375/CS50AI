from model import model

# Calculate probability for a given observation
probability = model.probability([["none", "no", "on time", "attend"]])
    #--Our query^^^ ("Will I attend the train meeting given there is no rain, no track maintenance, and the train is on time?")

print(probability)  # => 0.34 !!
