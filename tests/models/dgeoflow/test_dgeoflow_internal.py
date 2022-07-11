from pathlib import Path

import pytest
from pydantic import ValidationError

from geolib.models.dgeoflow import DGeoflowModel
from geolib.models.dgeoflow.internal import ForeignKeys, BoundaryCondition, DGeoflowStructure

from geolib.models.dstability.utils import children
from tests.utils import TestUtils


class TestDGeoflowInternal:
    @pytest.mark.integrationtest
    def test_dstability_fk_validation(self):
        # 1. Set up test model
        test_input_filepath = Path(
            TestUtils.get_local_test_data_dir("dgeoflow/Berekening3.flox")
        )
        dm = DGeoflowModel(filename=None)
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
            DGeoflowStructure(**dict(dm.datastructure))


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
        dm = DGeoflowModel()
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dgeoflow/Berekening3")
        )
        dm.parse(test_filepath)

        # Verify expecations
        assert isinstance(dm.datastructure.boundary_conditions[0], BoundaryCondition)

        # Test
        child_classes = [type(x).__name__ for x in children(dm.datastructure)]

        # Verify result
        assert "PersistableBoundaryCondition" in child_classes
