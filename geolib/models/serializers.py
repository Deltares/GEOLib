from pydantic import BaseModel as DataClass


class BaseSerializer(DataClass):
    """Basic class for serializers."""

    ds: dict

    def render(self):
        return str(self.ds)

    def write(self, filename: str):
        """Test."""
        with open(filename, "w") as io:
            io.write(self.render())
