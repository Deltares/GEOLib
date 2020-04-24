# -*- coding: utf-8 -*-

"""
This module contains the primary objects that power GEOLib.
"""
import abc
import os
import logging
from types import CoroutineType
from typing import List, Optional, Type

from pydantic import BaseModel as DataClass
from pydantic import FilePath, HttpUrl

from .meta import MetaData
from .parsers import BaseParserProvider
from .base_model_structure import BaseModelStructure


class BaseModel(DataClass, abc.ABC):
    input_fn: Optional[FilePath]
    output_fn: Optional[FilePath]
    datastructure: Optional[BaseModelStructure]

    async def execute(self, timeout: int = 10) -> CoroutineType:
        """Execute a Model and wait for `timeout` seconds."""

    async def execute_remote(self, endpoint: HttpUrl) -> CoroutineType:
        """Execute a Model on a remote endpoint."""

    def serialize(self, filename: Optional[FilePath]) -> str:
        """Serialize model to input file."""

    @property
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
        pass

    @property
    def input(self):
        """Access internal dict-like datastructure of the input."""
        pass

    @property
    def output(self):
        """Access internal dict-like datastructure of the output.

        Requires a succesful execute. Throws an error with error codes
        and explanation from the error file if not.
        """


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
