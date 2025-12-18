from datetime import datetime
import json
import os
from typing import List, Dict, Any, Optional

from employees import Gender, Chief
from workshop import WorkShop
from workers import *

class Factory():
    """Класс завода."""
    def __init__(self, name: str = "Завод"):
        """
        Инициализация завода.

        Args:
            name: Название завода
        """
        self.name = name
        self.__workshops: List[WorkShop] = []
        self.__log_file = "factory_log.json"
        self.__data_file = "factory_data.json"
        if not os.path.exists(self.__log_file):
            self.__save_log("Инициализация завода", {"name": name})
        if not os.path.exists(self.__data_file):
            self.save_data()

    def add_workshop(self, workshop: WorkShop) -> None:
        """
        Добавление цеха на завод.

        Args:
            workshop: Цех для добавления
        """
        self.__workshops.append(workshop)
        self.__save_log("Добавление цеха", {"workshop_name": workshop.name})

    def remove_workshop(self, workshop_name: str) -> bool:
        """
        Удаление цеха с завода.

        Args:
            workshop_name: Название цеха для удаления

        Returns:
            True если удаление прошло успешно, иначе False
        """
        for i, workshop in enumerate(self.__workshops):
            if workshop.name == workshop_name:
                self.__workshops.pop(i)
                self.__save_log("Удаление цеха", {"workshop_name": workshop_name})
                return True
        return False

    def get_workshop(self, name: str) -> Optional[WorkShop]:
        """
        Получение цеха по имени.

        Args:
            name: Название цеха

        Returns:
            Найденный цех или None
        """
        for workshop in self.__workshops:
            if workshop.name == name:
                return workshop
        return None

    def get_all_workshops(self) -> List[WorkShop]:
        """Получение списка всех цехов."""
        return self.__workshops.copy()

    def save_data(self):
        """Сохранение данных завода в JSON файл."""
        data = {
            "factory_name": self.name,
            "workshops": [w.to_dict() for w in self.__workshops],
            "total_workshops": len(self.__workshops),
            "total_employees": sum(len(w.get_employees()) for w in self.__workshops),
            "save_timestamp": datetime.now().isoformat()
        }

        with open(self.__data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.__save_log("Сохранение данных", {"data_file": self.__data_file})

    def load_data(self) -> bool:
        """
        Загрузка данных завода из JSON файла.

        Returns:
            True если загрузка прошла успешно, иначе False
        """
        try:
            with open(self.__data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.name = data.get("factory_name", self.name)
            self.__workshops = []

            for workshop_data in data.get("workshops", []):
                chief_data = workshop_data["chief"]
                chief = Chief(
                    name=chief_data["name"],
                    surname=chief_data["surname"],
                    age=chief_data["age"],
                    gender=Gender(chief_data["gender"])
                )
                chief.__id = chief_data["id"]

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

                    emp.__id = emp_data["id"]
                    employees.append(emp)

                workshop = WorkShop(workshop_data["name"], chief, employees)
                self.__workshops.append(workshop)

            self.__save_log("Загрузка данных", {"data_file": self.__data_file})
            return True

        except FileNotFoundError:
            return False
        except Exception as e:
            self.__save_log("Ошибка загрузки данных", {"error": str(e)})
            return False

    def __save_log(self, action: str, details: Dict[str, Any]) -> None:
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
        if os.path.exists(self.__log_file):
            try:
                with open(self.__log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_entry)

        with open(self.__log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def __str__(self) -> str:
        """Строковое представление завода."""
        result = f"Завод: {self.name}\n"
        result += f"Количество цехов: {len(self.__workshops)}\n"

        total_employees = 0
        for workshop in self.__workshops:
            employees_count = len(workshop.get_employees())
            total_employees += employees_count
            result += f"\n{workshop.name}: {employees_count} работников"

        result += f"\n\nВсего работников на заводе: {total_employees}"
        return result
