# -*- coding: utf-8 -*-

"""
This module contains the primary objects that power GEOLib.
"""
import abc
import logging
import os
from abc import abstractmethod, abstractproperty
from pathlib import Path
from subprocess import run
from types import CoroutineType
from typing import List, Optional, Type, Union

import requests
from pydantic import BaseModel as DataClass
from pydantic import DirectoryPath, FilePath, HttpUrl

from geolib.errors import CalculationError

from .base_model_structure import BaseModelStructure
from .meta import MetaData
from .parsers import BaseParserProvider


class BaseModel(DataClass, abc.ABC):
    filename: Union[FilePath, DirectoryPath, None]
    datastructure: Optional[Type[BaseModelStructure]]
    meta: MetaData = MetaData()

    def execute(self, timeout_in_seconds: int = 2 * 60) -> "BaseModel":
        """Execute a Model and wait for `timeout` seconds."""
        if self.filename is None:
            raise ValueError("Set filename or serialize first!")
        if not self.filename.exists():
            logging.warning("Serializing before executing.")
            self.serialize(self.filename)
        process = run(
            [str(self.meta.console_folder / self.console_path)]
            + self.console_flags
            + [str(self.filename)],
            timeout=timeout_in_seconds,
            cwd=str(self.meta.console_folder),
        )

        # Successfull run
        output_filename = output_filename_from_input(self)
        logging.info(
            f"Checking for {output_filename}, while process exited with {process.returncode}"
        )
        if process.returncode == 0 and output_filename.exists():
            self.parse(output_filename)
            return self  # TODO Figure out whether we should instantiate a new model (parse is a classmethod)

        # Unsuccessfull run
        else:
            error = self.get_error_context()
            raise CalculationError(process.returncode, error)

    def execute_remote(self, endpoint: HttpUrl) -> "BaseModel":
        """Execute a Model on a remote endpoint."""
        r = requests.post(endpoint + "calculate", json={"model": self.json()})
        if r.status_code == 200:
            return self.__class__(**r.json())
        else:
            raise CalculationError(r.status_code, r.text)

    def get_error_context(self) -> str:
        err_fn = output_filename_from_input(self, extension=".err")
        batch_fn = self.meta.console_folder / "Batchlog.txt"
        error = ""
        if err_fn.exists():
            with open(err_fn) as f:
                error += f"### {err_fn} ###\n"
                error += f.read()
        elif batch_fn.exists():
            with open(batch_fn) as f:
                error += f"### {batch_fn} ###\n"
                error += f.read()
        else:
            error = "Couldn't determine source of error."
        return error

    @abstractmethod
    def serialize(
        self, filename: Union[FilePath, DirectoryPath, None]
    ) -> Union[FilePath, DirectoryPath, None]:
        """Serialize model to input file."""

    @property
    def console_path(self) -> Path:
        raise NotImplementedError("Implement in concrete classes.")

    @property
    def console_flags(self) -> List[str]:
        return []

    @abstractproperty
    def parser_provider_type(self) -> Type[BaseParserProvider]:
        """Returns the parser provider type of the current concrete class.

        Raises:
            NotImplementedError: If not implemented in the concrete class.

        Returns:
            Type[BaseParserProvider] -- Concrete parser provider.
        """
        raise NotImplementedError("Implement in concrete classes.")

    def parse(self, filename: FilePath) -> BaseModelStructure:
        """Parse input or outputfile to Model, depending on extension."""
        self.filename = filename
        self.datastructure = self.parser_provider_type().parse(filename)
        return self.datastructure

    @property
    def is_valid(self) -> bool:
        """Checks validity and integrity of structure."""
        if self.datastructure is not None:
            return self.datastructure.is_valid
        else:
            logging.warning("No datastructured parsed yet!")
            return False

    def set_metadata(self, meta: MetaData):
        """Set custom metadata for input file."""
        self.metadata = meta

    @property
    def input(self):
        """Access internal dict-like datastructure of the input."""
        return self.datastructure

    @property
    def output(self):
        """Access internal dict-like datastructure of the output.

        Requires a succesful execute. Throws an error with error codes
        and explanation from the error file if not.
        """
        return self.datastructure.results


class BaseModelList(DataClass):
    """Hold multiple models that can be executed in parallel."""

    models: List[BaseModel]

    async def execute(
        self, timeout: int = 10, nprocesses: Optional[int] = os.cpu_count()
    ) -> CoroutineType:
        """Execute all models in this class in parallel.

        We split the list to separate folders and call a batch processes on each folder.
        """

    async def execute_remote(self, endpoint: HttpUrl) -> CoroutineType:
        """Execute all models in this class in parallel on a remote endpoint.
        """


def output_filename_from_input(model: BaseModel, extension: str = None) -> Path:
    if not extension:
        extension = model.parser_provider_type().output_parsers[-1].suffix_list[0]
    return model.filename.with_suffix(extension)
