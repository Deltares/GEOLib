import csv
import re
from collections import namedtuple
from pathlib import Path

_CAMEL_TO_SNAKE_PATTERN = re.compile(r"(?<!^)(?=[A-Z])")


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
