class GEOLibError(Exception):
    """Base GEOLib Exception class."""


class ParserError(GEOLibError):
    """Base class for Parser errors."""


class GEOLibNotImplementedError(GEOLibError, NotImplementedError):
    """Base class for not implemented abstract classes."""


NotConcreteError = GEOLibNotImplementedError("Should be implemented in concrete class.")
