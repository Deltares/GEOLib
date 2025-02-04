from __future__ import annotations

import re
from typing import Any

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
    def remove_enum_explanation(structure: dict[str, Any]) -> dict[str, Any]:
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
    def get_property_key_value(cls, text: str, expected_property: str) -> tuple[str, str]:
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
        [TABLE]
        DataCount = x followed by
        [END OF TABLE]  directly when x = 0 or, when x > 0, by
        [COLUMN INDICATION]
        A
        B
        [END OF COLUMN INDICATION]
        [DATA]
        1 1
        2 2
        [END OF DATA]
        [END OF TABLE]

        Args:
            text (str): Wrapped table group to parse.

        Returns:
            DSerieStructure: Parsed structure.
        """

        def split_line(text: str) -> list[str]:
            parts = []
            for part in re.split(" |\t", text.strip()):
                if part == "":
                    continue
                if part.isdigit():
                    parts.append(int(part))
                else:
                    try:
                        parts.append(float(part))
                    except ValueError:
                        parts.append(part)
            return parts

        table_text = list(DSerieParser.parse_list_group(text).values())[0]
        table_data = list(DSerieParser.parse_list_group(table_text).values())
        if len(table_data) == 0:
            values_dict_list = table_data
            collection_property_name = list(cls.model_fields.items())[0][0]
            return cls(**{collection_property_name: values_dict_list})
        else:
            # Expected two groups (column_indication and data)
            keys = table_data[0].split("\n")
            values_dict_list = [
                dict(zip(keys, values))
                for values in map(split_line, table_data[1].split("\n"))
            ]
            collection_property_name = list(cls.model_fields.items())[0][0]

        return cls(**{collection_property_name: values_dict_list})


class DFoundationsCPTCollectionWrapper(DSerieListGroupNextStructure):
    @classmethod
    def group_delimiter(cls) -> str:
        return "[NEXT OF NUMBER OF CPTS]"
