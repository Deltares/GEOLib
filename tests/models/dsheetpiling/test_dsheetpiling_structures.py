from typing import Any

import pytest

from geolib.errors import ParserError
from geolib.models.dseries_parser import DSeriesStructure
from geolib.models.dsheetpiling.dsheetpiling_structures import (
    DSheetpilingSurchargeLoad,
    DSheetpilingTableEntry,
    DSheetpilingUnwrappedTable,
    DSheetpilingWithNumberOfRowsTable,
)


class TestDSheetpilingSurchargeLoad:
    @pytest.mark.unittest
    def test_when_get_list_field_names_returns_all_fields_and_point(self):
        class dummy_with_lists(DSheetpilingSurchargeLoad):
            property_one: list[str]
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


class TestDSheetpilingWithNumberOfRowsTable:
    @pytest.mark.unittest
    def test_given_table_with_number_of_rows_on_top_structure_is_parsed(self):
        # 1. Define test data
        class test_structure(DSheetpilingWithNumberOfRowsTable):
            test_structure: list[dict[str, float]]

        text_to_parse = """[TABLE]
            DataCount=2
            [COLUMN INDICATION]
            A
            B
            C
            [END OF COLUMN INDICATION]
            [DATA]
            4   2   4
            2.4 4.2 42
            [END OF DATA]
            [END OF TABLE]
        """
        # 2. Run test
        parsed_structure = test_structure.parse_text(text_to_parse)
        # 3. Verify final expectations
        assert parsed_structure
        assert len(parsed_structure.test_structure) == 2
        assert parsed_structure.test_structure[0]["a"] == 4
        assert parsed_structure.test_structure[0]["b"] == 2
        assert parsed_structure.test_structure[0]["c"] == 4
        assert parsed_structure.test_structure[1]["a"] == 2.4
        assert parsed_structure.test_structure[1]["b"] == 4.2
        assert parsed_structure.test_structure[1]["c"] == 42


class TestDSheetpilingTableEntry:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "separator", [pytest.param(" ", id="Space"), pytest.param("\t", id="Tabulator.")]
    )
    def test_given_text_with_columns_returns_list_structure(self, separator: str):
        class DummyUnwrapped(DSheetpilingTableEntry):
            prop_1: str
            prop_2: float

        # 1. Text to parse:
        text_to_parse = f"""1{separator}4.2{separator}{separator}property_two"""
        # 2. Run test
        unwrapped_struct = DummyUnwrapped.parse_text(text_to_parse)
        # 3. Verify expectations.
        assert unwrapped_struct.prop_1 == "property_two"
        assert unwrapped_struct.prop_2 == 4.2

    @pytest.mark.unittest
    def test_given_text_with_composite_name_returns_list_structure(self):
        class DummyUnwrapped(DSheetpilingTableEntry):
            prop_1: str
            prop_2: float

        # 1. Text to parse:
        text_to_parse = """1 4.2 property two"""
        # 2. Run test
        unwrapped_struct = DummyUnwrapped.parse_text(text_to_parse)
        # 3. Verify expectations.
        assert unwrapped_struct.prop_1 == "property two"
        assert unwrapped_struct.prop_2 == 4.2


class TestDSheetpilingUnwrappedTable:
    @pytest.mark.unittest
    def test_given_table_parse_structure(self):
        class DummyTableEntry(DSheetpilingTableEntry):
            name: str
            value: float

        class DummyUnwrappedTable(DSheetpilingUnwrappedTable):
            dummyunwrappedtable: list[DummyTableEntry]

        # 1. Define test data
        text_to_parse = """ 2 values
            nr value name
            1 4.2 first value
            2 24 second value"""
        # 2. Run test
        structure = DummyUnwrappedTable.parse_text(text_to_parse)
        # 3. Validate output.
        assert structure.dummyunwrappedtable
        assert len(structure.dummyunwrappedtable) == 2
        assert structure.dummyunwrappedtable[0].value == 4.2
        assert structure.dummyunwrappedtable[0].name == "first value"
        assert structure.dummyunwrappedtable[1].value == 24
        assert structure.dummyunwrappedtable[1].name == "second value"

    @pytest.mark.unittest
    def test_given_table_with_wrong_number_of_rows_parse_structure(self):
        class DummyTableEntry(DSheetpilingTableEntry):
            name: str
            value: float

        class DummyUnwrappedTable(DSheetpilingUnwrappedTable):
            dummyunwrappedtable: list[DummyTableEntry]

        # 1. Define test data
        text_to_parse = """ 1 value
            nr value name
            1 4.2 first value
            2 24 second value"""
        # 2. Run test
        with pytest.raises(ParserError) as e_info:
            DummyUnwrappedTable.parse_text(text_to_parse)
