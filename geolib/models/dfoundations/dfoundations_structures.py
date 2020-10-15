from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from geolib.models.dseries_parser import (
    DSerieListGroupNextStructure,
    DSerieParser,
    DSeriesInlineProperties,
    DSeriesStructure,
    get_line_property_key_value,
    get_line_property_value,
)


class DFoundationsEnumStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text):
        parsed_structure = DSerieParser.parse_group_as_dict(text)
        kwargs = cls.remove_enum_explanation(parsed_structure)
        return cls(**kwargs)

    @staticmethod
    def remove_enum_explanation(structure: Dict[str, Any]) -> Dict[str, Any]:
        """Remove trailing explanations from values of `structure`
        0 : Mechanical qc required -> 0
        """
        updated_structure = {}
        for key, value in structure.items():
            if isinstance(value, str) and ":" in value:
                value = get_line_property_value(value, reversed_key=True)
            updated_structure[key] = value
        return updated_structure


class DFoundationsInlineProperties(DSeriesInlineProperties):
    @classmethod
    def get_property_key_value(cls, text: str, expected_property: str) -> Tuple[str, str]:
        """Returns the value content for a line of format:
        value : key || value = key

        Args:
            text (str): Text line with value-key

        Returns:
            str: Filtered value.
        """
        if text:
            # If the value is not empty, extract its value (assume it's on the first position)
            _, value = get_line_property_key_value(text, reversed_key=True)
            return expected_property, value
        return expected_property, text


class DFoundationsTableWrapper(DSeriesStructure):
    @classmethod
    def parse_text(cls, text):
        """Parses a Table wrapped in another group such as:
        [TABLE GROUP]
        [COLUMN INDICATION]
        A
        B
        [END OF COLUMN INDICATION]
        [GROUP DATA]
        1 1
        2 2
        [END OF GROUP DATA]
        [END OF TABLE GROUP]

        Args:
            text (str): Wrapped table group to parse.

        Returns:
            DSerieStructure: Parsed structure.
        """

        def split_line(text: str) -> List[str]:
            parts = re.split(" |\t", text.strip())
            return list(filter(lambda part: part != "", parts))

        table_text = list(DSerieParser.parse_list_group(text).values())[0]
        table_data = list(DSerieParser.parse_list_group(table_text).values())
        # Expected two groups (column_indication and data)
        keys = table_data[0].split("\n")
        values_dict_list = [
            dict(zip(keys, values))
            for values in map(split_line, table_data[1].split("\n"))
        ]
        collection_property_name = list(cls.__fields__.items())[0][0]
        return cls(**{collection_property_name: values_dict_list})


class DFoundationsCPTCollectionWrapper(DSerieListGroupNextStructure):
    @classmethod
    def group_delimiter(cls) -> str:
        return "[NEXT OF NUMBER OF CPTS]"
