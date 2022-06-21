import logging
import os
from random import randint
from typing import Dict, List, Tuple, Type, _GenericAlias, get_type_hints

import pytest
from pydantic.error_wrappers import ValidationError

from geolib.models.base_model import BaseModel
from geolib.models.dseries_parser import (
    DSeriesInlineMappedProperties,
    DSeriesInlineProperties,
    DSeriesInlineReversedProperties,
    DSeriesMatrixTreeStructureCollection,
    DSeriesRepeatedGroupedProperties,
    DSeriesRepeatedGroupsWithInlineMappedProperties,
    DSeriesStructure,
    DSeriesStructureCollection,
    DSeriesTableStructure,
    DSeriesTreeStructure,
    DSeriesTreeStructureCollection,
    DSeriesUnmappedNameProperties,
    DSeriesWrappedTableStructure,
    DSerieVersion,
    get_line_property_key_value,
    get_line_property_value,
    make_key,
)


class TestParserUtil:
    @pytest.mark.unittest
    def test_make_key_function(self):
        in_key = "GROUP - KEY-WITH (ODD.NAME)"
        out_key = "group___key__with_odd____name"
        assert make_key(in_key) == out_key

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text, expected_value",
        [
            pytest.param("4.2 : property_value", "4.2"),
            pytest.param("4.2 = property_value", "4.2"),
            pytest.param("property_value", "property_value"),
            pytest.param("property value", "property"),
            pytest.param("4.2 :", "4.2"),
            pytest.param("4.2 =", "4.2"),
            pytest.param("= property_value", ""),
            pytest.param(": property_value", ""),
            pytest.param("=", ""),
        ],
    )
    def test_get_line_property_value_reversed_key_true(
        self, text: str, expected_value: str
    ):
        assert get_line_property_value(text, reversed_key=True) == expected_value

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text, expected_value",
        [
            pytest.param("property_value: 4.2", "4.2"),
            pytest.param("property_value = 4.2", "4.2"),
            pytest.param("property_value", "property_value"),
            pytest.param("property value", "property"),
            pytest.param("property_value =", ""),
            pytest.param("property_value :", ""),
            pytest.param(": 4.2", "4.2"),
            pytest.param("= 4.2", "4.2"),
            pytest.param("=", ""),
        ],
    )
    def test_get_line_property_value_reversed_key_false(
        self, text: str, expected_value: str
    ):
        assert get_line_property_value(text, reversed_key=False) == expected_value

    @pytest.mark.parametrize(
        "text, expected_value",
        [
            pytest.param("property_value: 4.2", ("property_value", "4.2")),
            pytest.param("property_value = 4.2", ("property_value", "4.2")),
            pytest.param("property_value", ("", "property_value")),
            pytest.param("property value", ("", "property")),
            pytest.param("property_value =", ("property_value", "")),
            pytest.param("property_value :", ("property_value", "")),
            pytest.param("= 4.2", ("", "4.2")),
            pytest.param(": 4.2", ("", "4.2")),
            pytest.param("=", ("", "")),
        ],
    )
    @pytest.mark.unittest
    def test_get_line_property_key_value_reversed_key_false(
        self, text: str, expected_value: Tuple[str, str]
    ):
        assert get_line_property_key_value(text, reversed_key=False) == expected_value

    @pytest.mark.parametrize(
        "text, expected_value",
        [
            pytest.param("4.2 : property_value", ("property_value", "4.2")),
            pytest.param("4.2 = property_value", ("property_value", "4.2")),
            pytest.param("property_value", ("", "property_value")),
            pytest.param("property value", ("", "property")),
            pytest.param("= property_value", ("property_value", "")),
            pytest.param(": property_value", ("property_value", "")),
            pytest.param("4.2 :", ("", "4.2")),
            pytest.param("4.2 =", ("", "4.2")),
            pytest.param("=", ("", "")),
        ],
    )
    @pytest.mark.unittest
    def test_get_line_property_key_value_reversed_key_true(
        self, text: str, expected_value: Tuple[str, str]
    ):
        assert get_line_property_key_value(text, reversed_key=True) == expected_value


class DummyTreeStructure(DSeriesTreeStructure):
    simple_property: int
    list_property: List[int]


