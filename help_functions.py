def dot(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2))
def get_col(matrix, i):
    return [row[i] for row in matrix]

def print_simplex(self):
    print(*self.c, "-> min")
    for i, j in zip(self.A, self.b):
        print(*i, "<=", j)

    print(f"Не базисные переменные: (индексы)", *self.non_basic_vars)
    print("Базисные переменные: (индексы)", *self.basic_vars)
    print("Сиплекс таблица:")

    for i in self.simplex_table:
        print(*i)
    print(*self.d, )
    print("\n")