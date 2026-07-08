from datetime import datetime
from pathlib import Path

import pytest
from pydantic_core._pydantic_core import ValidationError

from geolib.models.dgeoflow import DGeoFlowModel
from geolib.models.dgeoflow.internal import (
    BoundaryConditionCollection,
    DGeoFlowStructure,
    ForeignKeys,
    ProjectInfo,
)
from geolib.models.dstability.utils import children
from tests.utils import TestUtils


class TestDGeoFlowInternal:
    @pytest.mark.integrationtest
    def test_dstability_fk_validation(self):
        # 1. Set up test model
        test_input_filepath = Path(
            TestUtils.get_local_test_data_dir("dgeoflow/Berekening3.flox")
        )
        dm = DGeoFlowModel(filename=None)
        dm.parse(test_input_filepath)

        # 2. Verify initial expectations.
        assert test_input_filepath.exists()
        assert dm is not None

        # 3. Unlink a foreign key
        scenario = dm.datastructure.scenarios[0]
        scenario.GeometryId = -1
        dm.datastructure.scenarios[0] = scenario

        # 4. Verify structure is invalid, recreating triggers validation
        with pytest.raises(ValidationError):
            DGeoFlowStructure(**dict(dm.datastructure))

    @pytest.mark.unittest
    def test_foreign_keys(self):
        fk = ForeignKeys()
        mapping = fk.class_fields

        # Validate "Scenario" has 2 Id like fields defined
        assert "Scenario" in mapping
        assert len(mapping["Scenario"]) == 2

    @pytest.mark.unittest
    def test_find_subclass_from_children(self):
        # Setup
        dm = DGeoFlowModel()
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dgeoflow/Berekening3.flox")
        )
        dm.parse(test_filepath)

        # Verify expecations
        assert isinstance(
            dm.datastructure.boundary_conditions[0], BoundaryConditionCollection
        )

        # Test
        child_classes = [type(x).__name__ for x in children(dm.datastructure)]

        # Verify result
        assert "PersistableBoundaryCondition" in child_classes

    @pytest.mark.unittest
    def test_projectinfo_validation(self):
        projectinfo = ProjectInfo()

        assert projectinfo.Created == datetime.now().date()

        projectinfo = ProjectInfo(Created=datetime(2022, 11, 23))
        assert projectinfo.Created == datetime(2022, 11, 23).date()

        projectinfo = ProjectInfo(Created="23-11-2022")
        assert projectinfo.Created == datetime(2022, 11, 23).date()

        projectinfo = ProjectInfo(Created="2022-11-23")
        assert projectinfo.Created == datetime(2022, 11, 23).date()

    @pytest.mark.unittest
    def test_projectinfo_iso_datetime_format(self):
        """Test that ProjectInfo can parse ISO format dates with time (YYYY-MM-DDTHH:MM:SS).
        
        This test covers the fix for parsing dates from D-Stability Console output,
        which serializes dates with time component in ISO format.
        """
        # Parse ISO format with time (from console output)
        projectinfo = ProjectInfo(Created="2019-10-17T00:00:00")
        assert projectinfo.Created == datetime(2019, 10, 17).date()

        projectinfo = ProjectInfo(Date="2019-11-28T12:30:45")
        assert projectinfo.Date == datetime(2019, 11, 28).date()

        projectinfo = ProjectInfo(LastModified="2026-03-16T00:00:00")
        assert projectinfo.LastModified == datetime(2026, 3, 16).date()

    @pytest.mark.unittest
    def test_projectinfo_date_serialization_format(self):
        """Test that ProjectInfo serializes dates to DD-MM-YYYY format.
        
        This test ensures dates are serialized in the format expected by D-Stability Console.
        """
        projectinfo = ProjectInfo(
            Created="2019-10-17T00:00:00",
            Date="2019-11-28T00:00:00",
            LastModified="2026-03-16T00:00:00"
        )

        # Serialize to JSON
        json_str = projectinfo.model_dump_json()

        # Verify DD-MM-YYYY format in JSON output
        assert '"Created":"17-10-2019"' in json_str
        assert '"Date":"28-11-2019"' in json_str
        assert '"LastModified":"16-03-2026"' in json_str
