from help_functions import *

class SimplexMethod:
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.d = []
        self.dw = []
        self.basic_vars = []
        self.non_basic_vars = []
        self.simplex_table = []
        self.m = len(b)
        self.n = len(c)


        if len(self.A) != len(self.b):
            raise ValueError("А и b должны быть одинакового размера")

        for i in self.b:
            if i < 0:
                raise ValueError("Все коэффициенты должны быть больше 0")

        first_length = len(self.A[0])
        if any(len(row) != first_length for row in self.A[1:]):
            raise ValueError("Не хватает переменных")

    def print_simplex(self):
        print(*self.c, "-> min")
        print("Сиплекс таблица:")

        for i in self.simplex_table:
            print(*i)

        print("dw", *self.dw)
        print("d", *self.d )

        print("Базисные переменные: (индексы)", *self.basic_vars)
        print("\n")

    def add_basis(self):
        self.c += [0] * len(self.A)
        self.c += ['w'] * len(self.A)
        self.A = [row + [0] * i + [-1] + [0] * (len(self.b) - i - 1) for i, row in enumerate(self.A)]
        self.A = [row + [0] * i + [1] + [0] * (len(self.b) - i - 1) for i, row in enumerate(self.A)]

    def init_simplex_table(self):
        self.non_basic_vars = list(range(len(self.c) - len(self.b)))
        self.basic_vars = list(range(len(self.c) - len(self.b), len(self.c)))

        self.simplex_table = self.A

        for i, j in enumerate(self.simplex_table):
            j.insert(0, (self.b[i]))

    def delta_calculation(self):
        basic = []
        for i in self.basic_vars:
            basic.append(self.c[i])
        for i in range(len(self.basic_vars) + len(self.non_basic_vars) + 1):
            if i == 0: a, b = dot_extended(basic, get_col(self.simplex_table, i), 0)
            else: a, b = dot_extended(basic, get_col(self.simplex_table, i), self.c[i - 1])
            self.dw.append(a)
            self.d.append(b)

    def search_lead_element(self):
        while True:
            d = self.d
            lead_element_col = self.dw[1:].index(max(delta for delta in self.dw[1:])) + 1
            lead_element_row = min([i for i in range(self.m) if self.simplex_table[i][lead_element_col] > 0],
                                    key=lambda i: self.simplex_table[i][0] / self.simplex_table[i][lead_element_col])

            self.simplex_method(lead_element_row, lead_element_col)
            if d == self.d:
                break

    def simplex_method(self, lead_element_row, lead_element_col):

        lead_element_element = self.simplex_table[lead_element_row][lead_element_col]
        self.simplex_table[lead_element_row] = [ round(element / lead_element_element, 1)
                                                for element in self.simplex_table[lead_element_row]]

        for i in range(len(self.simplex_table)):
            if i != lead_element_row:
                multiplier = self.simplex_table[i][lead_element_col]
                self.simplex_table[i] = [round(self.simplex_table[i][j] - multiplier * self.simplex_table[lead_element_row][j], 1)
                                         for j in range(len(self.simplex_table[i]))]

        self.basic_vars[lead_element_row] = lead_element_col - 1

        self.d = []
        self.dw = []
        self.delta_calculation()
    def ouput_result(self):
        print("Y(X*) =", round(self.d[0], 2))

        n = []
        for i, j in enumerate(self.c):
            if j != 0 and j != 'w':
                n.append(i)
        for i in n:
            if i in self.basic_vars:
                print(f"X{(i + 1)} = {round(get_col(self.simplex_table, 0)[self.basic_vars.index(i)], 2)}")
            else:
                print(f"X{i + 1} = 0")

    def solve(self):
        self.add_basis()
        self.init_simplex_table()
        self.delta_calculation()
        self.search_lead_element()
        self.ouput_result()