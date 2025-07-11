import numpy as np


def main():
    """
    Главная функция программы, которая управляет генерацией матрицы,
    ее обработкой и сохранением результатов.
    """
    print("Лабораторная работа №2. Двумерные структуры данных")

    # Генерация матрицы
    matrix = generate_matrix()
    print("\nСгенерированная матрица:")
    print(matrix)

    # Обработка матрицы
    result_matrix = process_matrix(matrix)
    print("\nРезультирующая матрица с количеством отрицательных элементов:")
    print(result_matrix)

    # Сохранение результатов в файл
    save_results(matrix, result_matrix)
    print("\nРезультаты сохранены в файл 'matrix_results.txt'")


def generate_matrix():
    """
    Функция для генерации прямоугольной матрицы случайных чисел.

    Возвращает:
        numpy.ndarray: Сгенерированная матрица размером N x M.
    """
    while True:
        try:
            n = int(input("Введите количество строк матрицы (N): "))
            m = int(input("Введите количество столбцов матрицы (M): "))
            if n <= 0 or m <= 0:
                print("Размеры матрицы должны быть положительными числами.")
                continue
            break
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите целое число.")

    # Генерация матрицы со случайными целыми числами от -10 до 10
    return np.random.randint(-10, 11, size=(n, m))


def process_matrix(matrix):
    """
    Функция для обработки матрицы: подсчет отрицательных элементов
    в строках и столбцах и формирование результирующей матрицы.

    Параметры:
        matrix (numpy.ndarray): Исходная матрица для обработки.

    Возвращает:
        numpy.ndarray: Результирующая матрица с дополнительными строками и столбцами.
    """
    n, m = matrix.shape

    # Создаем результирующую матрицу с дополнительными строкой и столбцом
    result = np.zeros((n + 1, m + 1), dtype=int)

    # Копируем исходную матрицу в левый верхний угол
    result[:n, :m] = matrix

    # Подсчет отрицательных элементов в столбцах (последняя строка)
    for j in range(m):
        result[n, j] = np.sum(matrix[:, j] < 0)

    # Подсчет отрицательных элементов в строках (последний столбец)
    for i in range(n):
        result[i, m] = np.sum(matrix[i, :] < 0)

    # Подсчет общего количества отрицательных элементов (правый нижний угол)
    result[n, m] = np.sum(matrix < 0)

    return result


def save_results(original_matrix, result_matrix):
    """
    Функция для сохранения исходной и результирующей матриц в файл.

    Параметры:
        original_matrix (numpy.ndarray): Исходная матрица.
        result_matrix (numpy.ndarray): Обработанная матрица.
    """
    with open('matrix_results.txt', 'w') as f:
        f.write("Исходная матрица:\n")
        np.savetxt(f, original_matrix, fmt='%4d')

        f.write("\nРезультирующая матрица:\n")
        np.savetxt(f, result_matrix, fmt='%4d')

        # Добавляем пояснения к результирующей матрице
        f.write("\nПояснения:\n")
        f.write("- Последний столбец содержит количество отрицательных элементов в каждой строке\n")
        f.write("- Последняя строка содержит количество отрицательных элементов в каждом столбце\n")
        f.write("- Правый нижний элемент содержит общее количество отрицательных элементов в матрице\n")


if __name__ == "__main__":
    main()