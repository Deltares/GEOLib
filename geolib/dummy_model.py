import abc
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel

from geolib._compat import IS_PYDANTIC_V2
from geolib.models.meta import MetaData

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict
settings = MetaData()

### BASE MODEL STRUCTURE


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


class BaseModelStructure(BaseDataClass, abc.ABC):
    pass


class GeolibBaseModel(BaseDataClass, abc.ABC):
    filename: Optional[Path] = None
    datastructure: Optional[
        Union[BaseModelStructure]
    ] = None  # Adding DummyStructure in Union here would cause circular dependencies in the real application


### DUMMY MODEL STRUCTURE


class DummyStructure(BaseModelStructure):
    input_data: BaseModelStructure = BaseModelStructure()
    output_data: Optional[BaseModelStructure] = None


class DummyModel(GeolibBaseModel):
    filename: Optional[Path] = None
    datastructure: DummyStructure = DummyStructure()


class DummyModelList(BaseDataClass):
    dummy_models: List[
        DummyModel
    ]  # Changing this into List[DummyBaseModel] will cause the test to fail
    base_models: List[GeolibBaseModel]
    errors: List[str] = []
