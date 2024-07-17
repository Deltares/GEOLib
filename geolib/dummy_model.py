import abc
from pathlib import Path
from typing import List, Optional, Type, Union

from pydantic import BaseModel, DirectoryPath, FilePath

from geolib._compat import IS_PYDANTIC_V2
from geolib.models.dsettlement.dsettlement_parserprovider import (
    DSettlementParserProvider,
)
from geolib.models.meta import MetaData

if IS_PYDANTIC_V2:
    from pydantic import ConfigDict
settings = MetaData()


class BaseValidator:
    def __init__(self, ds):
        self.ds = ds

    @property
    def is_valid(self) -> bool:
        return all(
            [
                getattr(self, func)()
                for func in dir(self)
                if (func.startswith("is_valid_"))
            ]
        )


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
    @property
    def is_valid(self) -> bool:
        """Validates the current model structure."""
        return self.validator().is_valid

    def validator(self) -> BaseValidator:
        """Set the Validator class."""
        return BaseValidator(self)


class DSeriesStructure(BaseModelStructure):
    pass


class Results(DSeriesStructure):
    dummy: str = ""


class DummyInputStructure(DSeriesStructure):
    dummy: str = ""


class DummyOutputStructure(DSeriesStructure):
    results: Results
    input_data: DummyInputStructure


class DummyStructure(DSeriesStructure):
    input_data: DummyInputStructure = DummyInputStructure()
    output_data: Optional[Results] = None


class DummyBaseModel(BaseDataClass, abc.ABC):
    filename: Optional[Path] = None
    datastructure: Optional[BaseModelStructure] = None


class DummyModel(DummyBaseModel):
    filename: Optional[Path] = None
    datastructure: Union[DummyStructure, DummyOutputStructure] = DummyStructure()

    @property
    def parser_provider_type(self) -> Type[DSettlementParserProvider]:
        pass

    def serialize(
        self, filename: Union[FilePath, DirectoryPath, None]
    ) -> Union[FilePath, DirectoryPath, None]:
        pass


class DummyModelList(BaseDataClass):
    dummy_models: List[
        DummyModel
    ]  # Changing this into List[DummyBaseModel] will cause the test to fail
    base_models: List[DummyBaseModel]
    errors: List[str] = []
