from __future__ import annotations

import logging
from typing import Any, Dict, List, Tuple

from geolib.models.dseries_parser import (
    DSerieListGroupNextStructure,
    DSerieParser,
    DSeriesInlineProperties,
    DSeriesRepeatedGroupedProperties,
    DSeriesStructure,
    get_line_property_key_value,
    get_line_property_value,
    make_key,
    split_line_elements,
    strip_line_first_element,
)

logger = logging.getLogger(__name__)


class ComplexVerticalSubstructure(DSeriesStructure):
    """Specific Vertical substructure with a dedicated
    parser because of the oddities stored in that group."""

    def __init__(self, *args, **kwargs):
        """Replace unnamed arguments by fieldnames in order.

        Some structure in DSerie files have no names attached
        and are just values. This provides a way to still parse
        them.
        """
        largs = list(args)
        for field, fieldtype in self.__fields__.items():
            if len(largs) == 0:
                break
            if field in kwargs:
                continue
            else:
                value = strip_line_first_element(largs.pop(0))
                logger.debug(f"Setting {field}: {fieldtype} to {value}")
                kwargs[field] = value

        if len(largs) > 0:
            raise Exception(f"Failed to convert args to kwargs: {largs} left unmapped.")

        super().__init__(*args, **kwargs)

    @classmethod
    def parse_text(cls, text: str):
        """Parser that:

        - Knows about structure with fields and subgroups
        - Knows about repeated Vertical fields without a specific collection
        - Knows about the bug of time-dependent data groups that end without the - included
        - Knows about the bug of absence of the second end-tag of time-dependent data

        Arguments:
            data {str} -- Data to parse.
        """
        EXCEPTIONS = ["soil", "vertical", "time__dependent_data"]
        parsed_dict = {}
        currentkey = ""
        data = []
        args = []
        text_lines = list(filter(None, text.split("\n")))
        for i, line in enumerate(text_lines):
            sline = line.strip()
            # keyline
            if sline.startswith("[") and sline.endswith("]"):
                # [ key name ] => key_name
                key = make_key(sline[1:-1])

                # new group
                if currentkey == "":
                    logger.debug(f"Found new {key}")
                    currentkey = key
                    if len(data) > 0:
                        args.extend(data)
                    data = []

                # duplicate group before end
                elif currentkey == key:

                    # If key already exists, this is a group -> List
                    if currentkey in parsed_dict:
                        parsed_dict[currentkey] = parsed_dict[currentkey] + [
                            "".join(data)
                        ]
                    elif currentkey in EXCEPTIONS:
                        parsed_dict[currentkey] = ["".join(data)]
                    else:
                        parsed_dict[currentkey] = "".join(data)

                    data = []

                    logger.debug(
                        f"Duplicate key {key} at line {i} without first encountered and END OF."
                    )

                # end of current group
                elif key == "end_of_" + currentkey:
                    logger.debug(f"Found {key}")
                    # If key already exists, this is a group -> List
                    if currentkey in parsed_dict:
                        parsed_dict[currentkey] = parsed_dict[currentkey] + [
                            "".join(data)
                        ]
                    elif currentkey in EXCEPTIONS:
                        parsed_dict[currentkey] = ["".join(data)]
                    else:
                        parsed_dict[currentkey] = "".join(data)
                    data = ""
                    currentkey = ""

                # sub group that is eaten for now
                else:
                    data.append(line + "\n")

            # dataline
            else:
                data.append(line + "\n")

        # Because no [end] exist for duplicate group...
        parsed_dict[currentkey] = parsed_dict[currentkey] + ["".join(data)]

        return cls(*args, **parsed_dict)


class DSerieRepeatedTableStructure(DSeriesRepeatedGroupedProperties):
    @classmethod
    def group_value_is_list(cls, group_key: str) -> bool:
        """Override of parent method. Only the columns are not a list.

        Args:
            group_key (str): Property name.

        Returns:
            bool: Whether the key represents a list of values or not.
        """
        return group_key != "column_indication"

    @classmethod
    def get_validated_mappings(cls, generated_dict: Dict[str, str]) -> Dict[str, str]:
        """Transforms the generated dict from the parent into our own mapping.

        Args:
            generated_dict (Dict[str, str]): Parsed dictionary from parent.

        Returns:
            Dict[str, str]: Mapped dictionary with concrete properties.
        """
        class_name = cls.__name__.lower()
        n_groups = len(generated_dict.items())
        if n_groups != 2:
            raise ValueError(f"Expected 2 groups for {class_name} but got {n_groups}.")
        columns = [
            make_key(line)
            for line in generated_dict.pop("column_indication").split("\n")
            if line != ""
        ]
        parsed_dict: Dict[str, str] = {}
        # We assume there is only one 'repeated' key, so we get the values from it.
        for group_data in list(generated_dict.values())[0]:
            mapped_group = cls.get_mapped_group(columns, group_data)
            group_key = list(mapped_group.keys())[0]
            if group_key in parsed_dict.keys():
                raise ValueError(
                    f"No repeated table keys ({group_key}) allowed for {class_name}."
                )
            parsed_dict.update(mapped_group)

        return {cls.__name__.lower(): parsed_dict}

    @staticmethod
    def get_mapped_group(
        column_list: List[str], group_line: str
    ) -> Dict[str, List[Dict[str, str]]]:
        """Based on the input column and the group line, generates a list of
        dictionary entries which are mapped to the first element of the group
        line.

        Args:
            column_list (List[str]): List of columns to map.
            group_line (str): Content containing id of dictionary and list values.

        Returns:
            Dict[str, List[Dict[str, str]]]: Generated mapped group.
        """
        lines = [
            split_line_elements(line) for line in group_line.split("\n") if line != ""
        ]
        entry_id = lines.pop(0)[0]
        return {entry_id: [dict(zip(column_list, parts)) for parts in lines]}
