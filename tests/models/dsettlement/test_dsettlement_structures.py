import pytest

from geolib.models.dseries_parser import DSeriesRepeatedGroupedProperties
from geolib.models.dsettlement.dsettlement_structures import (
    ComplexVerticalSubstructure,
    DSerieRepeatedTableStructure,
)


class TestDSerieRepeatedTableStructure:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "property_name, expected_value",
        [("this_is_also_a_list", True), ("column_indication", False)],
    )
    def test_given_group_keys_when_group_value_is_list_then_return_expected(
        self, property_name: str, expected_value: bool
    ):
        class dummy_class(DSerieRepeatedTableStructure):
            pass

        assert dummy_class.group_value_is_list(property_name) is expected_value

    @pytest.mark.integrationtest
    def test_given_text_when_parse_text_then_return_structure(self):
        class repeated_table(DSerieRepeatedTableStructure):
            repeated_table: dict[int, list[dict[str, int]]]

        # 1. Define test data
        text_to_parse = """[COLUMN INDICATION]
            A
            B
            C
            [END OF COLUMN INDICATION]
            [GROUP DATA]
            3
            1 1 1
            2 2 2
            2 3 4
            [END OF GROUP DATA]
            [GROUP DATA]
            4
            1 1 1
            4 3 2
            2 3 4
            [END OF GROUP DATA]"""
        expected_dict = {
            3: [
                {"a": 1, "b": 1, "c": 1},
                {"a": 2, "b": 2, "c": 2},
                {"a": 2, "b": 3, "c": 4},
            ],
            4: [
                {"a": 1, "b": 1, "c": 1},
                {"a": 4, "b": 3, "c": 2},
                {"a": 2, "b": 3, "c": 4},
            ],
        }

        # 2. Run test
        parsed_struct = repeated_table.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_struct.repeated_table == expected_dict

    @pytest.mark.unittest
    def test_given_too_many_groups_when_get_validated_mappings_raises(self):
        # 1. Define test data.
        class_name = DSerieRepeatedTableStructure.__name__.lower()
        expected_error = f"Expected 2 groups for {class_name} but got 0."

        # 2. Run test.
        with pytest.raises(ValueError) as e_info:
            DSerieRepeatedTableStructure.get_validated_mappings({})

        # 3. Verify final expectations.
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_repeated_groups_ids_when_get_validated_mappings_raises(self):
        # 1. Define test data.
        class_name = DSerieRepeatedTableStructure.__name__.lower()
        group_key = "dumb_key"
        expected_error = f"No repeated table keys ({group_key}) allowed for {class_name}."
        test_dict = {
            "column_indication": "a\nb\n",
            "group_data": [f"{group_key}\n4 2\n", "24\n2 4\n", f"{group_key}\n0 5\n"],
        }

        # 2. Run test.
        with pytest.raises(ValueError) as e_info:
            DSerieRepeatedTableStructure.get_validated_mappings(test_dict)

        # 3. Verify final expectations.
        assert str(e_info.value) == expected_error
