import abc
from math import isfinite

from pydantic import BaseModel as DataClass

from .validators import BaseValidator


class BaseModelStructure(DataClass, abc.ABC):
    @property
    def is_valid(self) -> bool:
        """ Validates the current model structure. """
        return self.validator().is_valid

    def validator(self) -> BaseValidator:
        """Set the Validator class."""
        return BaseValidator(self)

    class Config:
        extra = "forbid"
        arbitrary_types_allowed = False
        validate_on_assignment = True
