import os
from random import randint
from typing import List, get_type_hints, _GenericAlias, Type, Tuple, Dict
import pytest

from geolib.models.base_model import BaseModel
from geolib.models.dseries_parser import (
    DSeriesMatrixTreeStructure,
    DSeriesTreeStructure,
    DSeriesListTreeStructureCollection,
    DSeriesStructure,
    make_key,
)


class TestParserUtil:
    @pytest.mark.unittest
    def test_make_key_function(self):
        in_key = "GROUP - KEY-WITH (ODD.NAME)"
        out_key = "group___key__with_odd____name"
        assert make_key(in_key) == out_key


class DummyTreeStructure(DSeriesTreeStructure):
    simple_property: str
    list_property: List[int]


class DummyListTreeStructureCollection(DSeriesListTreeStructureCollection):
    tabbedtreestructures: List[DummyTreeStructure]


class TestDSeriesTreeStructure:
    @pytest.mark.unittest
    def test_given_unmatchedpropertyvaluestext_when_parse_text_lines_then_raises_valueerror(
        self,
    ):
        # 1. Set up test data
        text_lines = [["2"], ["4"], ["2"]]
        expected_error = f"Expected 4 values for property list_property."
        parsed_structure = None
        # 2. Run and verify
        with pytest.raises(ValueError) as e_info:
            parsed_structure = DummyTreeStructure.parse_text_lines(text_lines)

        # 3. Verify final expectations
        assert parsed_structure is None
        assert str(e_info.value) == expected_error

    class DummyTreeStructureListFirst(DSeriesTreeStructure):
        list_property: List[int]
        single_property: int

    @pytest.mark.unittest
    def test_given_notenoughlistvalues_when_parse_text_lines_then_raises_valueerror(self):
        # 1. Set up test data
        text_lines = ["2", "4", "2"]
        expected_error = f"Expected text line property for single_property."
        parsed_structure = None
        # 2. Run and verify
        with pytest.raises(ValueError) as e_info:
            parsed_structure = self.DummyTreeStructureListFirst.parse_text_lines(
                text_lines
            )

        # 3. Verify final expectations
        assert parsed_structure is None
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_enoughlist_values_when_parse_text_lines_then_parses_allproperties(
        self,
    ):
        # 1. Set up test data
        text_lines = [["2"], ["4", "2"], ["42"]]
        parsed_structure = None

        # 2. Run and verify
        (
            parsed_structure,
            consumed_lines,
        ) = self.DummyTreeStructureListFirst.parse_text_lines(text_lines)

        # 3. Verify final expectations
        assert parsed_structure
        assert consumed_lines == len(text_lines)
        assert parsed_structure.list_property == [4, 2]
        assert parsed_structure.single_property == 42

    @pytest.mark.unittest
    def test_given_unmatchedpropertylinestext_when_parse_then_raises_valueerror(self):
        # 1. Set up test data
        text_lines = ["2"]
        expected_error = (
            ""
            + f"There should be at least 2"
            + f" fields to correctly initalize object {DummyTreeStructure}"
        )
        parsed_structure = None
        # 2. Run and verify
        with pytest.raises(ValueError) as e_info:
            parsed_structure = DummyTreeStructure.parse_text_lines(text_lines)

        # 3. Verify final expectations
        assert parsed_structure is None
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_linesofproperties_when_parse_then_creates_class_with_properties(self):
        # 1. Set up test data.
        text_lines = [["2"], ["2"], ["4", "2"]]
        expected_id = "2"
        expected_values = [4, 2]

        # 2. Run test.
        parsed_structure, consumed_lines = DummyTreeStructure.parse_text_lines(text_lines)

        # 3. Verify final expectations
        assert parsed_structure, "No structure was parsed."
        assert consumed_lines == len(text_lines)
        assert parsed_structure.simple_property == expected_id
        assert parsed_structure.list_property == expected_values

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "list_size",
        [
            pytest.param(9, id="Below limit"),
            pytest.param(15, id="One extra line"),
            pytest.param(31, id="Three extra lines"),
        ],
    )
    def test_given_dummytreestructuretext_with_multiplecurvelines_when_parse_text_then_creates_correctly(
        self, list_size: int
    ):
        # 1. Set up test data
        single_property_value = "dummy_id"
        max_line_elements = 10
        values = [randint(0, 100) for idx in range(1, list_size)]
        text_to_parse = (
            ""
            + f"{single_property_value} - Structure id\n"
            + f"{len(values)} - number of elements in list\n"
        )
        step_values = [
            values[i : i + max_line_elements]
            for i in range(0, len(values), max_line_elements)
        ]
        for step_value in step_values:
            text_to_parse += " ".join([str(value) for value in step_value])
            text_to_parse += "\n"

        # 2. Run test
        parsed_structure = DummyTreeStructure.parse_text(text_to_parse)

        # 3. Verify final expectation
        assert isinstance(parsed_structure, DSeriesTreeStructure)
        assert parsed_structure.simple_property == single_property_value
        assert (
            parsed_structure.list_property == values
        ), "Parsed values don't match expectations."

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "list_size",
        [
            pytest.param(9, id="Below limit"),
            pytest.param(15, id="One extra line"),
            pytest.param(31, id="Three extra lines"),
        ],
    )
    def test_given_dummytreestructuretext_with_multiplecurvelines_when_parse_text_lines_then_creates_correctly(
        self, list_size: int
    ):
        # 1. Set up test data
        single_property_value = "dummy_id"
        max_line_elements = 10
        values = [randint(0, 100) for idx in range(1, list_size)]
        step_values = [
            values[i : i + max_line_elements]
            for i in range(0, len(values), max_line_elements)
        ]
        text_lines_to_parse = [[single_property_value]]
        text_lines_to_parse.append([str(len(values))])
        for step in step_values:
            text_lines_to_parse.append([str(s_value) for s_value in step])

        # 2. Run test
        parsed_structure, read_lines = DummyTreeStructure.parse_text_lines(
            text_lines_to_parse
        )

        # 3. Verify final expectation
        assert isinstance(parsed_structure, DSeriesTreeStructure)
        assert read_lines == len(text_lines_to_parse)
        assert parsed_structure.simple_property == single_property_value
        assert (
            parsed_structure.list_property == values
        ), "Parsed values don't match expectations."


