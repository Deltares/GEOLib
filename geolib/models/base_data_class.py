from pydantic import BaseModel

from geolib._compat import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict

from .meta import MetaData

settings = MetaData()


class BaseDataClass(BaseModel):
    """Base class for *all* pydantic classes in GEOLib."""

    if IS_PYDANTIC_V2:
        model_config = ConfigDict(
            validate_assignment=True,
            arbitrary_types_allowed=True,
            validate_default=True,
            extra=settings.extra_fields,
        )
    else:

        class Config:
            validate_assignment = True
            arbitrary_types_allowed = True
            validate_all = True
            extra = settings.extra_fields
