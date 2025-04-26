import os
import csv
from operator import itemgetter


def main():
    """
    Главная функция программы, которая управляет всеми операциями
    """
    print("Лабораторная работа №3. Файлы и словари\n")

    # Задание 1: Подсчет файлов в директории
    count_files_in_directory()

    # Задание 2: Работа с файлом data.csv
    # Проверяем существование файла
    if not os.path.exists('data.csv'):
        print("\nФайл data.csv не найден. Создаем пример файла.")
        create_sample_file()

    # Чтение данных из файла
    visits = read_visits_from_file()

    # 2.1. Сортировка по строковому полю (ФИО пациента)
    print("\nПосещения, отсортированные по ФИО пациента:")
    sorted_by_patient = sort_visits(visits, 'patient_name')
    print_visits(sorted_by_patient)

    # 2.2. Сортировка по числовому полю (длительность)
    print("\nПосещения, отсортированные по длительности:")
    sorted_by_duration = sort_visits(visits, 'duration')
    print_visits(sorted_by_duration)

    # 2.3. Фильтрация по критерию (длительность > 15 минут)
    print("\nПосещения длительностью более 15 минут:")
    filtered_visits = filter_visits(visits, 'duration', 15)
    print_visits(filtered_visits)

    # Задание 3: Добавление новых данных и сохранение в файл
    add_new_visit(visits)
    save_visits_to_file(visits)
    print("\nНовые данные сохранены в файл data.csv")


def count_files_in_directory():
    """
    Функция для подсчета файлов в текущей директории
    """
    files = [f for f in os.listdir() if os.path.isfile(f)]
    print(f"Количество файлов в текущей директории: {len(files)}")


def create_sample_file():
    """
    Функция для создания примерного файла data.csv, если он не существует
    """
    sample_data = [
        {'id': '1', 'patient_name': 'Иванов И.И.', 'doctor_name': 'Петров П.П.',
         'reason': 'ОРВИ', 'duration': 20},
        {'id': '2', 'patient_name': 'Сидоров С.С.', 'doctor_name': 'Васильева В.В.',
         'reason': 'Консультация', 'duration': 15},
        {'id': '3', 'patient_name': 'Петрова П.П.', 'doctor_name': 'Смирнов С.С.',
         'reason': 'Анализы', 'duration': 10},
        {'id': '4', 'patient_name': 'Кузнецов К.К.', 'doctor_name': 'Петров П.П.',
         'reason': 'Обследование', 'duration': 30},
        {'id': '5', 'patient_name': 'Алексеева А.А.', 'doctor_name': 'Васильева В.В.',
         'reason': 'Прививка', 'duration': 5}
    ]

    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'patient_name', 'doctor_name', 'reason', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_data)


def read_visits_from_file():
    """
    Чтение данных о посещениях из файла data.csv

    Возвращает:
        list: Список словарей с информацией о посещениях
    """
    visits = []
    with open('data.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Преобразуем duration в int
            row['duration'] = int(row['duration'])
            visits.append(row)
    return visits


def sort_visits(visits, field):
    """
    Сортировка списка посещений по указанному полю

    Параметры:
        visits (list): Список посещений
        field (str): Поле для сортировки

    Возвращает:
        list: Отсортированный список посещений
    """
    return sorted(visits, key=itemgetter(field))


def filter_visits(visits, field, threshold):
    """
    Фильтрация списка посещений по критерию

    Параметры:
        visits (list): Список посещений
        field (str): Поле для фильтрации
        threshold: Пороговое значение

    Возвращает:
        list: Отфильтрованный список посещений
    """
    return [visit for visit in visits if visit[field] > threshold]


def print_visits(visits):
    """
    Вывод списка посещений в удобочитаемом формате

    Параметры:
        visits (list): Список посещений для вывода
    """
    if not visits:
        print("Нет данных для отображения")
        return

    print("{:<5} {:<20} {:<20} {:<20} {:<10}".format(
        "№", "ФИО пациента", "ФИО врача", "Причина", "Длительность"))
    print("-" * 80)

    for visit in visits:
        print("{:<5} {:<20} {:<20} {:<20} {:<10}".format(
            visit['id'],
            visit['patient_name'],
            visit['doctor_name'],
            visit['reason'],
            visit['duration']
        ))


def add_new_visit(visits):
    """
    Добавление нового посещения в список

    Параметры:
        visits (list): Список посещений для дополнения
    """
    print("\nДобавление нового посещения:")

    new_visit = {
        'id': str(len(visits) + 1),
        'patient_name': input("ФИО пациента: "),
        'doctor_name': input("ФИО врача: "),
        'reason': input("Причина обращения: ")
    }

    while True:
        try:
            new_visit['duration'] = int(input("Длительность приема (мин): "))
            break
        except ValueError:
            print("Ошибка! Введите целое число для длительности.")

    visits.append(new_visit)
    print("Новое посещение успешно добавлено!")


def save_visits_to_file(visits):
    """
    Сохранение списка посещений в файл data.csv

    Параметры:
        visits (list): Список посещений для сохранения
    """
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'patient_name', 'doctor_name', 'reason', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(visits)


if __name__ == "__main__":
    main()