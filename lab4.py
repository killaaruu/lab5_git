import os
import csv
from datetime import datetime
from typing import Iterator, List, Dict, Optional


class MedicalVisit:
    """Базовый класс для представления посещения поликлиники"""

    # Статическое поле для хранения всех посещений
    _all_visits = []

    def __init__(self, visit_id: str, patient_name: str, doctor_name: str,
                 reason: str, duration: int, visit_date: Optional[str] = None):
        self._id = visit_id
        self._patient_name = patient_name
        self._doctor_name = doctor_name
        self._reason = reason
        self._duration = duration
        self._visit_date = visit_date or datetime.now().strftime("%Y-%m-%d")

        # Добавляем экземпляр в общий список
        MedicalVisit._all_visits.append(self)

    def __setattr__(self, name: str, value: str) -> None:
        """Контроль установки атрибутов"""
        if name == '_duration' and int(value) <= 0:
            raise ValueError("Длительность должна быть положительным числом")
        super().__setattr__(name, value)

    def __getitem__(self, key: str) -> str:
        """Доступ к атрибутам как к элементам коллекции"""
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(f"Нет атрибута {key}")

    def __repr__(self) -> str:
        """Официальное строковое представление"""
        return (f"MedicalVisit(id={self._id}, patient={self._patient_name}, "
                f"doctor={self._doctor_name}, reason={self._reason}, "
                f"duration={self._duration}, date={self._visit_date})")

    def __str__(self) -> str:
        """Неформальное строковое представление"""
        return (f"Посещение #{self._id}: {self._patient_name} у {self._doctor_name} "
                f"по причине '{self._reason}' ({self._duration} мин)")

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Длительность должна быть положительным числом")
        self._duration = value

    @staticmethod
    def load_from_csv(filename: str = 'data.csv') -> None:
        """Статический метод для загрузки данных из CSV"""
        MedicalVisit._all_visits.clear()
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    MedicalVisit(
                        visit_id=row['id'],
                        patient_name=row['patient_name'],
                        doctor_name=row['doctor_name'],
                        reason=row['reason'],
                        duration=int(row['duration']),
                        visit_date=row.get('date')
                    )
        except FileNotFoundError:
            print(f"Файл {filename} не найден")

    @staticmethod
    def save_to_csv(filename: str = 'data.csv') -> None:
        """Статический метод для сохранения данных в CSV"""
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'patient_name', 'doctor_name', 'reason', 'duration', 'date'
            ])
            writer.writeheader()
            for visit in MedicalVisit._all_visits:
                writer.writerow({
                    'id': visit._id,
                    'patient_name': visit._patient_name,
                    'doctor_name': visit._doctor_name,
                    'reason': visit._reason,
                    'duration': visit._duration,
                    'date': visit._visit_date
                })

    @staticmethod
    def count_files_in_directory(path: str = '.') -> int:
        """Статический метод для подсчета файлов в директории"""
        return len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    @classmethod
    def get_visits_by_doctor(cls, doctor_name: str) -> Iterator['MedicalVisit']:
        """Генератор для получения посещений конкретного врача"""
        for visit in cls._all_visits:
            if visit._doctor_name == doctor_name:
                yield visit

    @classmethod
    def get_long_visits(cls, min_duration: int = 15) -> Iterator['MedicalVisit']:
        """Генератор для получения длительных посещений"""
        for visit in cls._all_visits:
            if visit._duration > min_duration:
                yield visit

    def to_dict(self) -> Dict[str, str]:
        """Преобразование объекта в словарь"""
        return {
            'id': self._id,
            'patient_name': self._patient_name,
            'doctor_name': self._doctor_name,
            'reason': self._reason,
            'duration': self._duration,
            'date': self._visit_date
        }


class ExtendedMedicalVisit(MedicalVisit):
    """Расширенный класс посещения с дополнительной информацией"""

    def __init__(self, visit_id: str, patient_name: str, doctor_name: str,
                 reason: str, duration: int, diagnosis: str,
                 visit_date: Optional[str] = None):
        super().__init__(visit_id, patient_name, doctor_name, reason, duration, visit_date)
        self._diagnosis = diagnosis

    def __repr__(self) -> str:
        """Переопределение repr для расширенного класса"""
        return (f"ExtendedMedicalVisit(id={self._id}, patient={self._patient_name}, "
                f"doctor={self._doctor_name}, reason={self._reason}, "
                f"duration={self._duration}, diagnosis={self._diagnosis}, "
                f"date={self._visit_date})")

    def __str__(self) -> str:
        """Переопределение str для расширенного класса"""
        return (f"Расширенное посещение #{self._id}: {self._patient_name} у "
                f"{self._doctor_name} с диагнозом '{self._diagnosis}'")


