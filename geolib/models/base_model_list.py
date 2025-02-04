import logging
import os
from subprocess import Popen

import requests
from pydantic import DirectoryPath, HttpUrl
from requests.auth import HTTPBasicAuth

from geolib.errors import CalculationError
from geolib.models import meta
from geolib.models.base_data_class import BaseDataClass
from geolib.models.base_model import BaseModel, output_filename_from_input

logger = logging.getLogger(__name__)
meta = meta.MetaData()


class BaseModelList(BaseDataClass):
    """Hold multiple models that can be executed in parallel.

    Note that all models need to have a unique filename
    otherwise they will overwrite eachother. This also helps with
    identifying them later."""

    models: list[BaseModel]
    errors: list[str] = []

    def execute(
        self,
        calculation_folder: DirectoryPath,
        timeout_in_seconds: int = meta.timeout,
        nprocesses: int | None = os.cpu_count(),
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

            executable = meta.console_folder / lead_model.default_console_path
            if not executable.exists():
                logger.error(
                    f"Please make sure the `geolib.env` file points to the console folder. GEOLib now can't find it at `{executable}`"
                )
                raise CalculationError(
                    -1, f"Console executable not found at {executable}."
                )

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
        for models in split_models:
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
            auth=HTTPBasicAuth(meta.gl_username, meta.gl_password),
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