class TestDSeriesListTreeStructureCollection:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "separator", [pytest.param(" ", id="Space"), pytest.param("\t", id="Tabulated")]
    )
    def test_given_listtreestructurecollectiontext_when_parse_then_returns_object(
        self, separator
    ):
        # 1. Set up test model.
        structure_name = "my_structure"
        structure_content = {
            "1": [randint(0, 100) for idx in range(1, 4)],
            "2": [randint(0, 100) for idx in range(1, 24)],
            "3": [randint(0, 100) for idx in range(1, 2)],
            "4": [randint(0, 100) for idx in range(1, 42)],
        }

        max_elements_per_line = 10
        content_lines = f"{len(structure_content)} - Number of {structure_name}\n"
        for s_key, s_value in structure_content.items():
            content_lines += (
                ""
                + f"{separator}{s_key} - Structure id\n"
                + f"{separator*2}{len(s_value)} - number of curves on boundary, next line(s) are curvenumbers\n"
            )
            step_values = [
                s_value[i : i + max_elements_per_line]
                for i in range(0, len(s_value), max_elements_per_line)
            ]
            for step_value in step_values:
                content_lines += f"{separator*3}"
                content_lines += f"{separator}".join([str(value) for value in step_value])
                content_lines += "\n"

        # 2. Run test.
        parsed_collection = DummyListTreeStructureCollection.parse_text(content_lines)

        # 3. Verify final expectations.
        assert parsed_collection, "No structure was generated."
        assert isinstance(parsed_collection, DSeriesListTreeStructureCollection)
        parsed_dict_collection = dict(parsed_collection)
        assert len(parsed_dict_collection["tabbedtreestructures"]) == len(
            structure_content
        )
        for parsed_structure in parsed_dict_collection["tabbedtreestructures"]:
            parsed_as_dict = dict(parsed_structure)
            structure_id = parsed_as_dict["simple_property"]
            assert structure_content[structure_id] == parsed_as_dict["list_property"], (
                "" + f"Structure {structure_id} has not been parsed correctly."
            )

    @pytest.mark.unittest
    def test_given_unmatchedstructurestext_when_parse_then_raises_valueerror(self):
        # 1. Set up test data
        text = "2 - structures\n"
        expected_error = "" + "Expected 2 structures, but missing text lines for 2."
        parsed_structure = None
        # 2. Run and verify
        with pytest.raises(ValueError) as e_info:
            parsed_structure = DummyListTreeStructureCollection.parse_text(text)

        # 3. Verify final expectations
        assert parsed_structure is None
        assert str(e_info.value) == expected_error


