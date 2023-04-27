"""
Common utility methods used within GEOLib.
"""

import csv
import logging
import re
from collections import namedtuple
from pathlib import Path
from typing import Any

from pydantic import validator

_CAMEL_TO_SNAKE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")

logger = logging.getLogger(__name__)


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return _CAMEL_TO_SNAKE_PATTERN.sub("_", name).lower()


def snake_to_camel(name: str) -> str:
    return "".join(word.title() for word in name.split("_"))


def csv_as_namedtuples(fn: Path, delimiter=";"):
    with open(fn, newline="") as f:
        reader = csv.reader(f, delimiter=delimiter)
        header = namedtuple("Header", next(reader))
        for data in map(header._make, reader):
            yield data


def make_newline_validator(*field_name: str, req_newlines: int = 2):
    """Get a dynamic validator for ensuring a set number of lines."""

    def field_must_contain_newlines(v: str):
        newlines = v.count("\n")
        if newlines < req_newlines:
            logger.warning(
                f"Added {req_newlines - newlines} lines to run_identification."
            )
            v += (req_newlines - newlines) * "\n"
        elif newlines > req_newlines:
            logger.warning(
                f"More than {req_newlines+1} lines in run_identification will be ignored in the GUI."
            )
        return v

    return validator(*field_name, allow_reuse=True)(field_must_contain_newlines)
