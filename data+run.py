from simplex_method import *

prices = [-2, -3]

norms = [
    [1, -2],
    [2, -1],
    [-1, 2],
]

limit = [2, 5, 4]

test_simplex = SimplexMethod(norms, limit, prices)
test_simplex.solve()