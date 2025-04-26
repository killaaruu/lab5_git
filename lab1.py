def main():
    """
    Главная функция программы, которая управляет вводом данных и вызовом обработки списков.
    """
    print("Лабораторная работа №1. Обработка списков")

    # Ввод списка A
    a = input_list("A")
    # Ввод списка B
    b = input_list("B")

    print("\nИсходный список A:", a)
    print("Исходный список B:", b)

    # Обработка списка A без использования стандартных функций
    a_processed_manual = process_list_manual(a.copy(), b)
    print("\nРезультат обработки (без стандартных функций):", a_processed_manual)

    # Обработка списка A с использованием стандартных функций
    a_processed_std = process_list_std(a.copy(), b)
    print("Результат обработки (со стандартными функциями):", a_processed_std)


def input_list(list_name):
    """
    Функция для ввода списка с клавиатуры или автоматической генерации.

    Параметры:
        list_name (str): Имя списка (A или B) для отображения в подсказках.

    Возвращает:
        list: Введенный или сгенерированный список.
    """
    while True:
        try:
            choice = input(f"\nВвести список {list_name} с клавиатуры (1) или сгенерировать автоматически (2)? ")
            if choice == '1':
                # Ввод с клавиатуры
                elements = input(f"Введите элементы списка {list_name} через пробел: ").split()
                return [int(x) for x in elements]
            elif choice == '2':
                # Автоматическая генерация
                import random
                size = int(input(f"Введите размер списка {list_name} для генерации: "))
                return [random.randint(1, 10) for _ in range(size)]
            else:
                print("Пожалуйста, введите 1 или 2.")
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите корректные данные.")


def process_list_manual(a, b):
    """
    Обработка списка A без использования стандартных функций.
    Удаляет цепочки нечетных элементов, в которых нет ни одного элемента из списка B.

    Параметры:
        a (list): Список A для обработки.
        b (list): Список B для проверки элементов.

    Возвращает:
        list: Обработанный список A.
    """
    i = 0
    while i < len(a):
        # Находим начало цепочки нечетных элементов
        if a[i] % 2 != 0:
            start = i
            # Находим конец цепочки
            while i < len(a) and a[i] % 2 != 0:
                i += 1
            end = i

            # Проверяем, есть ли в цепочке элементы из B
            has_b_element = False
            for j in range(start, end):
                # Проверяем, есть ли текущий элемент в B
                elem_in_b = False
                for elem_b in b:
                    if a[j] == elem_b:
                        elem_in_b = True
                        break
                if elem_in_b:
                    has_b_element = True
                    break

            # Если в цепочке нет элементов из B, удаляем ее
            if not has_b_element:
                del a[start:end]
                i = start  # После удаления возвращаемся на новую позицию
        else:
            i += 1
    return a


def process_list_std(a, b):
    """
    Обработка списка A с использованием стандартных функций.
    Удаляет цепочки нечетных элементов, в которых нет ни одного элемента из списка B.

    Параметры:
        a (list): Список A для обработки.
        b (list): Список B для проверки элементов.

    Возвращает:
        list: Обработанный список A.
    """
    i = 0
    while i < len(a):
        if a[i] % 2 != 0:
            start = i
            # Находим конец цепочки нечетных элементов
            while i < len(a) and a[i] % 2 != 0:
                i += 1
            end = i

            # Получаем подсписок цепочки
            sublist = a[start:end]

            # Проверяем пересечение с списком B
            if not any(elem in b for elem in sublist):
                del a[start:end]
                i = start
        else:
            i += 1
    return a


if __name__ == "__main__":
    main()