class DummyListTreeStructureCollection(DSeriesTreeStructureCollection):
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
        expected_id = 2
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
        single_property_value = "123"
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
        assert str(parsed_structure.simple_property) == single_property_value
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
        single_property_value = "123"
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
        assert str(parsed_structure.simple_property) == single_property_value
        assert (
            parsed_structure.list_property == values
        ), "Parsed values don't match expectations."

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "separator", [pytest.param(":", id="Two points"), pytest.param("=", id="Equal")]
    )
    def test_given_structuretext_with_multiplesubstructures_property_then_allextracted(
        self, separator: str
    ):
        class tp_test_simple_element(DSeriesTreeStructure):
            name: str
            val_1: float

        class tp_test_composite_element(DSeriesTreeStructure):
            struct_name: str
            val_0: float
            composite_val: List[tp_test_simple_element]

        # 1. Define test data.
        text_to_parse = (
            ""
            + "Struct_1\n"
            + f"4.2 {separator} val_0\n"
            + f"2 {separator} composite_val\n"
            + "SimpleElement \n"
            + f"42 {separator} val_1\n"
            + "OtherElement \n"
            + f"24 {separator} val_1\n"
        )

        # 2. Run test.
        struct_result = tp_test_composite_element.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert isinstance(struct_result, tp_test_composite_element)
        assert struct_result.struct_name == "Struct_1"
        assert struct_result.val_0 == 4.2
        assert len(struct_result.composite_val) == 2
        first_element = struct_result.composite_val[0]
        assert isinstance(first_element, tp_test_simple_element)
        assert first_element.name == "SimpleElement"
        assert first_element.val_1 == 42
        last_element = struct_result.composite_val[1]
        assert isinstance(last_element, tp_test_simple_element)
        assert last_element.name == "OtherElement"
        assert last_element.val_1 == 24


class TestDSeriesTreeStructureCollection:
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
        assert isinstance(parsed_collection, DSeriesTreeStructureCollection)
        parsed_dict_collection = dict(parsed_collection)
        assert len(parsed_dict_collection["tabbedtreestructures"]) == len(
            structure_content
        )
        for parsed_structure in parsed_dict_collection["tabbedtreestructures"]:
            parsed_as_dict = dict(parsed_structure)
            structure_id = parsed_as_dict["simple_property"]
            assert (
                structure_content[str(structure_id)] == parsed_as_dict["list_property"]
            ), ("" + f"Structure {structure_id} has not been parsed correctly.")

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "separator", [pytest.param(":", id="Two points"), pytest.param("=", id="Equal")]
    )
    def test_given_textwith_simplestructure_then_extracted(self, separator: str):
        class tp_test_element(DSeriesTreeStructure):
            struct_name: str
            val_1: float
            val_2: float

        class tp_test_treecollection(DSeriesTreeStructureCollection):
            tree_collection: List[tp_test_element]

        # 1. Define test data.
        text_to_parse = (
            ""
            + "1 = number of items\n"
            + "Struct_1\n"
            + f"4.2 {separator} val_1\n"
            + f"2.4 {separator} val_2\n"
        )

        # 2. Run test.
        struct_result = tp_test_treecollection.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert isinstance(struct_result, tp_test_treecollection)
        assert len(struct_result.tree_collection) == 1
        read_element = struct_result.tree_collection[0]
        assert isinstance(read_element, tp_test_element)
        assert read_element.val_1 == 4.2
        assert read_element.val_2 == 2.4

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "separator", [pytest.param(":", id="Two points"), pytest.param("=", id="Equal")]
    )
    def test_given_textwith_complexstructure_then_extracted(self, separator: str):
        class tp_test_simplestruct(DSeriesTreeStructure):
            prop_1: float
            prop_2: float

        class tp_test_collection(DSeriesTreeStructureCollection):
            tp_collection: List[tp_test_simplestruct]

        class tp_test_compositestruct(DSeriesTreeStructure):
            struct_name: str
            val_1: float
            val_2: float
            extra_struct: tp_test_collection

        class tp_test_treecollection(DSeriesTreeStructureCollection):
            tree_collection: List[tp_test_compositestruct]

        # 1. Define test data.
        text_to_parse = (
            ""
            + "1 = number of items\n"
            + "Struct_1\n"
            + f"4.2 {separator} val_1\n"
            + f"2.4 {separator} val_2\n"
            + f"1{separator} extra_struct \n"
            + f"24{separator} prop_1 \n"
            + f"42{separator} prop_2"
        )

        # 2. Run test.
        struct_result = tp_test_treecollection.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert isinstance(struct_result, tp_test_treecollection)
        assert len(struct_result.tree_collection) == 1
        read_element = struct_result.tree_collection[0]
        assert isinstance(read_element, tp_test_compositestruct)
        assert read_element.val_1 == 4.2
        assert read_element.val_2 == 2.4
        assert len(read_element.extra_struct.tp_collection) == 1
        substruct = read_element.extra_struct.tp_collection[0]
        assert isinstance(substruct, tp_test_simplestruct)
        assert substruct.prop_1 == 24
        assert substruct.prop_2 == 42

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


