import abc

from geolib.models.base_data_class import BaseDataClass

from .validators import BaseValidator


class BaseModelStructure(BaseDataClass, abc.ABC):
    @property
    def is_valid(self) -> bool:
        """Validates the current model structure."""
        return self.validator().is_valid

    def validator(self) -> BaseValidator:
        """Set the Validator class."""
        return BaseValidator(self)
