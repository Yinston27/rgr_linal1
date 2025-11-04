from fractions import Fraction

def printer(matrgaus, por=None, f=None):
    if type(matrgaus) == int:
        print('Вырожденная матрица!')
        return None
    POR = len(matrgaus)
    if f == None:
        for i in matrgaus:
            for j in i:
                print(j, end='\t')
            print()
        print()
    else:
        for i in matrgaus:
            for j in i[POR:]:
                print(j, end='\t')
            print()
        print()


def subtraction_all(matrix, LINE, POR):
    list_k = [matrix[j][LINE] for j in range(POR)]
    for strok in [h for h in range(POR) if h != LINE]:
        matrix[strok] = [matrix[strok][l] - list_k[strok]*matrix[LINE][l] for l in range(len(matrix[LINE]))]
    return matrix
            
def revert_col(matrics, one_col, two_col):
    col_one = [i[one_col] for i in matrics] 
    for i in range(len(matrics)):
        matrics[i][one_col] = matrics[i][two_col]
        matrics[i][two_col] = col_one[i]
    return matrics

# -----
def matrix_value(matrix, unknows_list, rang_matrix, mode='slau'):
    line_list = [0 for i in range(len(unknows_list))]
    # печать значений
    if mode == 'fund':
        for i in range(rang_matrix):
            line = 0
            for j in range(len(unknows_list)):
                if i == j:
                    key = i
                    if i == rang_matrix - 1 and matrix[i][-1] != 0 and rang_matrix == len(matrix):
                        line += Fraction(matrix[i][-1])
                elif j == i + 1 and matrix[i][-1] != 0:
                    line += Fraction(matrix[i][-1])
                else:
                    if matrix[i][j] == 0:
                        continue
                    else:
                        if matrix[i][j] == 1:
                            line += Fraction(-1*unknows_list[j])
                        else:
                            line += Fraction(-1*matrix[i][j])*Fraction(unknows_list[j])
            line_list[key] = line   

        if rang_matrix < len(unknows_list):
            for j in range(rang_matrix, len(unknows_list)):
                line_list[j] = Fraction(unknows_list[j])
    print(line_list)
        
        # 

# ----

def simplified_matrix(matrix, mode = None):
    POR = len(matrix)
    if type(mode) == list:
        unknows_list = mode[:]
    for LINE in range(POR):
        if matrix[LINE][LINE] != 0:
            matrix[LINE] = [matrix[LINE][l] / matrix[LINE][LINE] for l in range(len(matrix[LINE]))]
            matrix = subtraction_all(matrix, LINE, POR)
        else:
            if len(set(matrix[LINE][:POR])) == 1 and 0 in matrix[LINE][:POR]:
                if mode == -1:
                    return LINE
                elif (LINE == POR - 1) and (type(mode) == list):
                    return [matrix, unknows_list, LINE]
                else:
                    if mode == 1 and LINE == POR - 1:
                        return POR - 1
                    else:
                        for i in range(POR-LINE-1):
                            matrix.append(matrix.pop(LINE))
                            if not(len(set(matrix[LINE][:POR])) == 1 and 0 in matrix[LINE][:POR]):
                                break
                            if i == LINE-1:
                                if type(mode) != list:
                                    return LINE
                                else:
                                    return [matrix, unknows_list, LINE]
            col_index = [i for i in range(LINE, POR) if matrix[LINE][i] != 0]
            one_col = min(col_index)
            if one_col == LINE:
                continue
            else:
                matrix = revert_col(matrix, one_col, LINE)
                if mode == 1:
                    continue
                elif type(mode) == list:
                    unknows_list[one_col], unknows_list[LINE] = unknows_list[LINE], unknows_list[one_col]
            matrix[LINE] = [matrix[LINE][l] / matrix[LINE][LINE] for l in range(len(matrix[LINE]))]
            matrix = subtraction_all(matrix, LINE, POR)
    if mode == -1:
        return matrix
    elif mode == 1:
        return len(matrix)
    else:
        # Список - матрица и порядок неизвестных
        return [matrix, unknows_list, POR]


def revert_matr(POR=2):
    matr = [list(map(Fraction, input(f"Коэффиценты {i+1} строки через пробел: ").split(' '))) for i in range(POR)]
    matrgaus = [[] for i in range(POR)]
    # Составление расширенной матрицы
    for i in range(POR):
        line_E = list(map(int, ('0 '*POR).split(' ')[:-1]))
        line_E[i] = 1
        matrgaus[i] = matr[i] + line_E
    # Проход по строкам расш матр
    matrgaus = simplified_matrix(matrgaus, mode = -1)
    # если матрица вырождена
    if type(matrgaus) == int:
        return matrgaus
    matrics = [[] for i in range(POR)]
    for line in range(POR):
        matrics[line] = [i for i in matrgaus[line][POR:]]
    return matrics


def rang(por=2):
    matrix = [list(map(Fraction, input(f"Коэффиценты {i+1} строки через пробел: ").split(' '))) for i in range(por)]
    rang_m = simplified_matrix(matrix, mode=1)
    if type(rang_m) == list:
        print(f'Ранг - {len(rang_m)}')
    else:
        print(f'Ранг - {rang_m}')



def slau(unknows, lines):
    matric = [list(map(Fraction, input(f"Коэффиценты {i+1} уравнения через пробел: ").split(' '))) for i in range(lines)]
    list_b = list(map(Fraction, input(f"Коэффиценты столбца B через пробел: ").split(' ')))
    matrix_b = [matric[i]+[list_b[i]] for i in range(lines)]
    unknows_list = []
    for i in range(unknows):
        unknows_list.append(f'{i+1}')
        
    matrix_b, unknows_list, rang_matrix_b = simplified_matrix(matrix_b, mode = unknows_list)
    if [matrix_b[i][-1] for i in range(rang_matrix_b, lines) if matrix_b[i][-1] != 0]:
        print('Решений нет')
        return None
     
    line_list = []
    free_vars = []
    
    # Определяем свободные переменные
    if rang_matrix_b < unknows:
        free_vars = unknows_list[rang_matrix_b:]
    
    # Формируем уравнения для базисных переменных
    for i in range(rang_matrix_b):
        equation = f'X{unknows_list[i]} = '
        terms = []
        
        # Свободный член
        if matrix_b[i][-1] != 0:
            terms.append(f'{matrix_b[i][-1]}')
        
        # Коэффициенты при свободных переменных
        for j in range(rang_matrix_b, unknows):
            if matrix_b[i][j] != 0:
                coeff = -matrix_b[i][j]
                if coeff > 0:
                    terms.append(f'+ {coeff}×X{unknows_list[j]}')
                else:
                    terms.append(f'- {-coeff}×X{unknows_list[j]}')
        
        # Коэффициенты при других базисных переменных (для диагонального вида)
        for j in range(i + 1, rang_matrix_b):
            if matrix_b[i][j] != 0:
                coeff = -matrix_b[i][j]
                if coeff > 0:
                    terms.append(f'+ {coeff}×X{unknows_list[j]}')
                else:
                    terms.append(f'- {-coeff}×X{unknows_list[j]}')
        
        if not terms:  # если нет дополнительных членов
            terms.append('0')
        
        equation += ' '.join(terms)
        line_list.append(equation)
    
    # Добавляем свободные переменные
    for var in free_vars:
        line_list.append(f'X{var} - свободная переменная')
    
    # Выводим результаты
    for line in line_list:
        print(line)


# printer(revert_matr(3))
# rang(4)
slau(3, 3)

def fundamental_matrix():
    ...

