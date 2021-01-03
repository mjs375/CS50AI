from constraint import *

#--Create a new problem
problem = Problem()

# Add variables
problem.addVariables(
    ["A", "B", "C", "D", "E", "F", "G"],
    ["Monday", "Tuesday", "Wednesday"]
)

# Add constraints (A class can't be on same day as B, &c.)
CONSTRAINTS = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "E"),
    ("C", "F"),
    ("D", "E"),
    ("E", "F"),
    ("E", "G"),
    ("F", "G")
]
for x, y in CONSTRAINTS:
    #--Classes can't have exams on same days:
    problem.addConstraint(lambda x, y: x != y, (x, y))

# Solve problem
for solution in problem.getSolutions():
    print(solution)
