from pathlib import Path

import pytest
from geolib.geometry import Point
from geolib.models import DStabilityModel
from geolib.models.dstability.analysis import (
    DStabilityBishopAnalysisMethod,
    DStabilityCircle,
)

from tests.utils import TestUtils


class TestDStabilityNaNFields:
    @pytest.mark.systemtest
    def test_nan_fields_become_string_in_json(self):
        test_input_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/EmptyFile.stix")
        )

        dm = DStabilityModel()
        dm.parse(test_input_filepath)

        bishop_analysis_method = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=float("nan"), z=3), radius=15)
        )
        dm.set_model(bishop_analysis_method, 0, 0)

        data = dm.datastructure.model_dump_json()
        # Using `in` was very slow, hence the find
        assert data.find('"NaN"') != -1  # Assert that quoted NaNs are found
        assert data.find(" NaN") == -1  # Assert that an unquoted NaN isn't found
