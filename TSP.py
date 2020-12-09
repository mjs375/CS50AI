# # # TRAVELING SALESMAN PROBLEM # # #
import six
import sys
sys.modules['sklearn.externals.six'] = six
    #^^error in mlrose, above corrects it
import mlrose
import numpy as np

"""
mlrose
    - implements randomization/search algorithms, applying them to optimization problems.
The Traveling Salesman Problem:
    - The goal is to discover the shortest circuit of 'n' cities (nodes), starting & ending in the same city, and visiting each other one only once.
        - solution = vector of 'n' integers, in range 0 to n-1, specifying the order of cities visited.
    - for larger values of 'n', it isn't possible to calculate every possible solution. Instead, use a randomized optimization algorithm!


Define an optimization problem object:
    - TSPOpt() optimization problem class
Problem steps to solution:
    1. Define a fitness function objects
    2. Define an optimization problem object
    3. Select/run randomized optimization algorithm
Fitness function should calc the total length of a given tour.
    - mlrose's predefined TravellingSales() class does this.
TravellingSales() class needs either:
    - all the (x,y) coordinates of the cities, or
    - the distances between each pair of cities for which travel is possible.
"""


""" If we used city-pair distances:
dist_list = [
            (0, 1, 3.16), (0, 2, 4.3), (0, 3, 5.32), ...
            (1, 2, 4.23), (1, 3, 4.32), ...]
#-- where: (city1, city2, distance)

fitness_dists = mlrose.TravellingSales(distance = dist_list)
"""



#--List of city coordinates:
    #-- aka cities [0, 1, 2, 3, 4, 5, 7]
coords_list = [(1, 1), (4, 2), (5, 2), (6, 4),
               (4, 4), (3, 6), (1, 5), (2, 3)]
#--A possible solution could be
    # x = [0, 4, 2, 6, 5, 3, 7, 1] (assuming city 0 is start/end)
#--but this isn't the shortest circuit.



#--Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords = coords_list)



problem_fit = mlrose.TSPOpt(length=8, fitness_fn=fitness_coords, maximize=False)
    #--length of problem: number of cities to visit
    #--maximize: False (this is a minimize problem, shortest dist!)

#--Solve problem using genetic algorithm:
best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)
    # Default settings:
    #-- population size = 200  (pop_size)
    #-- mutation probability = 0.1 (mutation_prob)
    #-- max num attempts per step = 10 (max_attempts)
    #-- no limit on max total num of iterations of algorithm (max_iters)

print(f"The best state found is: {best_state}.")
print(f"The fitness of the best state is: {best_fitness}")
"""
The best state found is: [1 3 4 5 6 7 0 2].
    - the best sequence of cities
The fitness of the best state is: 18.89580466036301
    - the travel path distance (shortest found)
"""


best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob=0.2, max_attempts=100, random_state=2)
print("Another solution found, using an increased attempts/mutation probability:")
print(f"The best state found is: {best_state}.")
print(f"The fitness of the best state is: {best_fitness}")
