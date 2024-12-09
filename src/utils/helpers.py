from .exceptions import ServiceValidationError


class ServiceHelper:

    @classmethod
    def check_string_is_all_alpha(cls, value: str):
        return all(list(map(str.isalpha, value.split(" "))))

    @classmethod
    def check_combined_code(cls, value: str):
        if len(value) != 6:
            raise ServiceValidationError(message=f"[{value}] must be 6 characters long(2 codes together)")
        if not cls.check_string_is_all_alpha(value=value):
            raise ServiceValidationError(message=f"Currency codes has extra characters or digits")

    @classmethod
    def check_rate(cls, value: float):
        if value < 0:
            raise ServiceValidationError(message=f"Rate mist be grater than 0")
