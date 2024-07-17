from pathlib import Path
from typing import List, Optional, Type, Union

from pydantic import DirectoryPath, FilePath

from geolib.models.base_model import BaseModel
from geolib.models.base_model_structure import BaseDataClass
from geolib.models.dseries_parser import DSeriesStructure
from geolib.models.dsettlement.dsettlement_parserprovider import (
    DSettlementParserProvider,
)


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


class DummyModel(BaseModel):
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
    ]  # Changing this into List[BaseModel] will cause the test to fail
    base_models: List[BaseModel]
    errors: List[str] = []
