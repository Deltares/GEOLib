import pytest
import shutil
from pathlib import Path
from tests.utils import TestUtils


@pytest.fixture(scope="session")
def cleandir():
    test_output_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
    shutil.rmtree(test_output_folder)

