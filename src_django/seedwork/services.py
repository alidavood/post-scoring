from seedwork.exceptions import ServiceModelClassDidNotSetException
from seedwork.models import BaseModel


class AbstractService:
    model_class: BaseModel = None

    @classmethod
    def _get_model_class(cls) -> BaseModel:
        if not cls.model_class:
            raise ServiceModelClassDidNotSetException(
                "Please set the model_class value"
            )
        return cls.model_class
