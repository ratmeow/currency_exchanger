from typing import Any


class ServiceError(Exception):
    def __init__(self, message: str = ""):
        self.message = message


class UniqueError(ServiceError):
    pass


class DatabaseInternalError(ServiceError):
    def __init__(self):
        super().__init__(message="Database Internal Error")


class DatabaseNotFoundError(ServiceError):
    pass


class ServiceValidationError(ServiceError):
    pass
