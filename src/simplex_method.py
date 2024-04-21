from help_functions import *
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

        print(*self.c, end='\n')
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
        self.dw = []
        self.d = []
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
            positive_num = [i for i in range(self.m) if self.simplex_table[i][lead_element_col] > 0]

            if positive_num:
                lead_element_row = min(positive_num,
                                       key=lambda i: self.simplex_table[i][0] / self.simplex_table[i][lead_element_col])
            else:
                print("Система не имеет решений или имеет множество решений")
                return 0

            # lead_element_row = min([i for i in range(self.m) if self.simplex_table[i][lead_element_col] > 0],
            #                         key=lambda i: self.simplex_table[i][0] / self.simplex_table[i][lead_element_col])

            self.simplex_method(lead_element_row, lead_element_col)

            # print("Итерация №", count)
            # self.print_simplex()
            # count += 1

            # sleep(1)

            if delta == self.d[1:len(self.c) - len(self.A)]:
                break

    def simplex_method(self, lead_element_row, lead_element_col):
        lead_element_element = self.simplex_table[lead_element_row][lead_element_col]
        self.simplex_table[lead_element_row] = [element / lead_element_element
                                                for element in self.simplex_table[lead_element_row]]

        for i in range(len(self.simplex_table)):
            if i != lead_element_row:
                multiplier = self.simplex_table[i][lead_element_col]
                self.simplex_table[i] = [self.simplex_table[i][j] - multiplier * self.simplex_table[lead_element_row][j]
                                         for j in range(len(self.simplex_table[i]))]

        self.basic_vars[lead_element_row] = lead_element_col - 1
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
        print(result[:len(result) - len(self.A) + 1] + ")")

    def calc(self):
        n = []
        for i, j in enumerate(self.c):
            if j != 0 and j != 'w':
                n.append(i)
        result = []
        for i in n:
            if i in self.basic_vars:
                result.append(round(get_col(self.simplex_table, 0)[self.basic_vars.index(i)], 2))
            else:
                result.append(0)

        return round(self.d[0], 2), result


    def solve(self, round_value = 2):
        self.add_basis()
        self.init_simplex_table()
        self.delta_calculation()
        self.search_lead_element()
        self.ouput_result(round_value)
        # self.print_simplex()

    # def round_table(self):
    #     rounded_table = []
    #     for row in self.simplex_table:
    #         rounded_row = [round(element, 2) for element in row]


    def sensitivity_analysis(self):
        strange_list = []
        index = 0
        # self.print_simplex()
        A = []
        func = [x for x in self.c if x != 0 and x != 'w']

        self.basic_vars = [i + 1 for i in self.basic_vars]
        for i in range(len(self.c) - len(self.A), 0, -1):
            if i not in self.basic_vars:
                A.append(get_col(self.simplex_table, i))
            else:
                pass
        A.reverse()
        print(A)
        for i in A:
            for j, k in zip(self.basic_vars, i):
                if j in list(range(1, self.n + 1)):
                    index = j
                    strange_list.append(round(k, 2))

        more_or_equal = []
        less_or_equal = []
        #
        # print(func)
        # print(strange_list)
        # print(index)

        if strange_list[index - 1] > 0:
            more_or_equal.append(-dot(strange_list, func)/strange_list[index -1])
        else:
            less_or_equal.append(-dot(strange_list, func)/strange_list[index -1])

        if len(more_or_equal) != 0:
            print("[", *more_or_equal, "; + inf)", sep='')
        elif len(less_or_equal) != 0:
            print("(- inf; ", *less_or_equal, ")", sep='')


        # print(self.d[:len(self.c) - len(self.A)])

        for i, j in zip(self.basic_vars, get_col(self.simplex_table, 0)):
            if i == index:
                strange_value = j
                for k in range(self.m):
                    if self.simplex_table[k][0] == strange_value:
                        self.simplex_table[k][0] = func[index-1] - int(input(f"Введите число\n"))
        self.delta_calculation()
        # if any(delta < 0 for delta in self.d[:len(self.c) - len(self.A)]):
        #     print(self.d[1:len(self.c) - len(self.A)])
        # else:

        self.search_lead_element()
        # print(self.d[:len(self.c) - len(self.A)])
        self.ouput_result(2)
        print("\n")

    def analysis(self):
        a = 0
        b = 0

        for j in range(1, 100):
            self.c[0] = j
            prev_a, prev_b = self.calc()
            # print(prev_a, prev_b)

            self.delta_calculation()
            self.search_lead_element()
            new_a, new_b = self.calc()


            if prev_a != new_a and prev_b != new_b:
                a = j
        print(f"x1: (0; {a - 1}]")

        for j in range(1, 100):
            self.c[1] = j
            prev_a, prev_b = self.calc()
            # print(prev_a, prev_b)

            self.delta_calculation()
            self.search_lead_element()
            new_a, new_b = self.calc()

            if prev_a != new_a and prev_b != new_b:
                b = j
        print(f"x2: (0; {b})")
