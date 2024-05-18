class BaseCustomException(Exception):
    """A base class for all BaseCustomException"""

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return self.message


class ServiceModelClassDidNotSetException(BaseCustomException):
    ...
