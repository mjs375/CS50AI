from pomegranate import *

# Observation model for each state
sun = DiscreteDistribution({
    "umbrella": 0.2, # emission probability (if sun, 20% chance of umbrella)
    "no umbrella": 0.8 # 80% chance of umbrella given sun
})

rain = DiscreteDistribution({
    "umbrella": 0.9,
    "no umbrella": 0.1
})

states = [sun, rain]

# Transition model
transitions = numpy.array(
    [[0.8, 0.2], # Tomorrow's predictions if today = sun
     [0.3, 0.7]] # Tomorrow's predictions if today = rain
)

# Starting probabilities (50/50 chance at start)
starts = numpy.array([0.5, 0.5])

# Create the model
model = HiddenMarkovModel.from_matrix(
    transitions, states, starts,
    state_names=["sun", "rain"]
)
model.bake()
