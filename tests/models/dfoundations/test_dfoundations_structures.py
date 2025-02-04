from contextlib import nullcontext as does_not_raise
from random import choice, randint
from string import ascii_lowercase

import pytest
from pydantic_core._pydantic_core import ValidationError

from geolib.models.dfoundations.dfoundations_structures import (
    DFoundationsCPTCollectionWrapper,
    DFoundationsEnumStructure,
    DFoundationsTableWrapper,
)


class TestDFoundationsEnumStructure:
    @pytest.mark.unittest
    def test_remove_enum_explanation(self):
        structure = {"foo": "1 : bar", "ffo": "2", "fff": 1}

        out = DFoundationsEnumStructure.remove_enum_explanation(structure)

        assert "foo" in out
        assert out["foo"] == "1"
        assert out["ffo"] == "2"
        assert out["fff"] == 1


class TestDFoundationsCPTCollectionWrapper:
    @pytest.mark.integrationtest
    def test_given_DFoundationsCPTCollectionWrapper_text_when_parse_then_returns_structure(
        self,
    ):
        class test_simple_element(DFoundationsEnumStructure):
            first_value: int

        class test_wrapped_collection(DFoundationsCPTCollectionWrapper):
            collection: list[test_simple_element]

        # 1. Define test data.
        structure_first_value_list = [42, 24]
        text_to_parse = (
            "" + "[NUMBER OF STRUCTURES]\n" + "2\n" + "----------------------------\n"
        )
        for i, structure_first_value in enumerate(structure_first_value_list):
            text_to_parse += (
                ""
                + "[FIRST_VALUE]\n"
                + f"{structure_first_value}\n"
                + "[END OF FIRST_VALUE]\n"
            )
            if i != len(structure_first_value_list) - 1:
                text_to_parse += "[NEXT OF NUMBER OF CPTS]\n"
        text_to_parse += "[END OF NUMBER OF STRUCTURES]"

        # 2. Run test.
        parsed_structure = test_wrapped_collection.parse_text(text_to_parse)

        # 3. Validate final expectations.
        assert parsed_structure
        assert len(parsed_structure.collection) == 2
        for struct_pos, structure in enumerate(parsed_structure.collection):
            assert isinstance(structure, test_simple_element)
            assert structure.first_value == structure_first_value_list[struct_pos]


class TestDFoundationsTableWrapper:
    class test_simple_table(DFoundationsTableWrapper):
        value: list[dict[str, int | float | str]]

    class test_table_str_first(DFoundationsTableWrapper):
        value: list[dict[str, str | int | float]]

    class test_table_float_first(DFoundationsTableWrapper):
        value: list[dict[str, float | int | str]]

    class test_table_only_int(DFoundationsTableWrapper):
        value: list[dict[str, int]]

    class test_table_only_float(DFoundationsTableWrapper):
        value: list[dict[str, float]]

    class test_table_only_str(DFoundationsTableWrapper):
        value: list[dict[str, str]]

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "table_type, expected_column_type, run_expectation",
        [
            pytest.param(
                test_simple_table, [int, float, str], does_not_raise(), id="Int-Float-Str"
            ),
            pytest.param(
                test_table_str_first,
                [int, float, str],
                does_not_raise(),
                id="Str-Int-Float",
            ),
            pytest.param(
                test_table_float_first,
                [int, float, str],
                does_not_raise(),
                id="Float-Int-Str",
            ),
            pytest.param(
                test_table_only_int, [], pytest.raises(ValidationError), id="Int"
            ),
            pytest.param(
                test_table_only_float, [], pytest.raises(ValidationError), id="Float"
            ),
            # pytest.param(
            #     test_table_only_str, [str, str, str], does_not_raise(), id="Str"
            # ),
        ],
    )
    def test_given_dfoundationstablewrapper_when_parse_type_done_in_order(
        self, table_type: type, expected_column_type: list[type], run_expectation
    ):
        # 1. Define test data
        input_dict = {"int": 42, "float": 4.2, "str": "'42'"}
        text_to_parse = (
            ""
            + "[TABLE]\n"
            + "[COLUMN INDICATION]\n"
            + "{}\n".format("\n".join(input_dict.keys()))
            + "[END OF COLUMN INDICATION]\n"
            + "[DATA]\n"
            + "{}\n".format(" ".join([str(value) for value in input_dict.values()]))
            + "[END OF DATA]\n[END OF TABLE]"
        )
        parsed_table = None

        # 2. Run test
        with run_expectation:
            parsed_table = table_type.parse_text(text_to_parse)

        # 3. Verify final result
        if not expected_column_type:
            # The test was expected to raise an exception, so don't go further:
            return
        assert len(parsed_table.value) == 1
        parsed_dict = parsed_table.value[0]
        assert type(parsed_dict["int"]) == expected_column_type[0]
        assert type(parsed_dict["float"]) == expected_column_type[1]
        assert type(parsed_dict["str"]) == expected_column_type[2]

    @pytest.mark.integrationtest
    def test_given_dfoundationstablewrapper_with_multiple_types_when_parse_then_return_structure(
        self,
    ):
        # 1. Define test data.
        keys = ["yo", "lo", "man"]
        measured_values = [
            {
                keys[0]: randint(0, 100),
                keys[1]: float(randint(0, 100)),
                keys[2]: "".join(choice(ascii_lowercase) for _ in range(4)),
            }
            for idx in range(1, 4)
        ]
        text_to_parse = (
            ""
            + "[TABLE]\n"
            + "[COLUMN INDICATION]\n"
            + "{}\n".format("\n".join(keys))
            + "[END OF COLUMN INDICATION]\n"
            + "[DATA]\n"
        )
        for data_values in measured_values:
            values = " ".join([str(value) for value in data_values.values()])
            text_to_parse += "" + f"{values}\n"
        text_to_parse += "[END OF DATA]\n[END OF TABLE]\n"
        # 2. Run test.
        parsed_table = self.test_simple_table.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_table
        assert parsed_table.value == measured_values
        # Verify types for all entries
        for value in parsed_table.value:
            assert isinstance(value["yo"], int)
            assert isinstance(value["lo"], float)
            assert isinstance(value["man"], str)
