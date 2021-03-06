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
            TestUtils.get_local_test_data_dir("dstability/Tutorial_v20_2_1")
        )

        dm = DStabilityModel()
        dm.parse(test_input_filepath)

        bishop_analysis_method = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(center=Point(x=float("nan"), z=3), radius=15)
        )
        dm.set_model(bishop_analysis_method)

        data = dm.datastructure.json()
        # Using `in` was very slow, hence the find
        assert data.find('"NaN"') != -1  # Assert that quoted NaNs are found
        assert data.find(" NaN") == -1  # Assert that an unquoted NaN isn't found
