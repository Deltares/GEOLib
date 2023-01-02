from io import BytesIO
from typing import Any
from typing import Dict
from typing import Union

from pydantic import FilePath

from geolib.models import BaseDataClass


class BaseSerializer(BaseDataClass):
    """Basic class for serializers."""

    ds: Dict[str, Any]

    def render(self) -> str:
        return str(self.ds)

    def write(self, filename: Union[FilePath, BytesIO]):
        """Write serialized model to Filepath or BytesIO buffer"""
        if isinstance(filename, BytesIO):
            filename.write(self.render().encode('utf-8'))
        with open(filename, "w") as io:
            io.write(self.render())
