import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid

class Gender(Enum):
    f = "female"
    m = "male"

class Employee(ABC):
    def __init__(self, name, surname, age, gender: Gender):
        self.__id = uuid.uuid4()
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.name} {self.surname}"

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_post(self):
        pass

    def get_id(self):
        return self.__id


class Chief(Employee):
    __post = "Начальник Цеха"

    def __init__(self, name, surname, age, gender: Gender):
        super().__init__(name, surname, age, gender)

    def get_post(self):
        return self.__post

    def get_info(self) -> Dict[str, Any]:
        """Получение информации о работнике"""
        info = {
            "id": self.get_id(),
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "gender": self.gender.value,
            "post": self.__post
        }
        return info

class Worker(Employee, ABC):
    __post = "Рабочий"

    def __init__(self, name, surname, age, gender):
        super().__init__(name, surname, age, gender)

    def get_post(self):
        return self.__post

    @abstractmethod
    def get_role(self):
        pass

class Turner(Worker):
    __role = "Токарь"

    def __init__(self, name, surname, age, gender):
        super().__init__(name, surname, age, gender)

    def get_role(self):
        return self.__role

    def get_info(self) -> Dict[str, Any]:
        """Получение информации о работнике"""
        info = {
            "id": str(self.get_id()),
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "gender": self.gender.value,
            "post": self.get_post(),
            "role": self.__role
        }
        return info

class WorkShop():
    def __init__(self, name, chief: Chief, employees: List[Employee] = []):
        self.name = name
        self.__chief = chief
        self.__employees = employees

    def get_emloyees(self) -> List[Employee]:
        return self.__employees

    def del_employees(self) -> None:
        self.__employees = []

    def get_emloyee(self, n) -> Employee:
        if isinstance(n, int):
            return self.__employees[n]
        elif isinstance(n, str):
            for employee in self.__employees:
                if employee.get_id() == n:
                    return employee

    def __add__(self, other):
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            new_workshop = WorkShop(self.name, self.__chief, self.get_emloyees().extend(other))
            return new_workshop
        if isinstance(other, Employee):
            new_workshop = WorkShop(self.name, self.__chief, self.get_emloyees().append(other))
            return new_workshop
        else:
            raise Exception("Workshop can only be folded with Employee")

    def __iadd__(self, other):
        if isinstance(other, List) and all(isinstance(i, Employee) for i in other):
            self.__employees.extend(other.get_emloyees)
        if isinstance(other, Employee):
            self.__employees.append(other)
        else:
            raise Exception("Workshop can only be folded with Employee")

    def __sub__(self, other):
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
            raise Exception("Workshop can only be subtracked with Employee")

    def __isub__(self, other):
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
            raise Exception("Workshop can only be subtracked with Employee")

    def __str__(self) -> str:
        result = f"Цех: {self.name}\n"
        result += f"Начальник цеха: {self.__chief}\n"
        result += f"Количество работников: {len(self.__employees)}\n"
        return result

    def __eq__(self, value):
        if isinstance(value, int):
            return (len(self.__employees) == value)
        if isinstance(value, WorkShop):
            res = True
            if self.name != value.name or self.__chief != value.get_chief()\
                                    or self.__employees == value.get_emloyees():
                res = False
            return res


    def get_chief(self):
        return self.__chief

class Factory():
    def __init__(self):
        pass
    def save_data(self):
        """Saving Data in JSON format"""
        pass

if __name__ == "__main__":
    c = Turner("la", "la", 23, Gender.f)
    w = WorkShop("test", c)
    # print(c.get_info())
    print(w)