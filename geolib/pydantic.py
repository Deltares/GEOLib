import sys

from pydantic.version import VERSION

PYDANTIC_V2 = VERSION.startswith("2.")


if PYDANTIC_V2:
    from pydantic.v1 import BaseModel, ValidationError, root_validator
    from pydantic.v1 import types as types
    from pydantic.v1 import validator
else:
    from pydantic import BaseModel, ValidationError, root_validator
    from pydantic import types as types
    from pydantic import validator

sys.modules["geolib.pydantic.types"] = types
