import logging
from datetime import datetime
from pydantic import DirectoryPath
from typing import _GenericAlias, get_type_hints, List
from os import makedirs

from geolib.models.serializers import BaseSerializer
from .internal import DStabilityInputStructure


class DStabilityInputSerializer(BaseSerializer):
    """Test"""

    ds: DStabilityInputStructure

    def write(self, filepath: DirectoryPath):

        # Find required .json files via type hints
        for field, fieldtype in get_type_hints(type(self.ds)).items():
            print(field, fieldtype)
            # On List types, write a folder
            if type(fieldtype) == _GenericAlias:  # quite hacky
                element_type, *_ = fieldtype.__args__  # use getargs in 3.8
                self.write_folder(field, element_type, filepath)

            # Otherwise its a single .json in the root folder
            else:
                fn = filepath / (fieldtype.structure_name() + ".json")
                with open(fn, "w") as io:
                    data = getattr(self.ds, field)
                    io.write(data.json(indent=4))

    def write_folder(self, field, fieldtype, filepath):

        folder = filepath / fieldtype.structure_group()
        makedirs(folder, exist_ok=True)

        for i, data in enumerate(getattr(self.ds, field)):
            suffix = f"_i" if i > 0 else ""
            fn = filepath / (fieldtype.structure_name() + suffix + ".json")
            with open(fn, "w") as io:
                io.write(data.json(indent=4))
