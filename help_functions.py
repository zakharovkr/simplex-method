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


def read_function(filename):
    prices = []
    norms = []
    limit = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        prices = list(map(int, lines[1].strip().split()))

        norm_start_index = lines.index("Коэффициенты уравнений\n") + 1
        norm_end_index = lines.index("Коэффициенты ограничений\n")
        for line in lines[norm_start_index: norm_end_index]:
            norm = list(map(int, line.strip().split()))
            if len(norm) != 0: norms.append(norm)
        limit = list(map(int, lines[norm_end_index + 1].strip().split()))

    return prices, norms, limit