class DummyMatrixStructure(DSeriesTreeStructure):
    first_prop: str
    second_prop: str
    third_prop: str


class TestDSeriesTreeStructureAsMatrix:
    class DummyMatrixTreeStructureCollection(DSeriesMatrixTreeStructureCollection):
        dummymatrixtreestructure: List[DummyMatrixStructure]

    @pytest.mark.unittest
    def test_given_unequal_lines_when_parse_text_then_raise_exception(self):
        # 1. Set up test data
        text_to_parse = "" + "2 - Number of structures\n" + "1 0 2"
        return_result = None
        expected_error = "Expected 2 structures, but missing text lines for 1."
        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            return_result = TestDSeriesTreeStructureAsMatrix.DummyMatrixTreeStructureCollection.parse_text(
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
        return_result = TestDSeriesTreeStructureAsMatrix.DummyMatrixTreeStructureCollection.parse_text(
            text_to_parse
        )

        # 3. Verify final expectations.
        assert return_result, "Structure should have been generated."
        assert isinstance(return_result, DSeriesMatrixTreeStructureCollection)
        for idx, result in enumerate(return_result.dummymatrixtreestructure):
            assert result.first_prop == values[idx][0]
            assert result.second_prop == values[idx][1]
            assert result.third_prop == values[idx][2]

    @pytest.mark.unittest
    def test_given_unequal_fields_when_parse_text_lines_then_raise_exception(self):
        # 1. Set up test data
        text_fields = ["1", "2"]
        return_result = None
        expected_error = (
            ""
            + f"There should be at least 3 fields to correctly initalize object {DummyMatrixStructure}"
        )
        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            return_result = TestDSeriesTreeStructureAsMatrix.DummyMatrixTreeStructureCollection.parse_text_lines(
                text_fields
            )

        # 3. Verify final expectations.
        assert return_result is None, "No structure should have been generated."
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_equal_fields_when_parse_text_lines_then_returns(self):
        # 1. Set up test data.
        text_fields = ["2", "4", "2"]
        parsed_structure = None

        # 2. Run test.
        parsed_structure, _ = DummyMatrixStructure.parse_text_lines(text_fields)

        # 3. Verify final expectations.
        assert parsed_structure is not None
        assert isinstance(parsed_structure, DSeriesTreeStructure)
        assert parsed_structure.first_prop == text_fields[0]
        assert parsed_structure.second_prop == text_fields[1]
        assert parsed_structure.third_prop == text_fields[2]


class TestDSeriesTableStructure:
    @pytest.mark.integrationtest
    def test_given_column_with_string_value_when_parse_then_returns_valid_structure(self):
        # 1. Define test data
        class test_table(DSeriesTableStructure):
            test_table: List[Dict[str, str]]

        string_value = "This is a string value"
        text_to_parse = f"""[COLUMN INDICATION]
            string_column
            [END OF COLUMN INDICATION]
            [DATA]
            1
            '{string_value}'
            [END OF DATA]"""
        # 2. Run test.
        parsed_structure = test_table.parse_text(text_to_parse)
        # 3. Validate final expectations.
        assert parsed_structure
        assert len(parsed_structure.test_table) == 1
        assert parsed_structure.test_table[0]["string_column"] == string_value


class TestDSeriesWrappedTableStructure:
    @pytest.mark.unittest
    def test_given_table_without_number_of_rows_structure_is_parsed(self):
        # 1. Prepare test data
        class test_structure(DSeriesWrappedTableStructure):
            test_structure: List[Dict[str, float]]

        text_to_parse = """
            [TABLE]
            [COLUMN INDICATION]
            Moment
            Shear force
            Displacements
            [END OF COLUMN INDICATION]
            [DATA]
                0.00000      0.00000   -193.89808
            [END OF DATA]
            [END OF TABLE]
            """
        # 2. Run test
        parsed_structure = test_structure.parse_text(text_to_parse)
        # 3. Verify final expectations.
        assert parsed_structure
        assert len(parsed_structure.test_structure) == 1
        parsed_value = parsed_structure.test_structure[0]
        assert parsed_value["moment"] == 0
        assert parsed_value["shear_force"] == 0
        assert parsed_value["displacements"] == -193.89808


class TestDSeriesInlineProperties:

    test_values = {"property_1": 42, "property_2": 24, "property_3": 4.2}

    valid_inline_properties = "property_1 = 42\n" + "property_2 = 24"
    valid_grouped_properties = "[PROPERTY_3]\n" + "4.2\n" + "[END OF PROPERTY_3]"

    class only_inline(DSeriesInlineProperties):
        property_1: int
        property_2: int

    class only_grouped(DSeriesInlineProperties):
        property_3: float

    class combined(DSeriesInlineProperties):
        property_1: int
        property_2: int
        property_3: float

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_input, class_to_parse",
        [
            pytest.param(valid_inline_properties, only_inline, id="Inline properties"),
            pytest.param(valid_grouped_properties, only_grouped, id="Group properties"),
            pytest.param(
                "\n".join([valid_inline_properties, valid_grouped_properties]),
                combined,
                id="Mixed properties",
            ),
        ],
    )
    def test_given_text_with_any_kind_of_properties_when_parse_text_then_returns_structure(
        self, text_input: str, class_to_parse: Type
    ):
        # 1. Run test.
        parsed_structure = class_to_parse.parse_text(text_input)

        # 2. Verify final expectations.
        assert parsed_structure is not None
        for key, value in dict(parsed_structure).items():
            assert self.test_values[key] == value

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_input, class_to_parse",
        [
            pytest.param(valid_inline_properties, only_inline, id="Inline properties"),
            pytest.param(valid_grouped_properties, only_grouped, id="Group properties"),
            pytest.param(
                "\n".join([valid_inline_properties, valid_grouped_properties]),
                combined,
                id="Mixed properties",
            ),
        ],
    )
    def test_given_text_with_header_when_parse_text_then_returns_structure(
        self, text_input: str, class_to_parse: Type
    ):
        # 1. Run test.
        class with_header(class_to_parse):
            @classmethod
            def header_lines(cls) -> int:
                return 2

        header_lines = "Header line 1\n" + "Header line 2\n"
        parsed_structure = with_header.parse_text(header_lines + text_input)

        # 2. Verify final expectations.
        assert parsed_structure is not None
        for key, value in dict(parsed_structure).items():
            assert self.test_values[key] == value

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse",
        [
            pytest.param("[property_1]\n[end of property_1]", id="Grouped"),
            pytest.param(" = property_1", id="Inline equal"),
            pytest.param(" : property_1", id="Inline two points"),
        ],
    )
    def test_given_text_with_empty_properties_when_parse_text_then_returns_structure_with_default(
        self, text_to_parse: str
    ):
        # 1. Define test data.
        class with_defaults(DSeriesInlineProperties):
            property_1: int = 42

        parsed_structure = None

        # 2. Run test.
        with pytest.raises(ValidationError):
            parsed_structure = with_defaults.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_structure is None

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text_to_parse, expected_key, expected_result",
        [
            pytest.param("key: value", "dummy_key", ("dummy_key", "value")),
            pytest.param("key= value", "dummy_key", ("dummy_key", "value")),
            pytest.param("value", "dummy_key", ("dummy_key", "value")),
            pytest.param("", "dummy_key", ("dummy_key", "")),
        ],
    )
    def test_given_text_without_key_when_get_property_key_value_then_returns_expected_property(
        self, text_to_parse: str, expected_key: str, expected_result: Tuple[str, str]
    ):
        # 1. Define test data:
        expected_key = "dummy_key"

        # 2. Run test
        key, value = DSeriesInlineMappedProperties.get_property_key_value(
            text_to_parse, expected_key
        )

        # 3. Verify final expectations.
        assert key, value == expected_result