class VisitCollection:
    """Класс-коллекция для работы с посещениями"""

    def __init__(self, visits: List[MedicalVisit]):
        self._visits = visits

    def __iter__(self) -> Iterator[MedicalVisit]:
        """Итератор по коллекции"""
        return iter(self._visits)

    def __getitem__(self, index: int) -> MedicalVisit:
        """Доступ по индексу"""
        return self._visits[index]

    def __len__(self) -> int:
        """Количество элементов в коллекции"""
        return len(self._visits)

    def sort_by(self, attribute: str, reverse: bool = False) -> 'VisitCollection':
        """Сортировка коллекции по атрибуту"""
        return VisitCollection(sorted(
            self._visits,
            key=lambda x: getattr(x, f"_{attribute}"),
            reverse=reverse
        ))

    def filter_by(self, attribute: str, value: str) -> 'VisitCollection':
        """Фильтрация коллекции по значению атрибута"""
        return VisitCollection([
            visit for visit in self._visits
            if getattr(visit, f"_{attribute}") == value
        ])


def main():
    print("Лабораторная работа №4. Классы\n")

    # 1. Подсчет файлов в директории (статический метод)
    file_count = MedicalVisit.count_files_in_directory()
    print(f"Количество файлов в текущей директории: {file_count}")

    # 2. Загрузка данных из файла
    MedicalVisit.load_from_csv()

    # Если файл был пуст, создаем тестовые данные
    if not MedicalVisit._all_visits:
        print("\nСоздаем тестовые данные...")
        MedicalVisit("1", "Иванов И.И.", "Петров П.П.", "ОРВИ", 20)
        MedicalVisit("2", "Сидоров С.С.", "Васильева В.В.", "Консультация", 15)
        ExtendedMedicalVisit("3", "Петрова П.П.", "Смирнов С.С.",
                             "Анализы", 10, "Здоров")
        ExtendedMedicalVisit("4", "Кузнецов К.К.", "Петров П.П.",
                             "Обследование", 30, "Гипертония")
        MedicalVisit("5", "Алексеева А.А.", "Васильева В.В.", "Прививка", 5)
        MedicalVisit.save_to_csv()

    # Создаем коллекцию посещений
    visits = VisitCollection(MedicalVisit._all_visits)

    # 3. Демонстрация работы итератора
    print("\nВсе посещения (через итератор):")
    for idx, visit in enumerate(visits, 1):
        print(f"{idx}. {visit}")

    # 4. Демонстрация доступа по индексу
    print("\nПервое посещение (доступ по индексу):")
    print(visits[0])

    # 5. Демонстрация сортировки
    print("\nПосещения, отсортированные по длительности:")
    sorted_visits = visits.sort_by("duration")
    for visit in sorted_visits:
        print(f"{visit.duration} мин: {visit._patient_name}")

    # 6. Демонстрация фильтрации
    print("\nПосещения у врача Петров П.П.:")
    filtered_visits = visits.filter_by("doctor_name", "Петров П.П.")
    for visit in filtered_visits:
        print(visit)

    # 7. Демонстрация генератора
    print("\nДлительные посещения (более 15 мин):")
    for visit in MedicalVisit.get_long_visits():
        print(visit)

    # 8. Добавление нового посещения
    print("\nДобавление нового посещения:")
    try:
        new_visit = MedicalVisit(
            visit_id=str(len(visits) + 1),
            patient_name=input("ФИО пациента: "),
            doctor_name=input("ФИО врача: "),
            reason=input("Причина обращения: "),
            duration=int(input("Длительность приема (мин): "))
        )
        print(f"Добавлено новое посещение: {new_visit}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # 9. Сохранение данных
    MedicalVisit.save_to_csv()
    print("\nДанные сохранены в файл data.csv")

    # 10. Демонстрация repr
    print("\nПример repr для посещения:")
    print(repr(visits[0]))

    # 11. Демонстрация наследования
    print("\nДемонстрация наследования (расширенные посещения):")
    for visit in visits:
        if isinstance(visit, ExtendedMedicalVisit):
            print(visit)


if __name__ == "__main__":
    main()