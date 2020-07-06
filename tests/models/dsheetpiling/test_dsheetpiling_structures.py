import pytest
from typing import List, Any
from geolib.models.dsheetpiling.dsheetpiling_structures import DSheetpilingSurchargeLoad


class TestDSheetpilingSurchargeLoad:
    @pytest.mark.unittest
    def test_when_get_list_field_names_returns_all_fields_and_point(self):
        class dummy_with_lists(DSheetpilingSurchargeLoad):
            property_one: List[str]
            property_two: str

        expected_output = ["property_one", "point"]
        assert dummy_with_lists.get_list_field_names() == expected_output

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "mapped_key, expected_value",
        [pytest.param("name", ""), pytest.param("points", [])],
    )
    def test_given_empty_dict_when_get_validated_mappings_sets_default_to_mapped_keys(
        self, mapped_key: str, expected_value: Any
    ):
        # 1. Run test
        output_dict = DSheetpilingSurchargeLoad.get_validated_mappings({})

        # 2. Verify final expectations
        assert output_dict[mapped_key] == expected_value

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "input_key, replace_key",
        [
            pytest.param("surcharge_load", "name"),
            pytest.param("", "name"),
            pytest.param("point", "points"),
        ],
    )
    def test_when_get_validated_mappings_replaces_input_key_with_mapped_key(
        self, input_key: str, replace_key: str
    ):
        # 1. Prepare test data
        value = "dummy value"
        test_dict = {input_key: value}

        # 2. Run test
        output_dict = DSheetpilingSurchargeLoad.get_validated_mappings(test_dict)

        # 3. Verify final expectations
        assert output_dict
        assert input_key not in output_dict.keys()
        assert output_dict[replace_key] == value
