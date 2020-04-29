from geolib.models import BaseValidator
import logging


class DStabilityValidator(BaseValidator):
    """Validator for DStability structure.
    
    Has access to self.ds from parent class.
    Will run all is_valid_ functions to check for validity."""

    def is_valid_stages(self) -> bool:
        """Number of stages should be the same:"""
        lengths_set = set()
        valid = True
        for key, value in ((k, v) for k, v in self.ds.dict().items() if 'result' not in k):  # Results not required for stage validity.
            if isinstance(value, list):
                lengths_set.add(len(value))
                if len(lengths_set) > 1:
                    logging.error(
                        f"{self.is_valid_stages.__doc__} {key} has different number of stages: {len(value)}."
                    )
                    valid = False
                    break

        return valid
