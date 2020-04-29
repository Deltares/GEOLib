import os
from typing import List, get_type_hints, _GenericAlias, Type, Tuple, Dict
import pytest

from geolib.models.base_model import BaseModel
from geolib.models.dseries_parser import (
    DSeriesTabbedTreeStructureCollection,
    DSeriesTabbedTreeStructure,
)


class TestDSeriesTabbedTreeStructureCollection:
    class DummyTabbedTreeStructure(DSeriesTabbedTreeStructure):

        struct_id: str
        single_property: List[int]

        @staticmethod
        def list_of_properties() -> List[str]:
            return ["struct_id", "single_property"]

    class DummyTabbedTreeStructureCollection(DSeriesTabbedTreeStructureCollection):

        tabbedtreestructures: List[DSeriesTabbedTreeStructure]

        @staticmethod
        def TabbedTreeStructure() -> Tuple[str, Type[DSeriesTabbedTreeStructure]]:
            return (
                "tabbedtreestructures",
                TestDSeriesTabbedTreeStructureCollection.DummyTabbedTreeStructure,
            )

    @pytest.mark.integrationtest
    def test_given_tabbedtreetext_when_parse_then_returns_object(self):
        # 1. Set up test model.
        structure_name = "my_structure"
        structure_content = {
            "1": [1, 2],
            "2": [3, 4],
            "3": [5, 6],
            "4": [7, 8],
        }
        content_lines = f"{len(structure_content)} - Number of {structure_name}\n"
        for s_key, s_value in structure_content.items():
            id_line = f"\t{s_key} - dumb text"
            n_prop_line = f"\t\t{len(s_value)} - dumb text too"
            prop_values_line = ""
            for value in s_value:
                prop_values_line += f"{value}\t"
            prop_values_line = f"\t\t\t{prop_values_line}"
            content_lines += f"{id_line}\n{n_prop_line}\n{prop_values_line}\n"

        # 2. Run test.
        parsed_collection = self.DummyTabbedTreeStructureCollection.parse_text(
            content_lines
        )

        # 3. Verify final expectations.
        assert parsed_collection, "No structure was generated."
        assert isinstance(parsed_collection, DSeriesTabbedTreeStructureCollection)
        parsed_dict_collection = dict(parsed_collection)
        assert len(parsed_dict_collection["tabbedtreestructures"]) == len(
            structure_content
        )
        for parsed_structure in parsed_dict_collection["tabbedtreestructures"]:
            parsed_as_dict = dict(parsed_structure)
            structure_id = parsed_as_dict["struct_id"]
            assert structure_content[structure_id] == parsed_as_dict["single_property"], (
                "" + f"Structure {structure_id} has not been parsed correctly."
            )


class TestDSeriesTabbedTreeStructure:
    class DummyTabbedTreeStructure(DSeriesTabbedTreeStructure):
        name: str
        firstproperty: List[int]
        randomproperty: List[int]
        lastproperty: List[int]

    @pytest.mark.unittest
    def test_given_no_concrete_class_when_get_list_of_properties_then_doesnotraise(self):
        # 1. Define and run expectation:
        return_result = None

        # 2. Run test
        return_result = DSeriesTabbedTreeStructure.list_of_properties()

        # 3. Verify final expectations
        assert isinstance(return_result, list), "Result should be an empty list."
        assert not return_result, "Result should be an empty list."

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "separator",
        [
            pytest.param(" ", id="Space separator."),
            pytest.param("\t", id="Tabulate separator.")])
    def test_given_tabbedstring_parse_text_returns_dseriesstruct_with_dict(self, separator):
        # 1. Set up test data
        parsed_structure = None
        structure_name = "my_structure"
        structure_content = {
            "name": structure_name,
            "firstproperty": [1, 2],
            "randomproperty": [3, 4],
            "lastproperty": [5, 6],
        }
        content_lines = f"{structure_name} - Id for {structure_name}\n"
        for s_key, s_value in list(structure_content.items())[1:]:
            property_line = f"{separator}{len(s_value)} - number of {s_key}"
            prop_values_line = ""
            for value in s_value:
                prop_values_line += f"{value}{separator}"
            prop_values_line = f"{separator * 2}{prop_values_line}"
            content_lines += f"{property_line}\n{prop_values_line}\n"

        # 2. Verify initial expectations
        assert self.DummyTabbedTreeStructure.list_of_properties() == list(
            structure_content.keys()
        )
        # 3. Run test
        parsed_structure = self.DummyTabbedTreeStructure.parse_text(content_lines)

        # 4. Verify final expectations
        assert parsed_structure is not None
        assert isinstance(parsed_structure, DSeriesTabbedTreeStructure)
        parsed_dict = dict(parsed_structure)
        for entry in structure_content:
            assert parsed_dict[entry] == structure_content[entry], (
                "" + f"Field {entry} has not been parsed correctly."
            )
