import pomegranate

from collections import Counter

from model import model

def generate_sample():

    # Mapping of random variable name to sample generated
    sample = {}

    # Mapping of distribution to sample generated
    parents = {}

    # Loop over all states, assuming topological order
    for state in model.states:

        # If we have a non-root node, sample conditional on parents
        if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
            sample[state.name] = state.distribution.sample(parent_values=parents)

        # Otherwise, just sample from the distribution alone (e.g. rain has no parent)
        else:
            sample[state.name] = state.distribution.sample()

        # Keep track of the sampled value in the parents mapping
        parents[state.distribution] = sample[state.name]

    # Return generated sample
    return sample

# Rejection sampling
# Compute distribution of Appointment given that train is delayed
N = 10000 # 10000 samples!
data = []
for i in range(N):
    sample = generate_sample()
    #-- if train is delayed, add to data the value of the appt variable:
    if sample["train"] == "delayed":
        data.append(sample["appointment"])
#--Counts all values in a dataset: how many times was the appt made/missed, given that the train was delayed?
print(Counter(data))
