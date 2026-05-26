from datetime import date
from pathlib import Path
from typing import Annotated, Any, BinaryIO

from pydantic import FilePath, PlainSerializer

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

FormattedDate = Annotated[
    date | None,
    PlainSerializer(
        lambda v: v.strftime("%d-%m-%Y") if v is not None else None,
        return_type=str | None
    )
]
