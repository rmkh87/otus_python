import re

from typing import Union, Any
from abc import ABC, abstractmethod
from datetime import datetime


class ValidateField(ABC):
    def __init__(self, **kwargs):
        pass

    def __set_name__(self, owner, name: str):
        self.name = name

    @abstractmethod
    def validate(self, value) -> tuple[bool, Union[Any, None], Union[ValueError, None]]:
        return True, value, None


class ValidateRequiredField(ValidateField):
    class RequiredFieldNoneValue:
        """ Класс для идентификации обязательного None значения"""
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__required = kwargs.get('required', False)

    def validate(self, value: Union[Any, None]) -> tuple[bool, Union[Any, None], Union[ValueError, None]]:
        """ Валидация значения """
        if self.__required and type(value) == self.RequiredFieldNoneValue:
            return False, None, ValueError(f'{self.name} is required value')
        elif type(value) == self.RequiredFieldNoneValue:
            return super().validate(None)
        return super().validate(value)


class ValidateNullableField(ValidateField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__nullable = kwargs.get('nullable', False)

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not self.__nullable and (value is None or not value):
            return False, None, ValueError(f'{self.name} is nullable value')
        return super().validate(value)


class ValidateCharField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not type(value) == str:
            return False, value, ValueError(f'{self.name} is not str type')
        return super().validate(value)


class ValidateEmailField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not value or not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value):
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)


class ValidatePhoneField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not value or not re.fullmatch(r"^7[0-9]{10}$", str(value)):
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)


class ValidateDateField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not re.fullmatch(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$', value):
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)


class ValidateBirthDayField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not re.fullmatch(r'^(3[01]|[12][0-9]|0[1-9]).(1[0-2]|0[1-9]).[0-9]{4}$', value):
            return False, value, ValueError(f'{self.name} is not valid')

        diff = datetime.now().date() - datetime.strptime(value, "%d.%m.%Y").date()
        if diff.days > 365*70:
            return False, value, ValueError(f'{self.name} is not valid')

        return super().validate(value)


class ValidateGenderField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if value not in [0, 1, 2]:
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)


class ValidateIdsField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not type(value) == list or (type(value) == list and any([type(item) != int for item in value])):
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)


class ValidateDictField(ValidateField):
    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        """ Валидация значения """
        if not value:
            return super().validate(value)

        if not type(value) == dict:
            return False, value, ValueError(f'{self.name} is not valid')
        return super().validate(value)