class TestDSeriesInlineReversedProperties:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse",
        [
            pytest.param("[property_1]\n[end of property_1]", id="Grouped"),
            pytest.param(" = property_1", id="Inline equal"),
            pytest.param(" : property_1", id="Inline two points"),
        ],
    )
    def test_given_text_with_empty_properties_when_parse_text_then_returns_structure_with_default(
        self, text_to_parse: str
    ):
        # 1. Define test data.
        class with_defaults(DSeriesInlineReversedProperties):
            property_1: int = 42

        parsed_structure = None

        # 2. Run test.
        with pytest.raises(ValidationError):
            parsed_structure = with_defaults.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_structure is None


class TestDSeriesInlineMappedProperties:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text_to_parse, expected_key, expected_result",
        [
            pytest.param("key: value", "dummy_key", ("key", "value")),
            pytest.param("key= value", "dummy_key", ("key", "value")),
            pytest.param("value", "dummy_key", ("dummy_key", "value")),
            pytest.param("", "dummy_key", ("dummy_key", "")),
        ],
    )
    def test_given_text_without_key_when_get_property_key_value_then_returns_expected_property(
        self, text_to_parse: str, expected_key: str, expected_result: Tuple[str, str]
    ):
        # 1. Define test data:
        expected_key = "dummy_key"

        # 2. Run test
        key, value = DSeriesInlineMappedProperties.get_property_key_value(
            text_to_parse, expected_key
        )

        # 3. Verify final expectations.
        assert key, value == expected_result


