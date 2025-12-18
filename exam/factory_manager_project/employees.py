from abc import ABC, abstractmethod
from typing import Dict, Any
from enum import Enum
import uuid

class Gender(Enum):
    """Перечисление для представления пола работника."""

    FEMALE = "female"
    MALE = "male"

class Employee(ABC):
    """Абстрактный базовый класс для всех работников."""
    def __init__(self, name, surname, age, gender: Gender):
        """
        Инициализация работника.

        Args:
            name: Имя работника
            surname: Фамилия работника
            age: Возраст работника
            gender: Пол работника
        """
        self.__id = str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender

    def __str__(self):
        """Строковое представление работника."""
        return f"{self.name} {self.surname}"

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Получение полной информации о работнике."""
        pass

    @abstractmethod
    def get_post(self):
        """Получение должности работника."""
        pass

    def get_id(self):
        """Получение уникального идентификатора работника."""
        return self.__id

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта работника в словарь."""
        info = self.get_info()
        info["type"] = self.__class__.__name__
        return info


class Chief(Employee):
    """Класс начальника цеха."""

    def __init__(self, name: str, surname: str, age: int, gender: Gender):
        """
        Инициализация начальника цеха.

        Args:
            name: Имя начальника
            surname: Фамилия начальника
            age: Возраст начальника
            gender: Пол начальника
        """
        super().__init__(name, surname, age, gender)
        self.__post = "Начальник цеха"

    def get_post(self):
        """Получение должности начальника."""
        return self.__post

    def get_info(self) -> Dict[str, Any]:
        """
        Получение информации о начальнике цеха.

        Returns:
            Словарь с информацией о начальнике
        """
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
    """Абстрактный класс рабочего."""

    def __init__(self, name: str, surname: str, age: int, gender: Gender):
        """
        Инициализация рабочего.

        Args:
            name: Имя рабочего
            surname: Фамилия рабочего
            age: Возраст рабочего
            gender: Пол рабочего
        """
        super().__init__(name, surname, age, gender)
        self.__post = "Рабочий"

    def get_post(self) -> str:
        """Получение должности рабочего."""
        return self.__post

    @abstractmethod
    def get_role(self) -> str:
        """Получение специализации рабочего."""
        pass
