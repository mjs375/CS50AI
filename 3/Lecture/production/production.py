import scipy.optimize

# Objective Function: 50x_1 + 80x_2
    # 2 machines: X1 ($50/hr), X2 ($80/hr)
# Constraint 1: 5x_1 + 2x_2 <= 20
    # X1 costs 5 units of labor per hour; X2 costs 2. Have 20 units of labor to spend.
# Constraint 2: -10x_1 + -12x_2 <= -90
    # X1 produces 10 units/hr; X2 produces 12 units/hr. Company needs at least 90 units (or more).
        # Since we deal with <= (not >=), just multiply by -1 to flip the equation.



result = scipy.optimize.linprog(
    #--1st arg: Cost function: 50x_1 + 80x_2
    [50, 80],  # coefficients to optimize for
    # CONSTRAINTS:
    #--Coefficients for inequalities
    A_ub=[[5, 2], [-10, -12]], # coefficients for upper bound equation(s)
    #--Constraints for inequalities: 20 and -90
    b_ub=[20, -90], # actual bound for above args
)



if result.success:
    print(f"X1: {round(result.x[0], 2)} hours")
    print(f"X2: {round(result.x[1], 2)} hours")
else:
    print("No solution")



""" Optimal solution:
X1: 1.5 hours
X2: 6.25 hours
"""
