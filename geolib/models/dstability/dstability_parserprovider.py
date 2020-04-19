import inspect
import json
import logging
import os
import sys
from enum import Enum
from typing import List, Type, _GenericAlias
from typing import get_type_hints

from pydantic import FilePath, DirectoryPath, BaseModel

from geolib.models.dseries_parser import DSerieParser
from geolib.models.parsers import BaseParser, BaseParserProvider

from .internal import *


class DStabilityInputParser(BaseParser):
    """DStability parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return ["", ".json"]

    def parse(self, filepath: DirectoryPath) -> DStabilityInputStructure:
        ds = {}

        # Find required .json files via type hints
        for field, fieldtype in get_type_hints(DStabilityInputStructure).items():
            # On List types, parse a folder
            if type(fieldtype) == _GenericAlias:  # quite hacky
                element_type, *_ = fieldtype.__args__  # use getargs in 3.8
                ds[field] = self.parse_folder(element_type, filepath)
            # Otherwise its a single .json in the root folder
            else:
                fn = filepath / (fieldtype.structure_name() + ".json")
                if not fn.exists():
                    raise Exception(f"Couldn't find required file at {fn}")
                ds[field] = fieldtype.parse_file(fn)

        return DStabilityInputStructure(**ds)

    def parse_folder(self, fieldtype, filepath):
        out = []

        folder = filepath / fieldtype.structure_group()
        files = os.scandir(folder)
        sorted_files = sorted(map(lambda x: x.path, files))

        for file in sorted_files:
            if fieldtype.structure_name() in str(file):
                out.append(fieldtype.parse_file(file))

        if len(out) == 0:
            raise Exception(f"Couldn't find required file(s) at {folder}")

        return out


class DStabilityOutputParser(BaseParser):
    """DStability parser of input files."""

    @property
    def suffix_list(self) -> List[str]:
        return ["", ".json"]


class DStabilityParserProvider(BaseParserProvider):

    __input_parser = None
    __output_parser = None

    @property
    def input_parser(self) -> DStabilityInputParser:
        if not self.__input_parser:
            self.__input_parser = DStabilityInputParser()
        return self.__input_parser

    @property
    def output_parser(self):
        raise NotImplementedError()

    @property
    def parser_name(self) -> str:
        return "DStability"
