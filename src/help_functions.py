import sys

def dot_extended(vec1, vec2, c_value):
    d_value = []
    w_value = []
    for i, j in zip(vec1, vec2):
        if i == 'w':
            w_value.append(round(float(j), 1))
        if i != 'w':
            d_value.append(round(float(i * j), 1))

    a = sum(w_value)
    b = sum(d_value)

    if c_value == 'w':
        a-=1
    else:
        b-=c_value
    return a, b

def get_col(matrix, i):
    return [row[i] for row in matrix]

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
