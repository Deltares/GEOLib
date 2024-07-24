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
        test_filepath = Path(TestUtils.get_local_test_data_dir("dgeoflow/Berekening3"))
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
