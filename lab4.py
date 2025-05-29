import os
import csv
from operator import itemgetter


class Visit:
    def __init__(self, visit_id, patient_name, doctor_name, reason, duration):
        self.id = visit_id
        self.patient_name = patient_name
        self.doctor_name = doctor_name
        self.reason = reason
        self.duration = int(duration)

    def __setattr__(self, key, value):
        # Запись значений только через __setattr__
        if key in ['id', 'patient_name', 'doctor_name', 'reason', 'duration']:
            object.__setattr__(self, key, value)
        else:
            raise AttributeError(f"Недопустимый атрибут: {key}")

    def __repr__(self):
        return f"Visit(id={self.id}, patient='{self.patient_name}', doctor='{self.doctor_name}', reason='{self.reason}', duration={self.duration})"

    def to_dict(self):
        return {
            'id': self.id,
            'patient_name': self.patient_name,
            'doctor_name': self.doctor_name,
            'reason': self.reason,
            'duration': self.duration
        }

    @staticmethod
    def from_dict(data):
        return Visit(
            data['id'],
            data['patient_name'],
            data['doctor_name'],
            data['reason'],
            data['duration']
        )


class ClinicHistory:
    def __init__(self, visits=None):
        self._visits = visits or []

    def __iter__(self):
        # Реализация итератора
        return iter(self._visits)

    def __getitem__(self, index):
        # Доступ по индексу
        return self._visits[index]

    def __len__(self):
        return len(self._visits)

    def add_visit(self, visit):
        self._visits.append(visit)

    def sort_by_patient(self):
        return ClinicHistory(sorted(self._visits, key=lambda v: v.patient_name))

    def sort_by_duration(self):
        return ClinicHistory(sorted(self._visits, key=lambda v: v.duration))

    def filter_by_duration(self, threshold):
        return ClinicHistory([v for v in self._visits if v.duration > threshold])

    def save_to_file(self, filename='data.csv'):
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'patient_name', 'doctor_name', 'reason', 'duration']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for visit in self._visits:
                writer.writerow(visit.to_dict())

    @staticmethod
    def load_from_file(filename='data.csv'):
        try:
            visits = []
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    visits.append(Visit.from_dict(row))
            return ClinicHistory(visits)
        except FileNotFoundError:
            print("Файл не найден.")
            return ClinicHistory()

    @staticmethod
    def generate_sample_data():
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
        return [Visit.from_dict(d) for d in sample_data]


class ExtendedClinicHistory(ClinicHistory):
    def total_duration(self):
        return sum(visit.duration for visit in self._visits)

    def patients_of_doctor(self, doctor_name):
        return ClinicHistory([v for v in self._visits if v.doctor_name == doctor_name])


def count_files_in_directory():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    return len(files)


def main():
    print("Лабораторная работа №4. Классы\n")

    # 1. Подсчет файлов в директории
    file_count = count_files_in_directory()
    print(f"Количество файлов в текущей директории: {file_count}\n")

    # 2. Загрузка данных из файла
    clinic_history = ClinicHistory.load_from_file()

    if not clinic_history:
        print("Файл data.csv не найден. Создаем пример данных.\n")
        clinic_history = ExtendedClinicHistory(ExtendedClinicHistory.generate_sample_data())

    # 2.1. Сортировка по ФИО пациента
    sorted_by_patient = clinic_history.sort_by_patient()
    print("Посещения, отсортированные по ФИО пациента:")
    for visit in sorted_by_patient:
        print(visit)

    # 2.2. Сортировка по длительности
    sorted_by_duration = clinic_history.sort_by_duration()
    print("\nПосещения, отсортированные по длительности:")
    for visit in sorted_by_duration:
        print(visit)

    # 2.3. Фильтрация по длительности
    filtered_visits = clinic_history.filter_by_duration(15)
    print("\nПосещения длительностью более 15 минут:")
    for visit in filtered_visits:
        print(visit)

    # Генератор пациентов определенного врача (через наследование)
    doctor_visits = clinic_history.patients_of_doctor('Васильева В.В.')
    print("\nПациенты у врача Васильева В.В.:")
    for visit in doctor_visits:
        print(visit)

    # Общая суммарная длительность приемов
    extended_clinic = ExtendedClinicHistory(clinic_history)
    print(f"\nОбщая длительность всех посещений: {extended_clinic.total_duration()} мин.")

    # Добавление нового посещения
    print("\nДобавление нового посещения:")
    new_visit = Visit(
        id=str(len(clinic_history) + 1),
        patient_name=input("ФИО пациента: "),
        doctor_name=input("ФИО врача: "),
        reason=input("Причина обращения: "),
        duration=int(input("Длительность (мин): "))
    )
    clinic_history.add_visit(new_visit)
    print("Новое посещение добавлено!\n")

    # Сохранение обратно в CSV
    clinic_history.save_to_file()
    print("Новые данные сохранены в файл data.csv")


if __name__ == "__main__":
    main()