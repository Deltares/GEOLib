# -*- coding: utf-8 -*-

"""
This module contains the primary objects that power GEOLib.
"""
import abc
import logging
import os
from abc import abstractmethod, abstractproperty
from pathlib import Path, PosixPath, WindowsPath
from subprocess import Popen, run
from types import CoroutineType
from typing import List, Optional, Type, Union

import requests
from pydantic import DirectoryPath, FilePath, HttpUrl, conlist
from pydantic.error_wrappers import ValidationError
from requests.auth import HTTPBasicAuth

from geolib.errors import CalculationError
from geolib.models import BaseDataClass

from .base_model_structure import BaseModelStructure
from .meta import MetaData
from .parsers import BaseParserProvider

logger = logging.getLogger(__name__)
meta = MetaData()


class BaseModel(BaseDataClass, abc.ABC):
    filename: Optional[Path]
    datastructure: Optional[BaseModelStructure]
    meta: MetaData = MetaData()

    def execute(self, timeout_in_seconds: int = meta.timeout) -> "BaseModel":
        """Execute a Model and wait for `timeout` seconds.

        The model is modified in place if the calculation and parsing
        is successful.
        """
        if self.filename is None:
            raise ValueError("Set filename or serialize first!")
        if not self.filename.exists():
            logger.warning("Serializing before executing.")
            self.serialize(self.filename)

        executable = self.meta.console_folder / self.console_path
        if not executable.exists():
            logger.error(
                f"Please make sure the `geolib.env` file points to the console folder. GEOLib now can't find it at `{executable}`"
            )
            raise CalculationError(-1, f"Console executable not found at {executable}.")

        process = run(
            [str(executable)] + self.console_flags + [str(self.filename.resolve())],
            timeout=timeout_in_seconds,
            cwd=str(self.filename.resolve().parent),
        )
        logger.debug(f"Executed with {process.args}")

        # Successfull run
        output_filename = output_filename_from_input(self)
        logger.info(
            f"Checking for {output_filename}, while process exited with {process.returncode}"
        )
        if output_filename.exists():
            try:
                self.parse(output_filename)
                return self  # TODO Figure out whether we should instantiate a new model (parse is a classmethod)
            except ValidationError:
                logger.warning(
                    f"Ouput file generated but parsing of {output_filename} failed."
                )
                error = self.get_error_context()
                raise CalculationError(process.returncode, error)

        # Unsuccessful run
        else:
            error = self.get_error_context()
            raise CalculationError(process.returncode, error)

    def execute_remote(self, endpoint: HttpUrl) -> "BaseModel":
        """Execute a Model on a remote endpoint.

        A new model instance is returned.
        """
        response = requests.post(
            requests.compat.urljoin(
                endpoint, f"calculate/{self.__class__.__name__.lower()}"
            ),
            data=self.json(),
            auth=HTTPBasicAuth(self.meta.gl_username, self.meta.gl_password),
        )
        if response.status_code == 200:
            data = response.json()
            # remove possibly invalid external metadata
            data.get("meta", {}).pop("console_folder", None)
            return self.__class__(**data)
        else:
            raise CalculationError(response.status_code, response.text)

    def get_error_context(self) -> str:
        err_fn = output_filename_from_input(self, extension=".err")
        batch_fn = self.filename.parent / "Batchlog.txt"
        error = f"{self.filename.name}\n"
        if err_fn.exists():
            with open(err_fn) as f:
                error += f"### {err_fn} ###\n"
                error += f.read()
        elif batch_fn.exists():
            with open(batch_fn) as f:
                error += f"### {batch_fn} ###\n"
                error += f.read()
        else:
            error = f"Couldn't determine source of error for {self.filename.name}."
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
            logger.warning("No datastructured parsed yet!")
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

        Requires a successful execute.
        """
        return self.datastructure.results


class BaseModelList(BaseDataClass):
    """Hold multiple models that can be executed in parallel.

    Note that all models need to have a unique filename
    otherwise they will overwrite eachother. This also helps with
    identifying them later."""

    models: List[BaseModel]
    meta: MetaData = MetaData()
    errors: List[str] = []

    def execute(
        self,
        calculation_folder: DirectoryPath,
        timeout_in_seconds: int = meta.timeout,
        nprocesses: Optional[int] = os.cpu_count(),
    ) -> "BaseModelList":
        """Execute all models in this class in parallel.

        We split the list to separate folders and call a batch processes on each folder.
        Note that the order of models will change.
        """

        # manual check as remote execution could result in zero models
        if len(self.models) == 0:
            raise ValueError("Can't execute with zero models.")

        lead_model = self.models[0]
        processes = []
        output_models = []
        errors = []

        # Divide the models over n processes and make sure to copy them to prevent aliasing
        split_models = [self.models[i::nprocesses] for i in range(nprocesses)]
        for i, models in enumerate(split_models):
            if len(models) == 0:
                continue
            unique_folder = calculation_folder / str(i)
            unique_folder.mkdir(parents=True, exist_ok=True)

            for model in models:
                fn = unique_folder / model.filename.name
                model.serialize(fn.resolve())

            executable = self.meta.console_folder / lead_model.console_path
            if not executable.exists():
                logger.error(
                    f"Please make sure the `geolib.env` file points to the console folder. GEOLib now can't find it at `{executable}`"
                )
                raise CalculationError(-1, f"Console executable not found at {executable}.")

            process = Popen(
                [str(executable)] + lead_model.console_flags + [str(i)],
                cwd=str(calculation_folder.resolve()),
            )
            processes.append(process)

        # Wait for all processes to be done
        for process in processes:
            logger.debug(f"Executed with {process.args}")
            process.wait(timeout=timeout_in_seconds)

        # Iterate over the models
        for i, models in enumerate(split_models):
            for model in models:
                model = model.copy(deep=True)  # prevent aliasing
                output_filename = output_filename_from_input(model)
                if output_filename.exists():
                    try:
                        model.parse(output_filename)
                        output_models.append(model)

                    except ValidationError:
                        logger.warning(
                            f"Ouput file generated but parsing of {output_filename.name} failed."
                        )
                        error = model.get_error_context()
                        errors.append(error)
                else:
                    logger.warning(
                        f"Model @ {output_filename.name} failed. Please check the .err file and batchlog.txt in its folder."
                    )
                    error = model.get_error_context()
                    errors.append(error)

        return self.__class__(models=output_models, errors=errors)

    def execute_remote(self, endpoint: HttpUrl) -> "BaseModelList":
        """Execute all models in this class in parallel on a remote endpoint.

        Note that the order of models will change.
        """
        lead_model = self.models[0]

        response = requests.post(
            requests.compat.urljoin(
                endpoint, f"calculate/{lead_model.__class__.__name__.lower()}s"
            ),
            data="[" + ",".join((model.json() for model in self.models)) + "]",
            auth=HTTPBasicAuth(lead_model.meta.gl_username, lead_model.meta.gl_password),
        )
        if response.status_code == 200:
            models = response.json()["models"]
            errors = response.json()["errors"]
            stripped_models = []
            for model in models:
                # remove possibly invalid external metadata
                model.get("meta", {}).pop("console_folder", None)
                stripped_models.append(lead_model.__class__(**model))
            return self.__class__(models=stripped_models, errors=errors)
        else:
            raise CalculationError(response.status_code, response.text)


def output_filename_from_input(model: BaseModel, extension: str = None) -> Path:
    if not extension:
        extension = model.parser_provider_type().output_parsers[-1].suffix_list[0]
    return model.filename.with_suffix(extension)