class TestDSeriesUnmappedNameProperties:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text_to_parse",
        [
            pytest.param("  value without key  "),
            pytest.param("  value without: key  "),
            pytest.param("  value without = key  "),
            pytest.param(" 42 "),
        ],
    )
    def test_given_expected_property_name_when_get_property_key_value_then_returns_stripped_text(
        self, text_to_parse: str
    ):
        # 1. Prepare test data.
        key = "name"

        # 2. Run test.
        parsed_key, parsed_value = DSeriesUnmappedNameProperties.get_property_key_value(
            text=text_to_parse, expected_property=key
        )

        # 3. Verify final expectations.
        assert parsed_key, parsed_value == (key, text_to_parse.strip())

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "text_to_parse, expected_tuple",
        [
            pytest.param("  value without key  ", (None, "value without key")),
            pytest.param("  value with: key  ", ("value with", "key")),
            pytest.param("  value with = key  ", ("value with", "key")),
            pytest.param(" 42 ", (None, "42")),
        ],
    )
    def test_given_no_expected_property_when_get_property_key_value_then_returns_expected(
        self, text_to_parse: str, expected_tuple: Tuple[str, str]
    ):
        # 1. Prepare test data.
        key = "dummy_key"
        expected_key, expected_value = expected_tuple
        if not expected_key:
            expected_key = key

        # 2. Run test.
        parsed_key, parsed_value = DSeriesUnmappedNameProperties.get_property_key_value(
            text=text_to_parse, expected_property=key
        )

        # 3. Verify final expectations.
        assert parsed_key, parsed_value == (expected_key, expected_value)


class TestDSeriesRepeatedGroupedProperties:
    class grouped_properties(DSeriesRepeatedGroupedProperties):
        property_one: int
        property_list: List[str]
        property_two: float

    @pytest.mark.integrationtest
    def test_given_grouped_properties_class_when_parse_inline_text_then_raises(self):
        # This test verifies that the class DSeriesRepeatedGroupedProperties is only being used
        # when the input text is all encapsulated in groups. For other cases a new class should
        # be implemented.
        # 1. Prepare test data
        text = (
            "property one = 42\n"
            + "[PROPERTY LIST]\nLorem\n[END OF PROPERTY LIST]\n"
            + "[PROPERTY LIST]\nIpsum\n[END OF PROPERTY LIST]\n"
            + "property two = 4.2"
        )
        parsed_structure = None

        # 2. Run test.
        with pytest.raises(ValidationError):
            parsed_structure = self.grouped_properties.parse_text(text)

        # 3. Verify final expectations.
        assert not parsed_structure, "No structure should have been generated."


