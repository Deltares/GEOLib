from abc import ABCMeta, abstractmethod
from datetime import datetime
from io import BytesIO
from os import makedirs
from typing import Dict, List, Union, _GenericAlias, get_type_hints
from zipfile import ZIP_DEFLATED, ZipFile

from pydantic import DirectoryPath, FilePath
from zipp import Path

from geolib.errors import NotConcreteError
from geolib.models.serializers import BaseSerializer
from geolib.models.utils import get_filtered_type_hints

from .internal import DStabilityStructure


class DStabilityBaseSerializer(BaseSerializer, metaclass=ABCMeta):
    """Serializer to folder/file structure."""

    ds: DStabilityStructure

    def serialize(self) -> Dict:
        serialized_datastructure: Dict = {}

        for field, fieldtype in get_filtered_type_hints(self.ds):
            # On List types, write a folder
            if type(fieldtype) == _GenericAlias:  # quite hacky
                element_type, *_ = fieldtype.__args__  # use getargs in 3.8

                folder = element_type.structure_group()
                serialized_datastructure[folder] = {}

                for i, data in enumerate(getattr(self.ds, field)):
                    suffix = f"_{i}" if i > 0 else ""
                    fn = element_type.structure_name() + suffix + ".json"
                    serialized_datastructure[folder][fn] = data.json(indent=4)

            # Otherwise its a single .json in the root folder
            else:
                fn = fieldtype.structure_name() + ".json"
                data = getattr(self.ds, field)
                serialized_datastructure[fn] = data.json(indent=4)

        return serialized_datastructure

    @abstractmethod
    def write(self, path):
        raise NotConcreteError


class DStabilityInputSerializer(DStabilityBaseSerializer):
    def write(self, filepath: DirectoryPath) -> DirectoryPath:
        serialized_datastructure = self.serialize()

        for filename, data in serialized_datastructure.items():

            if isinstance(data, dict):
                folder = filepath / filename
                folder.mkdir(parents=True, exist_ok=True)

                for ffilename, fdata in data.items():
                    fn = folder / ffilename
                    with fn.open("wb") as io:
                        io.write(fdata.encode("utf-8"))
            else:
                fn = filepath / filename
                with fn.open("wb") as io:
                    io.write(data.encode("utf-8"))

        return filepath


class DStabilityInputZipSerializer(DStabilityBaseSerializer):
    """DStabilSerializer for zipped.stix files."""

    def write(self, filepath: Union[FilePath, BytesIO]) -> Union[FilePath, BytesIO]:
        with ZipFile(filepath, mode="w", compression=ZIP_DEFLATED) as zip:
            serialized_datastructure = self.serialize()

            for filename, data in serialized_datastructure.items():

                if isinstance(data, dict):
                    folder = filename
                    for ffilename, fdata in data.items():
                        fn = folder + "/" + ffilename
                        with zip.open(fn, "w") as io:
                            io.write(fdata.encode("utf-8"))
                else:
                    with zip.open(filename, "w") as io:
                        io.write(data.encode("utf-8"))

            for zfile in zip.filelist:
                zfile.create_system = 0

        return filepath
