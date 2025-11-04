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
    
    # Дополнительная проверка: если есть строка 0 0 ... 0 | b, где b ≠ 0
    for i in range(len(matrix_b)):
        all_zeros = all(matrix_b[i][j] == 0 for j in range(unknows))
        if all_zeros and matrix_b[i][-1] != 0:
            print('Решений нет')
            return None
    
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

if __name__ == "__main__":
    slau(unknows=4, lines=3)