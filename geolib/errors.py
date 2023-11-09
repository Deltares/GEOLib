"""
Error definitions for GEOLib.
"""


class GEOLibError(Exception):
    """Base GEOLib Exception class."""


class CalculationError(GEOLibError):
    """CalculationError with a status_code."""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class ParserError(GEOLibError):
    """Base class for Parser errors."""


class GEOLibNotImplementedError(GEOLibError, NotImplementedError):
    """Base class for not implemented abstract classes."""


NotConcreteError = GEOLibNotImplementedError("Should be implemented in concrete class.")
