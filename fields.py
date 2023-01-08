from typing import Union
from weakref import WeakKeyDictionary
from validators import (
    ValidateRequiredField,
    ValidateNullableField,
    ValidateCharField,
    ValidateEmailField,
    ValidatePhoneField,
    ValidateDateField,
    ValidateBirthDayField,
    ValidateGenderField,
    ValidateIdsField,
    ValidateDictField,
)


class CharField(ValidateRequiredField, ValidateNullableField, ValidateCharField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class EmailField(CharField, ValidateEmailField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class PhoneField(ValidateRequiredField, ValidateNullableField, ValidatePhoneField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class DateField(ValidateRequiredField, ValidateNullableField, ValidateDateField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class BirthDayField(ValidateRequiredField, ValidateNullableField, ValidateBirthDayField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class GenderField(ValidateRequiredField, ValidateNullableField, ValidateGenderField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class ClientIDsField(ValidateRequiredField, ValidateNullableField, ValidateIdsField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate


class ArgumentsField(ValidateRequiredField, ValidateNullableField, ValidateDictField):
    def __init__(
            self,
            required: bool = False,
            nullable: bool = False,
    ):
        super().__init__(required=required, nullable=nullable)

        self.__data = WeakKeyDictionary()

    def __get__(self, instance, cls):
        return self.__data.get(instance, None)

    def __set__(self, instance, value: Union[str, None]):
        is_valid, value, error = self.__validate(value)
        if not is_valid:
            raise error

        self.__data[instance] = value

    def validate(self, value: Union[str, None]) -> tuple[bool, Union[str, None], Union[ValueError, None]]:
        return super().validate(value)

    __validate = validate