class TestDSeriesRepeatedGroupsWithInlineMappedProperties:
    @pytest.mark.unittest
    def test_given_unmapped_properties_when_get_inline_properties_then_returns_mapped(
        self,
    ):
        # 1. Prepare test data:
        expected_dict = {"property_1": "42", "property_2": "Lorem"}
        input_properties = [" Property 1 = 42 ", "Property 2: Lorem ipsum  "]
        # 2. Run test
        output_dict = (
            DSeriesRepeatedGroupsWithInlineMappedProperties.get_inline_properties(
                input_properties
            )
        )

        # 3. Verify final expectations
        assert output_dict == expected_dict

    @pytest.mark.unittest
    def test_given_repeated_property_when_get_inline_properties_then_returns_only_first_value(
        self,
    ):
        # 1. Prepare test data:
        expected_dict = {"property_1": "42"}
        input_properties = [" Property 1 = 42 ", "Property 1: 24"]
        # 2. Run test
        output_dict = (
            DSeriesRepeatedGroupsWithInlineMappedProperties.get_inline_properties(
                input_properties
            )
        )

        # 3. Verify final expectations
        assert output_dict == expected_dict

    @pytest.mark.integrationtest
    def test_given_mixed_group_with_inline_mapped_when_parse_text_returns_structure(self):
        # 1. Set up test data.
        class mixed_group(DSeriesRepeatedGroupsWithInlineMappedProperties):
            property_one: int
            property_two: float
            property_list: List[str]

        text = (
            "property one = 42\n"
            + "[PROPERTY LIST]\nLorem\n[END OF PROPERTY LIST]\n"
            + "[PROPERTY LIST]\nIpsum\n[END OF PROPERTY LIST]\n"
            + "property two = 4.2"
        )

        # 2. Run test.
        parsed_structure = mixed_group.parse_text(text)

        # 3. Verify final expectations.
        assert parsed_structure
        assert parsed_structure.property_one == 42
        assert parsed_structure.property_two == 4.2
        assert parsed_structure.property_list == ["Lorem", "Ipsum"]


class TestDSeriesStructureCollection:
    @pytest.mark.unittest
    def test_given_collection_with_multiple_properties_when_parse_text_raises_valueerror(
        self,
    ):
        # 1. Define test data.
        class multiple_properties(DSeriesStructureCollection):
            property_one: List[DSeriesStructure]
            property_two: List[DSeriesStructure]

        expected_error = (
            "This type of collection is only meant to have one field but 2 were defined."
        )
        parsed_collection = None

        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            parsed_collection = multiple_properties.parse_text("")

        # 3. Verify final expectations.
        assert parsed_collection is None
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_collection_with_wrong_number_of_structures_when_parse_text_raises_valueerror(
        self,
    ):
        class default_collection(DSeriesStructureCollection):
            collection_one: List[DSeriesStructure]

        # 1. Define test data.
        text_to_parse = (
            "1 = number of structures\n"
            + "[STRUCTURE]\n"
            + "property_dummy = 42\n"
            + "[END OF STRUCTURE]\n"
            + "[STRUCTURE]\n"
            + "property_dummy = 24\n"
            + "[END OF STRUCTURE]"
        )
        expected_error = "Expected 1 groups, but parsed 2."
        parsed_collection = None

        # 2. Run test
        with pytest.raises(ValueError) as e_info:
            parsed_collection = default_collection.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_collection is None
        assert str(e_info.value) == expected_error

    @pytest.mark.unittest
    def test_given_valid_collection_text_when_parse_text_then_returns_structure(
        self,
    ):
        class inline_properties_structure(DSeriesInlineProperties):
            property_dummy: int

        class default_collection(DSeriesStructureCollection):
            data: List[inline_properties_structure]

        # 1. Define test data.
        text_to_parse = (
            "2 = number of structures\n"
            + "[STRUCTURE]\n"
            + "property_dummy = 42\n"
            + "[END OF STRUCTURE]\n"
            + "[STRUCTURE]\n"
            + "property_dummy = 24\n"
            + "[END OF STRUCTURE]"
        )
        parsed_collection = None

        # 2. Run test
        parsed_collection = default_collection.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert len(parsed_collection.data) == 2
        assert parsed_collection.data[0].property_dummy == 42
        assert parsed_collection.data[1].property_dummy == 24


class TestDSeriesVersion:
    @pytest.mark.unittest
    def test_dserie_version(self, caplog):
        class Version(DSerieVersion):
            a: int = 1001

        # When we parse a file with a default version, no warning is given
        Version(a=1001)
        assert "The version of the input file is unsupported" not in caplog.text

        # But when we parse a version other than we support, we give a warning.
        Version(a=1000)
        assert "The version of the input file is unsupported" in caplog.text
