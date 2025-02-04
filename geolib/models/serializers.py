from pathlib import Path
from typing import Any, BinaryIO

from pydantic import FilePath

from geolib.models import BaseDataClass


class BaseSerializer(BaseDataClass):
    """Basic class for serializers."""

    ds: dict[str, Any]

    def render(self) -> str:
        return str(self.ds)

    def write(self, filename: FilePath | BinaryIO):
        """Write serialized model to Filepath or BytesIO buffer"""
        # if filename is pathlike, open file (in text mode) and write str
        if isinstance(filename, Path):
            with open(filename, "w", encoding="cp1252") as io:
                io.write(self.render())

        # if filename is opened file (in binary mode) or BytesIO object, write render as bytes
        else:
            filename.write(self.render().encode("cp1252"))
