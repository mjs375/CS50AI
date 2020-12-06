#CS50: Artificial Intelligence with Python
# Matthew James Spitzer
    # Usage: python degrees.py [directory]

import sys
import csv

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {} #--DICT{name:name_id,}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {} #--DICT{person_id:{name:?, birth:?, movies:(1,4,19...)}}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            #--Add person to PEOPLE{...}
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]") # USAGE
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: ")) # First actor's name (function)
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: ")) # Second actor's name
    if target is None:
        sys.exit("Person not found.")

# # # # # #
    path = shortest_path(source, target) #TO DO: write shortest_path function
# # # # # #
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



################################################################################
# 1. Start with person(A)_id.
# 2. Add person(A)_id's set of movies to frontier.
# 3. 1 at a time, get movie(1, 2...)'s set of stars.
# 4. Does movie(1)'s stars match person(B)_id?
    #. if so, return path/degrees of connection
    #. if not, continue adding nodes to frontier and exploring.

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) tuples that connect the source to the target.
       If no possible path, returns None. If multiple shortest paths, return any.
    """
    #--Keep track of how many nodes were explored:
    num_explored = 0

    #--Search algorithm:
    frontier = QueueFrontier() #Breadth-First Search (first-in, first-out)
    #frontier = StackFrontier()

    #--Person (A) is the start [source]. [target] is the goal.
    start_node = Node(state=source, parent=None, action=None)
    frontier.add(start_node)
    #--Set of explored actors (person_ids)
    explored = set()

    #--Loop until we find path from person(A)_id to person(B)_id:
    while True:
        #--Have we run out of frontier? (No solution possible):
        if frontier.empty():
            #raise Exception("None")
            return None

        #--Choose a node from the frontier:
        node = frontier.remove() #BFS pops off first-in, first-out style

        #--Check if the target:
        if node.state == target:
            path = [] # path (solution): list of tuples
            moves = int() # linked movies
            peeps = int() # linked people
            while node.parent is not None: # when None, you're at the original person(A):
                moves = node.action # movie_id
                peeps = node.state # person_id
                node = node.parent
                path.append((moves, peeps)) # Add tuple to list (film, actor)
            #--Reverse the path:
            path.reverse()
            print(f"Nodes explored: {num_explored}")
            return path # SOLUTION!

        #--Put 'spent' node in Explored (not the target/goal):
        explored.add(node.state)
        num_explored += 1

        #--Add neighbors to the frontier
        neighbors = neighbors_for_person(node.state)
        for film, actor in neighbors:
            if not frontier.contains_state(actor) and actor not in explored:
                child = Node(state=actor, parent=node, action=film) # initialize child
                #
                # TODO – MAKE ITS OWN FUNCTION (DRY!)
                # Put in shortcut check: is child.state == target?
                #
                frontier.add(child) # add child-node to frontier


################################################################################



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors



# # # # # # # # # # # # # # #
if __name__ == "__main__":  #
    main()                  #
# # # # # # # # # # # # # # #










"""
    #--Maps a way to look up person_id by name:
Names: {
'kevin bacon': {'102'},
'tom cruise': {'129'},
'cary elwes': {'144'},
'tom hanks': {'158'},
...}

    #--Maps person_id to dict w/: name, birth, movie-set:
People: {
'102': {'name': 'Kevin Bacon', 'birth': '1958', 'movies': {'112384', '104257'}},
'129': {'name': 'Tom Cruise', 'birth': '1962', 'movies': {'95953', '104257'}},
'144': {'name': 'Cary Elwes','birth': '1962', 'movies': {'93779'}},
'158': {'name': 'Tom Hanks', 'birth': '1956', 'movies': {'109830', '112384'}},
...}

    #--Maps movie_id to dict w/: title, movie_id, all stars:
Movies: {
'112384': {'title': 'Apollo 13', 'year': '1995', 'stars': {'641', '158', '102', '200'}},
'104257': {'title': 'A Few Good Men', 'year': '1992', 'stars': {'129', '197', '102', '193'}},
'109830': {'title': 'Forrest Gump', 'year': '1994', 'stars': {'641', '158', '398', '705'}},
...}

"""
