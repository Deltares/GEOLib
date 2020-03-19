# -*- coding: utf-8 -*-

"""
geolib.models
~~~~~~~~~~~~~~~
This module contains the primary objects that power GEOLIB.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0


class Model(object):
    def __init__(self, inputfn):
        self.inputfn = inputfn
        pass


    def initialize(self, config_file: str = None) -> str:
        """BMI. Create input file for model and return filename."""
        pass

    async def execute(self, timeout=10) -> bool:
        """Execute a Model and wait for `timeout` seconds."""
        pass

    def serialize(self) -> str:
        """Serialize input to file."""
        pass

    @classmethod
    def parse(cls, inputfilename: str):
        """Parse inputfile to Model."""
        return cls(inputfilename)

    def finalize(self) -> bool:
        """BMI. Read model dump."""
        pass

    def get_value(self, path: str):
        """BMI. Get value."""
        pass

    def set_value(self, path: str, value: any):
        """BMI. Set value of path."""
        pass

    def set_metadata(self, stuff: dict):
        """Set custom metadata for header."""
        pass
