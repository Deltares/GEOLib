from pathlib import Path
import pytest
from tests.utils import TestUtils, only_teamcity
from pydantic import ValidationError
from geolib.models.dstability import DStabilityModel
from geolib.models.dstability.internal import (
    DStabilityStructure,
    ForeignKeys,
    PersistableHeadLine,
    Waternet,
)
from geolib.models.dstability.utils import children


class TestDStabilityInternal:
    @pytest.mark.integrationtest
    def test_dstability_fk_validation(self):
        # 1. Set up test model
        test_input_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/example_1/Tutorial.stix")
        )
        dm = DStabilityModel(filename=None)
        dm.parse(test_input_filepath)

        # 2. Verify initial expectations.
        assert test_input_filepath.exists()
        assert dm is not None

        # 3. Unlink a foreign key
        stage = dm.datastructure.stages[0]
        stage.GeometryId = -1
        dm.datastructure.stages[0] = stage

        # 4. Verify structure is invalid, recreating triggers validation
        with pytest.raises(ValidationError):
            DStabilityStructure(**dict(dm.datastructure))

    @pytest.mark.unittest
    def test_foreign_keys(self):
        fk = ForeignKeys()
        mapping = fk.class_fields

        # Validate "Stage" has 12 Id like fields defined
        assert "Stage" in mapping
        assert len(mapping["Stage"]) == 12

    @pytest.mark.unittest
    def test_find_subclass_from_children(self):
        # Setup
        dm = DStabilityModel()
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/Tutorial_v20_2_1")
        )
        dm.parse(test_filepath)

        # Verify expecations
        assert isinstance(dm.datastructure.waternets[0], Waternet)

        # Test
        child_classes = [type(x).__name__ for x in children(dm.datastructure)]

        # Verify result
        assert "PersistableHeadLine" in child_classes

    @pytest.mark.acceptance
    @only_teamcity
    def test_duplicate_stage(self):

        # Setup
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dstability/Tutorial_v20_2_1")
        )
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dstability/"))
            / "duplicate_stages.stix"
        )
        dm = DStabilityModel()
        dm.parse(test_filepath)

        # Test
        dm.datastructure.duplicate_stage(
            0, label="Second default", notes="", unique_start_id=500
        )
        dm.serialize(test_output_filepath)

        # Verify correct execution
        dm.execute()
        assert dm.datastructure

    @pytest.mark.unittest
    def test_add_empty_stage(self):
        # Setup
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dstability/"))
            / "default_stages.stix"
        )
        dm = DStabilityModel(filename=None)
        unique_start_id = 512

        # Test
        stage_id, unique_id = dm.datastructure.add_default_stage(
            label="Second default", notes="", unique_start_id=unique_start_id
        )
        dm.serialize(test_output_filepath)  # For manual testing

        # Verify
        assert stage_id == 1
        assert unique_id > unique_start_id
