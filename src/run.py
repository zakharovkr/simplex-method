from simplex_method import *

try:
    prices, norms, limit = read_function('../data/data.txt')
    test_simplex = SimplexMethod(norms, limit, prices)
    test_simplex.solve()

except ValueError as e:
    print("Произошла ошибка: ", e)


