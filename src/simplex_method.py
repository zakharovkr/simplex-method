from help_functions import *
from decimal import Decimal
from time import sleep
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
        print("Сиплекс таблица:")

        for i in self.simplex_table:
            print(*i)

        print("\ndw", *self.dw)
        print("d", *self.d )

        print("\nБазисные переменные: ", end='')
        for i in self.basic_vars:
            print(i+1, end=' ')

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
        # count = 2
        # print("Итерация № 1")
        # self.print_simplex()

        while True:
            delta = self.dw[1:]
            if not any(delta > 0 for delta in self.dw[1:]):
                delta = self.d[1:len(self.c) - len(self.A)]


            lead_element_col = delta.index(max(delta for delta in delta)) + 1
            lead_element_row = min([i for i in range(self.m) if self.simplex_table[i][lead_element_col] > 0],
                                    key=lambda i: self.simplex_table[i][0] / self.simplex_table[i][lead_element_col])

            self.simplex_method(lead_element_row, lead_element_col)

            # print("Итерация №", count)
            # self.print_simplex()
            # count += 1
            # sleep(1)

            if delta == self.d[1:len(self.c) - len(self.A)]:
                break
            # if not any(delta > 0 for delta in self.dw[1:len(self.c) - len(self.A)]):
            #     break

    def simplex_method(self, lead_element_row, lead_element_col):
        lead_element_element = self.simplex_table[lead_element_row][lead_element_col]
        self.simplex_table[lead_element_row] = [Decimal(str(element / lead_element_element))
                                                for element in self.simplex_table[lead_element_row]]

        for i in range(len(self.simplex_table)):
            if i != lead_element_row:
                multiplier = self.simplex_table[i][lead_element_col]
                self.simplex_table[i] = [Decimal(str(self.simplex_table[i][j] - multiplier * self.simplex_table[lead_element_row][j]))
                                         for j in range(len(self.simplex_table[i]))]

        self.basic_vars[lead_element_row] = lead_element_col - 1

        self.d = []
        self.dw = []
        self.delta_calculation()

    def ouput_result(self, round_value):
        print("Y(X*) =", round(self.d[0], round_value))

        n = []
        for i, j in enumerate(self.c):
            if j != 0 and j != 'w':
                n.append(i)
        result = "X* = ("
        for i in n:
            if i in self.basic_vars:
                result += f"X{(i + 1)} = {round(get_col(self.simplex_table, 0)[self.basic_vars.index(i)], round_value)}; "

            else:
                result += f"X{i + 1} = 0; "
        result += ')'
        print(result[:len(result) - len(self.A)] + ")")

    def solve(self, round_value = 2):
        self.add_basis()
        self.init_simplex_table()
        self.delta_calculation()
        self.search_lead_element()
        self.ouput_result(round_value)