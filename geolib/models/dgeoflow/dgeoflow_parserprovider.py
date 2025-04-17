import logging
from zipfile import ZipFile

from pydantic import DirectoryPath, FilePath
from zipp import Path

from geolib.models.parsers import BaseParser, BaseParserProvider
from geolib.models.utils import get_filtered_type_hints, is_list

from .internal import BaseModelStructure, DGeoFlowStructure

logger = logging.getLogger(__name__)


class DGeoFlowParser(BaseParser):
    @property
    def suffix_list(self) -> list[str]:
        return [".json", ""]

    @property
    def structure(self) -> type[DGeoFlowStructure]:
        return DGeoFlowStructure

    def can_parse(self, filename: FilePath) -> bool:
        return super().can_parse(filename) or filename.is_dir()

    def parse(self, filepath: DirectoryPath) -> BaseModelStructure:
        data_structure = {}

        # Find required .json files via type hints
        for field, fieldtype in get_filtered_type_hints(self.structure):
            # On list types, parse a folder
            if is_list(fieldtype):
                element_type = fieldtype.__args__[0]
                data_structure[field] = self.__parse_folder(element_type, filepath / "")

            # Otherwise it is a single .json in the root folder
            else:
                fn = filepath / (fieldtype.structure_name() + ".json")
                if not fn.exists():
                    raise FileNotFoundError(f"Couldn't find required file at {fn}")
                data_structure[field] = fieldtype.model_validate_json(fn.open().read())

        return self.structure(**data_structure)

    def __parse_folder(self, fieldtype, filepath: DirectoryPath) -> list:
        out = []
        folder = filepath / fieldtype.structure_group()

        try:
            files = list(folder.iterdir())
        except FileNotFoundError:  # Not all result folders are required.
            return out
        # We need to sort to make sure that files such as x.json, x_1.json,
        # x_2.json etc. are stored sequentally, scandir produces arbitrary order.
        sorted_files = sorted(files, key=lambda x: x.name)
        for file in sorted_files:
            if fieldtype.structure_name() in file.name:
                out.append(fieldtype.model_validate_json(file.open().read()))
            else:
                logger.debug(f"Didn't match {fieldtype} for {file}")
        if len(out) == 0:
            logger.debug(f"Couldn't find {fieldtype} file(s) at {folder}")
        return out


class DGeoFlowZipParser(DGeoFlowParser):
    @property
    def suffix_list(self) -> list[str]:
        return [".flox"]

    def can_parse(self, filename: FilePath) -> bool:
        return filename.suffix in self.suffix_list

    def parse(self, filepath: FilePath) -> BaseModelStructure:
        with ZipFile(filepath) as zip:
            # Fix backslashes in zipfile (until fixed in DGeoFlow)
            for file in zip.filelist:
                new_filename = file.filename.replace("\\", "/")
                if new_filename != file.filename:
                    file.filename = new_filename
            for key in list(zip.NameToInfo.keys()):
                new_key = key.replace("\\", "/")
                if new_key != key:
                    zip.NameToInfo[new_key] = zip.NameToInfo.pop(key)

            path = Path(zip)
            data_structure = super().parse(path)
        return data_structure


class DGeoFlowParserProvider(BaseParserProvider):
    _input_parsers = None
    _output_parsers = None

    @property
    def input_parsers(self) -> tuple[DGeoFlowParser, DGeoFlowZipParser]:
        if not self._input_parsers:
            self._input_parsers = (DGeoFlowZipParser(), DGeoFlowParser())
        return self._input_parsers

    @property
    def output_parsers(self) -> tuple[DGeoFlowParser, DGeoFlowZipParser]:
        if not self._output_parsers:
            self._output_parsers = (DGeoFlowParser(), DGeoFlowZipParser())
        return self._output_parsers

    @property
    def parser_name(self) -> str:
        return "DGeoFlow"
