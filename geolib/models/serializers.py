from typing import Any, Dict

from pydantic import FilePath

from geolib.models import BaseDataClass


class BaseSerializer(BaseDataClass):
    """Basic class for serializers."""

    ds: Dict[str, Any]

    def render(self):
        return str(self.ds)

    def write(self, filename: FilePath):
        """Test."""
        with open(filename, "w") as io:
            io.write(self.render())
