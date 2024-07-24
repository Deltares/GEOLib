import abc

from pydantic import BaseModel, ConfigDict

from .meta import MetaData
from .validators import BaseValidator

settings = MetaData()


class BaseDataClass(BaseModel):
    """Base class for *all* pydantic classes in GEOLib."""

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        extra=settings.extra_fields,
    )


class BaseModelStructure(BaseDataClass, abc.ABC):
    @property
    def is_valid(self) -> bool:
        """Validates the current model structure."""
        return self.validator().is_valid

    def validator(self) -> BaseValidator:
        """Set the Validator class."""
        return BaseValidator(self)
