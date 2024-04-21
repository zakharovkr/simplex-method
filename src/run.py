from simplex_method import *


prices, norms, limit = read_function('../data/data.txt')
test_simplex = SimplexMethod(norms, limit, prices)
test_simplex.solve() #solve(3)  округляет до 3 знаков после запятой

# test_simplex.sensitivity_analysis()
test_simplex.analysis()
