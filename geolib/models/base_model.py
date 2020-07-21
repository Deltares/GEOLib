# -*- coding: utf-8 -*-

"""
This module contains the primary objects that power GEOLib.
"""
import abc
import logging
import os
from abc import abstractmethod, abstractproperty
from pathlib import Path, PosixPath, WindowsPath
from subprocess import run, Popen
from types import CoroutineType
from typing import List, Optional, Type, Union
from requests.auth import HTTPBasicAuth

import requests
import pydantic.json
from pydantic import BaseModel as DataClass
from pydantic import DirectoryPath, FilePath, HttpUrl, conlist

from geolib.errors import CalculationError

from .base_model_structure import BaseModelStructure
from .meta import MetaData
from .parsers import BaseParserProvider


class BaseModel(DataClass, abc.ABC):
    filename: Optional[Path]
    datastructure: Optional[BaseModelStructure]
    meta: MetaData = MetaData()

    def execute(self, timeout_in_seconds: int = 5 * 60) -> "BaseModel":
        """Execute a Model and wait for `timeout` seconds.

        The model is modified in place if the calculation and parsing
        is successfull.
        """
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
            cwd=str(self.filename.parent),
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
        """Execute a Model on a remote endpoint.

        A new model instance is returned.
        """
        response = requests.post(
            endpoint + f"calculate/{self.__class__.__name__.lower()}",
            data=self.json(),
            auth=HTTPBasicAuth(self.meta.gl_username, self.meta.gl_password),
        )
        if response.status_code == 200:
            return self.__class__(**response.json())
        else:
            raise CalculationError(response.status_code, response.text)

    def get_error_context(self) -> str:
        err_fn = output_filename_from_input(self, extension=".err")
        batch_fn = self.filename.parent / "Batchlog.txt"
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
        # self.datastructure = None
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

        Requires a successfull execute.
        """
        return self.datastructure.results


class BaseModelList(DataClass):
    """Hold multiple models that can be executed in parallel.
    
    Note that all models need to have a unique filename
    otherwise they will overwrite eachother. This also helps with 
    identifying them later."""

    models: conlist(BaseModel, min_items=1)

    def execute(
        self,
        calculation_folder: DirectoryPath,
        timeout_in_seconds: int = 10 * 60,
        nprocesses: Optional[int] = os.cpu_count(),
    ) -> List[BaseModel]:
        """Execute all models in this class in parallel.

        We split the list to separate folders and call a batch processes on each folder.
        Note that the order of models will change.
        """
        lead_model = self.models[0]
        processes = []
        output_models = []

        split_models = [self.models[i::nprocesses] for i in range(nprocesses)]
        for i, models in enumerate(split_models):
            if len(models) == 0:
                continue
            unique_folder = calculation_folder / str(i)
            unique_folder.mkdir(parents=True, exist_ok=True)

            for model in models:
                fn = unique_folder / model.filename.name
                model.serialize(fn)

            process = Popen(
                [str(lead_model.meta.console_folder / lead_model.console_path)]
                + lead_model.console_flags
                + [str(unique_folder)],
                cwd=str(unique_folder),
            )
            processes.append(process)

        # Wait for all processes to be done
        for process in processes:
            process.wait(timeout=timeout_in_seconds)

        # Iterate over the models
        for i, models in enumerate(split_models):
            for model in models:
                output_filename = output_filename_from_input(model)
                if output_filename.exists():
                    model.parse(output_filename)
                    output_models.append(model)
                else:
                    logging.warning(
                        f"Model @ {model.filename} failed. Please check the .err file and batchlog.txt in its folder."
                    )

        return self.__class__(models=output_models)

    def execute_remote(self, endpoint: HttpUrl) -> "BaseModelList":
        """Execute all models in this class in parallel on a remote endpoint.

        Note that the order of models will change.
        """
        lead_model = self.models[0]

        response = requests.post(
            endpoint + f"calculate/{lead_model.__class__.__name__.lower()}s",
            data="[" + ",".join((model.json() for model in self.models)) + "]",
            auth=HTTPBasicAuth(lead_model.meta.gl_username, lead_model.meta.gl_password),
        )
        if response.status_code == 200:
            models = response.json()["models"]
            return self.__class__(
                models=[lead_model.__class__(**model) for model in models]
            )
        else:
            raise CalculationError(response.status_code, response.text)


def output_filename_from_input(model: BaseModel, extension: str = None) -> Path:
    if not extension:
        extension = model.parser_provider_type().output_parsers[-1].suffix_list[0]
    return model.filename.with_suffix(extension)
