from os import scandir, path
from typing import List, _GenericAlias
from typing import get_type_hints, Type

from pydantic import DirectoryPath, FilePath

from geolib.models.parsers import BaseParser, BaseParserProvider

from .internal import BaseModelStructure, DStabilityStructure


class DStabilityParser(BaseParser):
    @property
    def suffix_list(self) -> List[str]:
        return [".json"]

    @property
    def structure(self) -> Type[DStabilityStructure]:
        return DStabilityStructure

    def can_parse(self, filename: FilePath) -> bool:
        return super().can_parse(filename) or path.isdir(filename)

    def parse(self, filepath: DirectoryPath) -> BaseModelStructure:
        ds = {}

        # Find required .json files via type hints
        for field, fieldtype in ((k, v) for k, v in get_type_hints(self.structure).items() if not k.startswith('__')):

            # On List types, parse a folder
            if type(fieldtype) == _GenericAlias:  # quite hacky
                element_type, *_ = fieldtype.__args__  # use getargs in 3.8
                ds[field] = self.__parse_folder(element_type, filepath)

            # Otherwise its a single .json in the root folder
            else:
                fn = filepath / (fieldtype.structure_name() + ".json")
                if not fn.exists():
                    raise Exception(f"Couldn't find required file at {fn}")
                ds[field] = fieldtype.parse_file(fn)

        return self.structure(**ds)

    def __parse_folder(self, fieldtype, filepath: DirectoryPath) -> List:
        out = []

        folder = filepath / fieldtype.structure_group()
        files = scandir(folder)
        # We need to sort to make sure that files such as x.json, x_1.json,
        # x_2.json etc. are stored sequentally, scandir produces arbitrary order.
        sorted_files = sorted(map(lambda x: x.path, files))

        for file in sorted_files:
            if fieldtype.structure_name() in str(file):
                out.append(fieldtype.parse_file(file))

        if len(out) == 0:
            raise Exception(f"Couldn't find required file(s) at {folder}")

        return out


class DStabilityParserProvider(BaseParserProvider):

    _input_parser = None
    _output_parser = None

    @property
    def input_parser(self) -> DStabilityParser:
        if not self._input_parser:
            self._input_parser = DStabilityParser()
        return self._input_parser

    @property
    def output_parser(self) -> DStabilityParser:
        if not self._output_parser:
            self._output_parser = DStabilityParser()
        return self._output_parser

    @property
    def parser_name(self) -> str:
        return "DStability"