class DummyMatrixStructure(DSeriesStructure):
    first_prop: str
    second_prop: str
    third_prop: str


class TestDSeriesMatrixTreeStructure:
    class DummyMatrixTreeStructure(DSeriesMatrixTreeStructure):
        dummymatrixtreestructure: List[DummyMatrixStructure]

    @pytest.mark.unittest
    def test_given_unequal_lines_when_parse_text_then_raise_exception(self):
        # 1. Set up test data
        text_to_parse = "" + "2 - Number of structures\n" + "1 0 2"
        return_result = None
        expected_error = "" + f"Number of rows does not match expected (2)."
        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            return_result = TestDSeriesMatrixTreeStructure.DummyMatrixTreeStructure.parse_text(
                text_to_parse
            )

        # 3. Verify final expectations.
        assert return_result is None, "No structure should have been generated."
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_equal_lines_when_parse_text_then_gets_new_structures(self):
        # 1. Set up test data
        values = [
            ["2", "4", "2"],
            ["4", "2", "4"],
        ]
        text_to_parse = "2 - Number of structures\n"
        for value in values:
            text_to_parse += "" + " ".join(value) + "\n"
        return_result = None

        # 2. Run test
        return_result = TestDSeriesMatrixTreeStructure.DummyMatrixTreeStructure.parse_text(
            text_to_parse
        )

        # 3. Verify final expectations.
        assert return_result, "Structure should have been generated."
        assert isinstance(return_result, DSeriesMatrixTreeStructure)
        for idx, result in enumerate(return_result.dummymatrixtreestructure):
            assert result.first_prop == values[idx][0]
            assert result.second_prop == values[idx][1]
            assert result.third_prop == values[idx][2]

    @pytest.mark.unittest
    def test_given_unequal_fields_when_parse_structure_then_raise_exception(self):
        # 1. Set up test data
        text_fields = ["1", "2"]
        return_result = None
        expected_error = (
            "" + f"There should be 3 fields to initalize object {DummyMatrixStructure}"
        )
        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            return_result = TestDSeriesMatrixTreeStructure.DummyMatrixTreeStructure.parse_structure(
                text_fields
            )

        # 3. Verify final expectations.
        assert return_result is None, "No structure should have been generated."
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_equal_fields_when_parse_structure_then_returns(self):
        # 1. Set up test data.
        text_fields = ["2", "4", "2"]
        parsed_structure = None

        # 2. Run test.
        parsed_structure = TestDSeriesMatrixTreeStructure.DummyMatrixTreeStructure.parse_structure(
            text_fields
        )

        # 3. Verify final expectations.
        assert parsed_structure is not None
        assert isinstance(parsed_structure, DSeriesStructure)
        assert parsed_structure.first_prop == text_fields[0]
        assert parsed_structure.second_prop == text_fields[1]
        assert parsed_structure.third_prop == text_fields[2]
