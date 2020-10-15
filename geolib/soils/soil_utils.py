from struct import pack, unpack_from

from pydantic.color import Color as PydanticColor


class Color(PydanticColor):
    """Color type from Pydantic

    see https://pydantic-docs.helpmanual.io/usage/types/#color-type

    Example:
        For construction::

            Color("ff00ff")  # hex value
            Color((255, 255, 255))  # rgb tuple
            Color("purple")  # named
    """

    def to_internal(self):
        r, g, b = self.as_rgb_tuple(alpha=False)
        return int.from_bytes(pack("BBBB", r, g, b, 0), "little")

    @classmethod
    def from_internal(cls, c: int):
        """Convert a D-Serie color integer into a Color."""
        r, g, b, _ = unpack_from("BBBB", c.to_bytes(4, "little"))
        return cls((r, g, b))
