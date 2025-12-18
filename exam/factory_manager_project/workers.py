from typing import Dict, Any

from employees import Worker, Gender

class Turner(Worker):
    """Класс токаря."""

    def __init__(self, name: str, surname: str, age: int, gender: Gender):
        """
        Инициализация токаря.

        Args:
            name: Имя токаря
            surname: Фамилия токаря
            age: Возраст токаря
            gender: Пол токаря
        """
        super().__init__(name, surname, age, gender)
        self.__role = "Токарь"

    def get_role(self) -> str:
        """Получение специализации токаря."""
        return self.__role

    def get_info(self) -> Dict[str, Any]:
        """
        Получение информации о токаре.

        Returns:
            Словарь с информацией о токаре
        """
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

class Locksmith(Worker):
    """Класс слесаря."""

    def __init__(self, name: str, surname: str, age: int, gender: Gender):
        """
        Инициализация слесаря.

        Args:
            name: Имя слесаря
            surname: Фамилия слесаря
            age: Возраст слесаря
            gender: Пол слесаря
        """
        super().__init__(name, surname, age, gender)
        self.__role = "Слесарь"

    def get_role(self) -> str:
        """Получение специализации слесаря."""
        return self.__role

    def get_info(self) -> Dict[str, Any]:
        """
        Получение информации о слесаре.

        Returns:
            Словарь с информацией о слесаре
        """
        info = super().get_info()
        info["role"] = self.__role
        return info


class Miller(Worker):
    """Класс фрезеровщика."""

    def __init__(self, name: str, surname: str, age: int, gender: Gender):
        """
        Инициализация фрезеровщика.

        Args:
            name: Имя фрезеровщика
            surname: Фамилия фрезеровщика
            age: Возраст фрезеровщика
            gender: Пол фрезеровщика
        """
        super().__init__(name, surname, age, gender)
        self.__role = "Фрезеровщик"

    def get_role(self) -> str:
        """Получение специализации фрезеровщика."""
        return self.__role

    def get_info(self) -> Dict[str, Any]:
        """
        Получение информации о фрезеровщике.

        Returns:
            Словарь с информацией о фрезеровщике
        """
        info = super().get_info()
        info["role"] = self.__role
        return info