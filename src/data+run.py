from simplex_method import *

try:
    prices, norms, limit = read_function('../data/data.txt')
    test_simplex = SimplexMethod(norms, limit, prices)
    test_simplex.solve()

except ValueError as e:
    print("Произошла ошибка:", e)


#https://linprog.com/en/main-simplex-method/result;queryParams=%7B%22n%22:3,%22m%22:2,%22max_min%22:%222%22,%22values%22:%5B%5B%221%22,%22-2%22,%221%22%5D,%5B%222%22,%22-1%22,%220%22%5D,%5B%22-1%22,%222%22,%223%22%5D%5D,%22function%22:%5B%22-2%22,%22-3%22%5D,%22equalSign%22:%5B%222%22,%222%22,%222%22%5D%7D