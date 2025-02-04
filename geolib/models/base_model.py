# -*- coding: utf-8 -*-

"""
This module contains the primary objects that power GEOLib.
"""
import abc
import logging
from abc import abstractmethod
from pathlib import Path
from subprocess import run

import requests
from pydantic import DirectoryPath, FilePath, HttpUrl, SerializeAsAny, ValidationError
from requests.auth import HTTPBasicAuth

from geolib.errors import CalculationError
from geolib.models import BaseDataClass
from geolib.models.base_model_structure import BaseModelStructure
from geolib.models.meta import MetaData
from geolib.models.parsers import BaseParserProvider

logger = logging.getLogger(__name__)
meta = MetaData()


class BaseModel(BaseDataClass, abc.ABC):
    filename: Path | None = None
    datastructure: SerializeAsAny[BaseModelStructure] | None = None
    """
    This is the base class for all models in GEOLib.
    
    Note that `datastructure` is a `SerializeAsAny` type, which means that
    the inheriting class is serialized according to its own definition (duck-typing).
    This is needed since Pydantic v2 as the default behavior has changed:
    https://docs.pydantic.dev/latest/concepts/serialization/#subclass-instances-for-fields-of-basemodel-dataclasses-typeddict
    """

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

        if self.custom_console_path is not None:
            executable = self.custom_console_path
        else:
            executable = meta.console_folder / self.default_console_path

        if not executable.exists():
            logger.error(
                f"Please make sure the `geolib.env` file points to the console folder. GEOLib now can't find it at `{executable}`"
            )
            raise CalculationError(-1, f"Console executable not found at {executable}.")

        process = run(
            [str(executable)]
            + self.console_flags
            + [str(self.filename.resolve())]
            + self.console_flags_post,
            timeout=timeout_in_seconds,
            cwd=str(self.filename.resolve().parent),
        )
        logger.debug(f"Executed with {process.args}")

        # Successful run
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
                    f"Output file generated but parsing of {output_filename} failed."
                )
                error = self.get_error_context()
                raise CalculationError(process.returncode, error)

        # Unsuccessful run
        else:
            error = self.get_error_context()
            raise CalculationError(
                process.returncode, error + " Path: " + str(output_filename.absolute())
            )

    def execute_remote(self, endpoint: HttpUrl) -> "BaseModel":
        """Execute a Model on a remote endpoint.

        A new model instance is returned.
        """
        response = requests.post(
            requests.compat.urljoin(
                endpoint, f"calculate/{self.__class__.__name__.lower()}"
            ),
            data=self.json(),
            auth=HTTPBasicAuth(meta.gl_username, meta.gl_password),
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
        self, filename: FilePath | DirectoryPath | None
    ) -> FilePath | DirectoryPath | None:
        """Serialize model to input file."""

    @property
    def default_console_path(self) -> Path:
        raise NotImplementedError("Implement in concrete classes.")

    @property
    def custom_console_path(self) -> Path | None:
        return None

    @property
    def console_flags(self) -> list[str]:
        return []

    @property
    def console_flags_post(self) -> list[str]:
        return []

    @property
    @abstractmethod
    def parser_provider_type(self) -> type[BaseParserProvider]:
        """Returns the parser provider type of the current concrete class.

        Raises:
            NotImplementedError: If not implemented in the concrete class.

        Returns:
            type[BaseParserProvider] -- Concrete parser provider.
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

    def get_meta_property(self, key: str) -> str | None:
        """Get a metadata property from the input file."""
        if hasattr(meta, key):
            return meta.__getattribute__(key)
        else:
            return None

    def set_meta_property(self, key: str, value: str) -> None:
        """Set a metadata property from the input file."""
        if hasattr(meta, key):
            meta.__setattr__(key, value)
        else:
            raise ValueError(f"Metadata property {key} does not exist.")


def output_filename_from_input(model: BaseModel, extension: str = None) -> Path:
    if not extension:
        extension = model.parser_provider_type().output_parsers[-1].suffix_list[0]
    return model.filename.with_suffix(extension)
