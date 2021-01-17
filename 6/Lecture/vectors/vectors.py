from scipy.spatial.distance import cosine

import math
import numpy as np

with open("words.txt") as f:
    words = dict()
    for i in range(50000):
        row = next(f).split()
        word = row[0]
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector


def distance(w1, w2):
    return cosine(w1, w2)

#--Closest words to one particular word
def closest_words(embedding):
    distances = {
        w: distance(embedding, words[w])
        for w in words
    }
    return sorted(distances, key=lambda w: distances[w])[:10]

#--THE closest word
def closest_word(embedding):
    return closest_words(embedding)[0]


"""
$ python3
>>> from vectors import *

>>> words["breakfast"]
...
>>> distance(words["book"], words["novel"])
...
>>> words["king"] - words["man"]
    # produces some vector
>>> closest_word( words["king"] - words["man"] + words["woman"] )
    # 'queen' !!!!!!
>>> closest_word(words["paris"] - words["france"] + words["england"])
    # 'london' !!!!!!


"""
