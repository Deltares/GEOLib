import abc
from datetime import date, datetime

from pydantic import field_validator

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

    @classmethod
    def nltime(cls, date_input: date | str) -> date:
        """Parse date from multiple formats: DD-MM-YYYY, YYYY-MM-DD, or ISO with time.
        
        Handles:
        - ISO format with time: YYYY-MM-DDTHH:MM:SS
        - Dutch format: DD-MM-YYYY
        - ISO format: YYYY-MM-DD
        """
        if isinstance(date_input, str):
            # Handle ISO format with time component (YYYY-MM-DDTHH:MM:SS)
            if "T" in date_input:
                date_input = datetime.fromisoformat(date_input).date()
            else:
                # Handle DD-MM-YYYY and YYYY-MM-DD formats
                position = date_input.index(max(date_input.split("-"), key=len))
                if position > 0:
                    date_input = datetime.strptime(date_input, "%d-%m-%Y").date()
                else:
                    date_input = datetime.strptime(date_input, "%Y-%m-%d").date()
        return date_input
