import os
from pathlib import Path

import pytest

from geolib.models import BaseModel
from geolib.models.dstability.dstability_parserprovider import (
    DStabilityParser,
    DStabilityParserProvider,
)
from tests.utils import TestUtils


class TestDStabilityInputParser:
    @pytest.mark.integrationtest
    def test_dstability_parse_directory(self):
        # 1. Set up test model
        input_parser = DStabilityParser()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dstability/example_1"))

        # 2. Verify initial expectations
        assert os.path.exists(test_filepath), "Testing directory not found."

        # 3. Run test.
        input_structure = input_parser.parse(test_filepath)
        assert input_structure.is_valid

        # 4. Verify final expectations.
        assert input_structure is not None
        data = input_structure.json(indent=4)
        with open("dstability_parsed_input.json", "w") as io:
            io.write(data)
