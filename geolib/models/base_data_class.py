from pydantic import BaseModel, ConfigDict

from .meta import MetaData

settings = MetaData()


class BaseDataClass(BaseModel):
    """Base class for *all* pydantic classes in GEOLib."""

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        validate_default=True,
        ser_json_inf_nan='constants',
        extra=settings.extra_fields,
    )
