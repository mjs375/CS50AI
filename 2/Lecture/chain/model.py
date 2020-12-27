from pomegranate import *

# Define starting probabilities
    #--
start = DiscreteDistribution({
    "sun": 0.5, #50/50 start probability
    "rain": 0.5
})

# Define transition model
transitions = ConditionalProbabilityTable([
    ["sun", "sun", 0.8], #If sunny day0, 80% chance sunny day1
    ["sun", "rain", 0.2], #If sunny day0, 20% chance rainy day1
    ["rain", "sun", 0.3],#...
    ["rain", "rain", 0.7]
], [start])

# Create Markov chain
model = MarkovChain([start, transitions])

# Sample 50 states from chain
print(model.sample(50))
