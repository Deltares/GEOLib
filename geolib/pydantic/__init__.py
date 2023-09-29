"""This is a compatibility module to accept both pydantic v1 and v2."""

from pydantic.version import VERSION

PYDANTIC_V2 = VERSION.startswith("2.")

pydanticv1_loaded = False
if PYDANTIC_V2:
    from pydantic.v1 import BaseModel, ValidationError, root_validator, validator

    pydanticv1_loaded = True
else:
    from pydantic import BaseModel, ValidationError, root_validator, validator
