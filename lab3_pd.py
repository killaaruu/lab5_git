import os
import pandas as pd


def main():
    print("Лабораторная работа №3. Файлы и словари (с использованием Pandas)\n")

    # 1. Подсчет файлов в директории
    count_files_in_directory()

    # 2. Работа с файлом data.csv
    if not os.path.exists('data.csv'):
        print("\nФайл data.csv не найден. Создаем пример файла.")
        create_sample_file()

    # Чтение данных в DataFrame
    try:
        df = pd.read_csv('data.csv', dtype={'id': str, 'duration': int})
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return

    # 2.1. Сортировка по строковому полю (ФИО пациента)
    print("\nПосещения, отсортированные по ФИО пациента:")
    print(sort_visits(df, 'patient_name'))

    # 2.2. Сортировка по числовому полю (длительность)
    print("\nПосещения, отсортированные по длительности:")
    print(sort_visits(df, 'duration'))

    # 2.3. Фильтрация по критерию (длительность > 15 минут)
    print("\nПосещения длительностью более 15 минут:")
    print(filter_visits(df, 'duration', 15))

    # 3. Добавление новых данных и сохранение
    df = add_new_visit(df)
    save_visits_to_file(df)
    print("\nНовые данные сохранены в файл data.csv")


def count_files_in_directory():
    """Подсчет файлов в текущей директории"""
    files = [f for f in os.listdir() if os.path.isfile(f)]
    print(f"Количество файлов в текущей директории: {len(files)}")


def create_sample_file():
    """Создание примерного файла data.csv"""
    data = {
        'id': ['1', '2', '3', '4', '5'],
        'patient_name': ['Иванов И.И.', 'Сидоров С.С.', 'Петрова П.П.', 'Кузнецов К.К.', 'Алексеева А.А.'],
        'doctor_name': ['Петров П.П.', 'Васильева В.В.', 'Смирнов С.С.', 'Петров П.П.', 'Васильева В.В.'],
        'reason': ['ОРВИ', 'Консультация', 'Анализы', 'Обследование', 'Прививка'],
        'duration': [20, 15, 10, 30, 5]
    }
    pd.DataFrame(data).to_csv('data.csv', index=False)


def sort_visits(df, column):
    """Сортировка DataFrame по указанному столбцу"""
    return df.sort_values(by=column)


def filter_visits(df, column, threshold):
    """Фильтрация DataFrame по значению столбца"""
    return df[df[column] > threshold]


def add_new_visit(df):
    """Добавление новой записи в DataFrame"""
    print("\nДобавление нового посещения:")

    new_data = {
        'id': str(len(df) + 1),
        'patient_name': input("ФИО пациента: "),
        'doctor_name': input("ФИО врача: "),
        'reason': input("Причина обращения: ")
    }

    while True:
        try:
            new_data['duration'] = int(input("Длительность приема (мин): "))
            break
        except ValueError:
            print("Ошибка! Введите целое число для длительности.")

    # Добавляем новую запись
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    print("Новое посещение успешно добавлено!")
    return df


def save_visits_to_file(df):
    """Сохранение DataFrame в файл"""
    df.to_csv('data.csv', index=False)


if __name__ == "__main__":
    main()