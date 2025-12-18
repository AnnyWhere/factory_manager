from datetime import datetime
import json
import os
from employees import Chief, Employee
from workshop import WorkShop
from factory import Factory
from workers import *


class Menu:
    """Класс-фасад для взаимодействия с пользователем и управления всей системой."""

    def __init__(self, factory_name: str = "ООО 'Промышленный Завод'"):
        """
        Инициализация меню-фасада.

        Args:
            factory_name: Название завода
        """
        self.factory = Factory(factory_name)
        self.data_file = "factory_data.json"
        self.log_file = "factory_log.json"

        if not os.path.exists(self.log_file):
            self._save_log("Инициализация системы", {"factory_name": factory_name})

        if not os.path.exists(self.data_file):
            self._save_data()

    def _save_log(self, action: str, details: dict) -> None:
        """
        Сохранение лога действий.

        Args:
            action: Описание действия
            details: Детали действия
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }

        logs = []
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_entry)

        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def _save_data(self) -> None:
        """Сохранение данных завода в JSON файл."""
        workshops_data = []
        for workshop in self.factory.get_all_workshops():
            workshops_data.append(workshop.to_dict())

        data = {
            "factory_name": self.factory.name,
            "workshops": workshops_data,
            "total_workshops": len(self.factory.get_all_workshops()),
            "total_employees": sum(len(w.get_employees()) for w in self.factory.get_all_workshops()),
            "save_timestamp": datetime.now().isoformat()
        }

        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self._save_log("Сохранение данных", {"data_file": self.data_file})

    def _load_data(self) -> bool:
        """
        Загрузка данных завода из JSON файла.

        Returns:
            True если загрузка прошла успешно, иначе False
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.factory.name = data.get("factory_name", self.factory.name)

            for workshop_data in data.get("workshops", []):
                chief_data = workshop_data["chief"]
                chief = Chief(
                    name=chief_data["name"],
                    surname=chief_data["surname"],
                    age=chief_data["age"],
                    gender=Gender(chief_data["gender"])
                )
                chief._id = chief_data["id"]

                employees = []
                for emp_data in workshop_data.get("employees", []):
                    emp_type = emp_data.get("type", "Worker")

                    if emp_type == "Chief":
                        emp = Chief(
                            name=emp_data["name"],
                            surname=emp_data["surname"],
                            age=emp_data["age"],
                            gender=Gender(emp_data["gender"])
                        )
                    elif emp_type == "Turner":
                        emp = Turner(
                            name=emp_data["name"],
                            surname=emp_data["surname"],
                            age=emp_data["age"],
                            gender=Gender(emp_data["gender"])
                        )
                    elif emp_type == "Locksmith":
                        emp = Locksmith(
                            name=emp_data["name"],
                            surname=emp_data["surname"],
                            age=emp_data["age"],
                            gender=Gender(emp_data["gender"])
                        )
                    elif emp_type == "Miller":
                        emp = Miller(
                            name=emp_data["name"],
                            surname=emp_data["surname"],
                            age=emp_data["age"],
                            gender=Gender(emp_data["gender"])
                        )
                    else:
                        continue

                    emp._id = emp_data["id"]
                    employees.append(emp)

                workshop = WorkShop(workshop_data["name"], chief, employees)
                self.factory.add_workshop(workshop)

            self._save_log("Загрузка данных", {"data_file": self.data_file})
            return True

        except FileNotFoundError:
            return False
        except Exception as e:
            self._save_log("Ошибка загрузки данных", {"error": str(e)})
            return False

    def _create_employee(self) -> Employee:
        """Создание работника через пользовательский ввод."""
        print("\nСоздание нового работника")
        print("-"*20)

        name = input("Имя: ")
        surname = input("Фамилия: ")
        age = int(input("Возраст: "))

        print("Выберите пол:")
        print("1. Мужской")
        print("2. Женский")
        gender_choice = input("Ваш выбор (1-2): ")
        gender = Gender.MALE if gender_choice == "1" else Gender.FEMALE

        print("\nВыберите должность:")
        print("1. Начальник цеха")
        print("2. Токарь")
        print("3. Слесарь")
        print("4. Фрезеровщик")

        role_choice = input("Ваш выбор (1-4): ")

        if role_choice == "1":
            return Chief(name, surname, age, gender)
        elif role_choice == "2":
            return Turner(name, surname, age, gender)
        elif role_choice == "3":
            return Locksmith(name, surname, age, gender)
        elif role_choice == "4":
            return Miller(name, surname, age, gender)
        else:
            print("Неверный выбор, создан работник по умолчанию (Токарь)")
            return Turner(name, surname, age, gender)

    def _manage_workshops(self) -> None:
        """Управление цехами завода."""
        while True:
            print("\n" + "-"*30)
            print("УПРАВЛЕНИЕ ЦЕХАМИ")
            print("-"*30)
            print("1. Создать цех")
            print("2. Просмотреть все цехи")
            print("3. Удалить цех")
            print("4. Назад")
            print("-"*30)

            workshop_choice = input("Ваш выбор (1-4): ")

            if workshop_choice == "1":
                self._create_workshop()

            elif workshop_choice == "2":
                self._view_all_workshops()

            elif workshop_choice == "3":
                self._remove_workshop()

            elif workshop_choice == "4":
                break
            else:
                print("Неверный выбор!")

    def _create_workshop(self) -> None:
        """Создание нового цеха."""
        print("\nСоздание нового цеха")
        name = input("Название цеха: ")

        print("\nСоздание начальника цеха:")
        chief = self._create_employee()
        if not isinstance(chief, Chief):
            print("Ошибка: Начальник цеха должен быть типа 'Начальник цеха'")
            return

        workshop = WorkShop(name, chief)
        self.factory.add_workshop(workshop)
        self._save_log("Создание цеха", {"workshop_name": name, "chief": str(chief)})
        print(f"Цех '{name}' успешно создан!")

    def _view_all_workshops(self) -> None:
        """Просмотр всех цехов завода."""
        workshops = self.factory.get_all_workshops()
        if not workshops:
            print("\nНа заводе нет цехов")
        else:
            print(f"\nЦехи завода '{self.factory.name}':")
            for i, workshop in enumerate(workshops, 1):
                print(f"\n{i}. {workshop}")

    def _remove_workshop(self) -> None:
        """Удаление цеха с завода."""
        name = input("Введите название цеха для удаления: ")
        if self.factory.remove_workshop(name):
            self._save_log("Удаление цеха", {"workshop_name": name})
            print(f"Цех '{name}' успешно удален!")
        else:
            print(f"Цех с названием '{name}' не найден")

    def _manage_employees(self) -> None:
        """Управление работниками цехов."""
        while True:
            print("\n" + "-"*30)
            print("УПРАВЛЕНИЕ РАБОТНИКАМИ")
            print("-"*30)
            print("1. Добавить работника в цех")
            print("2. Удалить работника из цеха")
            print("3. Просмотреть работников цеха")
            print("4. Назад")
            print("-"*30)

            employee_choice = input("Ваш выбор (1-4): ")

            if employee_choice == "1":
                self._add_employee_to_workshop()

            elif employee_choice == "2":
                self._remove_employee_from_workshop()

            elif employee_choice == "3":
                self._view_workshop_employees()

            elif employee_choice == "4":
                break
            else:
                print("Неверный выбор!")

    def _add_employee_to_workshop(self) -> None:
        """Добавление работника в цех."""
        workshop_name = input("Введите название цеха: ")
        workshop = self.factory.get_workshop(workshop_name)

        if workshop:
            employee = self._create_employee()
            workshop += employee
            self._save_log("Добавление работника", {
                "workshop": workshop_name,
                "employee": str(employee),
                "position": employee.get_post()
            })
            print(f"Работник {employee} добавлен в цех '{workshop_name}'")
        else:
            print(f"Цех с названием '{workshop_name}' не найден")

    def _remove_employee_from_workshop(self) -> None:
        """Удаление работника из цеха."""
        workshop_name = input("Введите название цеха: ")
        workshop = self.factory.get_workshop(workshop_name)

        if workshop:
            print(f"\nРаботники цеха '{workshop_name}':")
            employees = workshop.get_employees()
            for i, emp in enumerate(employees, 1):
                print(f"{i}. {emp} ({emp.get_post()})")

            try:
                idx = int(input("\nВведите номер работника для удаления: ")) - 1
                if 0 <= idx < len(employees):
                    employee = employees[idx]
                    workshop.remove_employee(idx)
                    self._save_log("Удаление работника", {
                        "workshop": workshop_name,
                        "employee": str(employee),
                        "position": employee.get_post()
                    })
                    print("Работник успешно удален!")
                else:
                    print("Неверный номер!")
            except ValueError:
                print("Введите число!")
        else:
            print(f"Цех с названием '{workshop_name}' не найден")

    def _view_workshop_employees(self) -> None:
        """Просмотр работников цеха."""
        workshop_name = input("Введите название цеха: ")
        workshop = self.factory.get_workshop(workshop_name)

        if workshop:
            print(f"\n{workshop}")
            print("Список работников:")
            employees = workshop.get_employees()
            for i, emp in enumerate(employees, 1):
                info = emp.get_info()
                role_info = f" ({info.get('role', '')})" if 'role' in info else ""
                print(f"{i}. {emp} - {info['post']}{role_info}")
        else:
            print(f"Цех с названием '{workshop_name}' не найден")

    def _view_factory_state(self) -> None:
        """Просмотр текущего состояния завода."""
        print("\n" + "="*50)
        print(self.factory)

        workshops = self.factory.get_all_workshops()
        if workshops:
            print("\nДетальная информация по цехам:")
            for workshop in workshops:
                print(f"\n{'-'*30}")
                print(workshop)

    def _compare_workshops(self) -> None:
        """Сравнение цехов по распределению работников."""
        workshops = self.factory.get_all_workshops()
        if len(workshops) < 2:
            print("Для сравнения нужно минимум 2 цеха!")
            return

        print("\nСписок цехов:")
        for i, workshop in enumerate(workshops, 1):
            print(f"{i}. {workshop.name}")

        try:
            idx1 = int(input("Введите номер первого цеха: ")) - 1
            idx2 = int(input("Введите номер второго цеха: ")) - 1

            if 0 <= idx1 < len(workshops) and 0 <= idx2 < len(workshops):
                w1 = workshops[idx1]
                w2 = workshops[idx2]

                print(f"\nСравнение цехов '{w1.name}' и '{w2.name}':")

                if w1 == w2:
                    print("Цеха имеют одинаковое распределение работников по классам!")
                else:
                    print("Цеха имеют разное распределение работников по классам!")

                print(f"\nРаспределение в '{w1.name}':")
                for cls, count in w1.get_employee_class_distribution().items():
                    print(f"  {cls}: {count}")

                print(f"\nРаспределение в '{w2.name}':")
                for cls, count in w2.get_employee_class_distribution().items():
                    print(f"  {cls}: {count}")

                self._save_log("Сравнение цехов", {
                    "workshop1": w1.name,
                    "workshop2": w2.name,
                    "are_equal": w1 == w2
                })

            else:
                print("Неверные номера цехов!")
        except ValueError:
            print("Введите числа!")

    def run(self) -> None:
        """Запуск основного цикла меню."""
        if self._load_data():
            print("Данные успешно загружены!")

        while True:
            print("\n" + "="*50)
            print("СИСТЕМА УПРАВЛЕНИЯ ЗАВОДОМ")
            print("="*50)
            print("1. Управление цехами")
            print("2. Управление работниками")
            print("3. Сохранить данные")
            print("4. Загрузить данные")
            print("5. Просмотр состояния завода")
            print("6. Сравнение цехов")
            print("7. Выход")
            print("="*50)

            choice = input("Ваш выбор (1-7): ")

            if choice == "1":
                self._manage_workshops()

            elif choice == "2":
                self._manage_employees()

            elif choice == "3":
                self._save_data()
                print("Данные успешно сохранены!")

            elif choice == "4":
                if self._load_data():
                    print("Данные успешно загружены!")
                else:
                    print("Ошибка при загрузке данных!")

            elif choice == "5":
                self._view_factory_state()

            elif choice == "6":
                self._compare_workshops()

            elif choice == "7":
                save = input("Сохранить данные перед выходом? (y/n): ")
                if save.lower() == 'y':
                    self._save_data()
                    print("Данные сохранены!")
                print("До свидания!")
                break

            else:
                print("Неверный выбор! Попробуйте снова.")
