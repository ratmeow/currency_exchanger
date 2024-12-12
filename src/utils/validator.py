from .exceptions import ServiceValidationError
from typing import Union, Any


class FieldValidator:
    @staticmethod
    def check_empty_field(value: str, field_name: str):
        if len(value) == 0:
            raise ServiceValidationError(message=f"{field_name} must be filled")

    @staticmethod
    def check_field_only_letters(value: str, field_name: str):
        if not all(list(map(str.isalpha, value.split(" ")))):
            raise ServiceValidationError(message=f"{field_name} [{value}] has extra characters or digits")

    @staticmethod
    def check_length_match(value: str, length: int, field_name: str):
        if len(value) != length:
            raise ServiceValidationError(message=f"{field_name} [{value}] must be {length} characters long")

    @staticmethod
    def check_field_not_negative(value: Union[int, float], field_name: str):
        if value < 0:
            raise ServiceValidationError(message=f"{field_name} must be grater than 0")

    @staticmethod
    def check_field_numeric(value: Any, field_name: str):
        try:
            int(value)
        except ValueError:
            raise ServiceValidationError(message=f"{field_name} must be numeric")

    @classmethod
    def check_combined_code(cls, value: str, field_name: str):
        cls.check_length_match(value=value, field_name=field_name, length=6)
        cls.check_field_only_letters(value=value, field_name=field_name)
