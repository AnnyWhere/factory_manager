from typing import Any, List, Dict, Optional, Union

from employees import Chief, Employee, Worker

class WorkShop():
    """Класс цеха."""
    def __init__(self, name, chief: Chief, employees: List[Employee] = []):
        """
        Инициализация цеха.

        Args:
            name: Название цеха
            chief: Начальник цеха
            employees: Список работников цеха
        """
        self.name = name
        self.__chief = chief
        self.__employees = employees

    def get_employees(self) -> List[Employee]:
        """Получение списка всех работников цеха."""
        return self.__employees.copy()

    def del_employees(self) -> None:
        """Очистка списка работников цеха."""
        self.__employees = []

    def remove_employee(self, identifier: Union[int, str]) -> bool:
        """
        Удаление работника из цеха.

        Args:
            identifier: Индекс работника в списке или его ID

        Returns:
            True если удаление прошло успешно, иначе False
        """
        if isinstance(identifier, int) and 0 <= identifier < len(self.__employees):
            self.__employees.pop(identifier)
            return True
        elif isinstance(identifier, str):
            for i, employee in enumerate(self.__employees):
                if employee.get_id() == identifier:
                    self.__employees.pop(i)
                    return True
        return False

    def get_emloyee(self, n) -> Optional[Employee]:
        """
        Получение работника по индексу или ID.

        Args:
            identifier: Индекс работника в списке или его ID

        Returns:
            Найденный работник или None
        """
        if isinstance(n, int):
            return self.__employees[n]
        elif isinstance(n, str):
            for employee in self.__employees:
                if employee.get_id() == n:
                    return employee

    def __add__(self, other):
        """
        Сложение цеха с работником или списком работников.

        Args:
            other: Работник или список работников

        Returns:
            Новый цех с добавленными работниками
        """
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            new_workshop = WorkShop(self.name, self.__chief, self.get_employees().extend(other))
            return new_workshop
        if isinstance(other, Employee):
            new_workshop = WorkShop(self.name, self.__chief, self.get_employees().append(other))
            return new_workshop
        else:
            raise TypeError("Workshop can only be added with Employee or list of Employees")

    def __iadd__(self, other):
        """
        Добавление работника или списка работников к цеху.

        Args:
            other: Работник или список работников

        Returns:
            Текущий цех с добавленными работниками
        """
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            self.__employees.extend(other.get_employees())
        if isinstance(other, Employee):
            self.__employees.append(other)
        else:
            raise TypeError("Workshop can only be added with Employee or list of Employees")

    def __sub__(self, other):
        """
        Вычитание работника или списка работников из цеха.

        Args:
            other: Работник или список работников для удаления

        Returns:
            Новый цех без удаленных работников
        """
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            ids = [i.get_id for i in other]
            employees = []
            for employee in self.__employees:
                if not employee.get_id() in ids:
                    employees.append(employee)
            return WorkShop(self.name, self.__chief, employees)
        if isinstance(other, Employee):
            employees = []
            for employee in self.__employees:
                if not employee.get_id() == other.get_id():
                    employees.append(employee)
            return WorkShop(self.name, self.__chief, employees)
        else:
            raise TypeError("Workshop can only be subtracted with Employee or list of Employees")

    def __isub__(self, other):
        """
        Удаление работника или списка работников из цеха.

        Args:
            other: Работник или список работников для удаления

        Returns:
            Текущий цех без удаленных работников
        """
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            ids = [i.get_id for i in other]
            for i, employee in enumerate(self.__employees):
                if employee.get_id() in ids:
                    self.__employees.pop(i)
        if isinstance(other, Employee):
            for i, employee in enumerate(self.__employees):
                if employee.get_id() == other.get_id():
                    self.__employees.pop(i)
                    break
        else:
            raise TypeError("Workshop can only be subtracted with Employee or list of Employees")

    def get_employees_by_role(self) -> Dict[str, int]:
        """Получение распределения работников по специализациям."""
        distribution = {}
        for employee in self.__employees:
            if isinstance(employee, Worker):
                role = employee.get_role()
                distribution[role] = distribution.get(role, 0) + 1
            else:
                post = employee.get_post()
                distribution[post] = distribution.get(post, 0) + 1
        return distribution

    def __str__(self) -> str:
        """Строковое представление цеха."""
        employees_by_role = self.get_employees_by_role()

        result = f"Цех: {self.name}\n"
        result += f"Начальник: {self.__chief}\n"
        result += f"Общее количество работников: {len(self.__employees)}\n"

        for role, count in employees_by_role.items():
            result += f"  {role}: {count}\n"

        return result

    def __eq__(self, value):
        """
        Сравнение цехов по количеству работников каждого класса.

        Args:
            other: Цех для сравнения или число

        Returns:
            True если равны, иначе False
        """
        if isinstance(value, int):
            return (len(self.__employees) == value)
        if isinstance(value, WorkShop):
            self_dist = self.get_employee_class_distribution()
            other_dist = value.get_employee_class_distribution()

            return self_dist == other_dist
        return False

    def get_employee_class_distribution(self) -> Dict[str, int]:
        """Получение распределения работников по классам."""
        distribution = {}
        for employee in self.__employees:
            class_name = employee.__class__.__name__
            distribution[class_name] = distribution.get(class_name, 0) + 1
        return distribution

    def get_chief(self):
        """Получение начальника цеха."""
        return self.__chief

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование цеха в словарь."""
        return {
            "name": self.name,
            "chief": self.__chief.to_dict(),
            "employees": [e.to_dict() for e in self.__employees],
            "employee_count": len(self.__employees),
            "distribution": self.get_employees_by_role()
        }