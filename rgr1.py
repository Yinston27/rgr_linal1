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

def simplified_matrix(matrix, mode=None):
    POR = len(matrix)
    if type(mode) == list:
        unknows_list = mode[:]
    
    for LINE in range(POR):
        # Если диагональный элемент нулевой, ищем ненулевой элемент в столбце
        if matrix[LINE][LINE] == 0:
            found = False
            for row in range(LINE + 1, POR):
                if matrix[row][LINE] != 0:
                    # Меняем строки местами
                    matrix[LINE], matrix[row] = matrix[row], matrix[LINE]
                    found = True
                    break
            
            if not found:
                # Ищем ненулевой элемент в этой строке справа
                for col in range(LINE + 1, len(matrix[LINE]) - 1):
                    if matrix[LINE][col] != 0:
                        # Меняем столбцы местами
                        if type(mode) == list:
                            unknows_list[LINE], unknows_list[col] = unknows_list[col], unknows_list[LINE]
                        for i in range(POR):
                            matrix[i][LINE], matrix[i][col] = matrix[i][col], matrix[i][LINE]
                        found = True
                        break
                
                if not found:
                    # Вся строка нулевая - пропускаем
                    continue
        
        # Нормализуем строку
        if matrix[LINE][LINE] != 0:
            divisor = matrix[LINE][LINE]
            matrix[LINE] = [elem / divisor for elem in matrix[LINE]]
            matrix = subtraction_all(matrix, LINE, POR)
    
    # Удаляем нулевые строки
    non_zero_rows = []
    for i in range(POR):
        if any(matrix[i][j] != 0 for j in range(len(matrix[i]) - 1)):
            non_zero_rows.append(matrix[i])
        elif matrix[i][-1] != 0:  # Случай 0 = b, где b != 0 - нет решений
            if type(mode) == list:
                return [matrix, unknows_list, i, True]  # Флаг отсутствия решений
    
    if mode == -1:
        return non_zero_rows
    elif mode == 1:
        return len(non_zero_rows)
    elif type(mode) == list:
        return [non_zero_rows, unknows_list, len(non_zero_rows), False]  # Решения есть
    else:
        return non_zero_rows

def slau(unknows, lines):
    matric = [list(map(Fraction, input(f"Коэффициенты {i+1} уравнения через пробел: ").split(' '))) for i in range(lines)]
    list_b = list(map(Fraction, input(f"Коэффициенты столбца B через пробел: ").split(' ')))
    matrix_b = [matric[i] + [list_b[i]] for i in range(lines)]
    unknows_list = [f'{i+1}' for i in range(unknows)]
    
    result = simplified_matrix(matrix_b, mode=unknows_list)
    # Проверяем наличие решений
    if result[3]:  # Если установлен флаг отсутствия решений
        print('Решений нет')
        return None
    
    matrix_b, unknows_list, rang_matrix_b = result[:3]
    line_list = []
    free_vars = []
    
    # Определяем свободные переменные
    if rang_matrix_b < unknows:
        free_vars = unknows_list[rang_matrix_b:unknows]
    
    # Формируем уравнения для базисных переменных
    for i in range(min(rang_matrix_b, unknows)):
        equation = f'X{unknows_list[i]} = '
        terms = []
        
        # Свободный член
        if matrix_b[i][-1] != 0:
            terms.append(f'{matrix_b[i][-1]}')
        
        # Коэффициенты при свободных переменных
        for j in range(rang_matrix_b, unknows):
            if j < len(matrix_b[i]) - 1 and matrix_b[i][j] != 0:
                coeff = -matrix_b[i][j]
                if coeff > 0:
                    terms.append(f'+ {coeff}×X{unknows_list[j]}')
                else:
                    terms.append(f'- {-coeff}×X{unknows_list[j]}')
        
        # Коэффициенты при других базисных переменных
        for j in range(i + 1, min(rang_matrix_b, unknows)):
            if j < len(matrix_b[i]) - 1 and matrix_b[i][j] != 0:
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
    print("\nРешение системы:")
    for line in line_list:
        print(line)


def fund_matrix(unknows=3, lines=3):
    matric = [list(map(Fraction, input(f"Коэффициенты {i+1} уравнения через пробел: ").split(' '))) for i in range(lines)]
    list_b = list(map(Fraction, input(f"Коэффициенты столбца B через пробел: ").split(' ')))
    matrix_b = [matric[i] + [list_b[i]] for i in range(lines)]
    unknows_list = [f'{i+1}' for i in range(unknows)]
    res = simplified_matrix(matrix_b, mode=unknows_list)

    if len(res) != 4:
        print('Упсс(')
        return res
    
    matrix, unknows_list, rang, nonconvergence = res

    if len(unknows_list) == rang:
        print('Система имеет только одно решение')
        return res
    
    identity_matrix = [[int(i==j) for j in range(len(unknows_list)-rang)] for i in range(len(unknows_list)-rang)]
    return_fund_matrix = [[] for i in range(len(unknows_list))]
    # сортировка по количеству нулей в строках матрицы, не считая свободные члены - от свободных до "самых базисных":
    matrix = sorted(matrix[::-1], key=lambda x: x[:-1].count(0), reverse=True) 
    vectors_list = [[0 for i in range(len(unknows_list))] for j in range(len(identity_matrix))]
    for iter_num_vector in range(len(vectors_list)):
        iter_vector = vectors_list[iter_num_vector]
        for number_line in range(len(unknows_list)-1, -1, -1):
            if number_line >= rang:
                iter_vector[number_line] = identity_matrix[iter_num_vector][number_line - rang]
            else:
                list_lin_komb = []
                for j in range(number_line+1, len(unknows_list)):
                    # print(number_line, str(iter_vector[j]), iter_vector)
                    list_lin_komb.append(-matrix[number_line + 1 - rang][j] * Fraction(str(iter_vector[j])))

                sum_list_lin_komb = 0
                for l in range(len(list_lin_komb)):
                    sum_list_lin_komb += list_lin_komb[l]
                
                iter_vector[number_line] = matrix[number_line + 1 - rang][-1] + sum_list_lin_komb
        
        unknows_list_for_sort = unknows_list[:]
        # сортировка
        for i in range(len(iter_vector)-1):
            for j in range(i, len(iter_vector)-1):
                if int(unknows_list_for_sort[j]) > int(unknows_list_for_sort[j+1]):
                    unknows_list_for_sort[j], unknows_list_for_sort[j+1] = unknows_list_for_sort[j+1], unknows_list_for_sort[j]
                    iter_vector[j], iter_vector[j+1] = iter_vector[j+1], iter_vector[j]
        # создание 
        for i in range(len(return_fund_matrix)):
            return_fund_matrix[i].append(iter_vector[i])
    # вывод
    for line in return_fund_matrix:
        print(*line)


if __name__ == "__main__":
    # printer(simplified_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], mode=-1))
    # slau(unknows=4, lines=3)
    # fund_matrix(unknows=4, lines=3)