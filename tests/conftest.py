import pytest
import shutil
from pathlib import Path
from tests.utils import TestUtils


@pytest.fixture(scope="session")
def cleandir_dsh():
    test_output_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
    #
    shutil.rmtree(test_output_folder)


@pytest.fixture(scope="session")
def cleandir_dfo():
    test_output_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
    #
    shutil.rmtree(test_output_folder)


@pytest.fixture(scope="session")
def cleandir_dse():
    test_output_folder = Path(TestUtils.get_output_test_data_dir("dsettlement"))
    #
    shutil.rmtree(test_output_folder)

