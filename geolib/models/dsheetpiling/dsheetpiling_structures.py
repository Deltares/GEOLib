import logging
import re
from typing import Any, Dict, List, Tuple, get_type_hints

from geolib.errors import ParserError
from geolib.models.dseries_parser import (
    DSerieListStructure,
    DSerieParser,
    DSeriesInlineProperties,
    DSeriesRepeatedGroupsWithInlineMappedProperties,
    DSeriesStructure,
    DSeriesUnmappedNameProperties,
    DSeriesWrappedTableStructure,
    get_line_property_value,
)

logger = logging.getLogger(__name__)


class DSeriesPilingDumpParserStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        if "[ECHO OF MSHEET INPUT]" in text:
            logger.warning("Replacing headers to create [DUMPFILE]")
            text = text.replace("[ECHO OF MSHEET INPUT]", "[DUMPFILE]").replace(
                "[END OF DUMP]", "[END OF OUTPUT DATA]\n[END OF DUMPFILE]"
            )
        if "[END OF DUMPFILE]" not in text:
            text += "\n[END OF OUTPUT DATA]\n[END OF DUMPFILE]\n"
        return super().parse_text(text)


class DSeriesPilingParserStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        if "[INPUT DATA]" not in text:
            logger.warning("Putting [INPUT DATA]")
            text = text.replace("[SOIL COLLECTION]", "[INPUT DATA]\n[SOIL COLLECTION]")
        if "[END OF INPUT FILE]" in text:
            text = text.replace("[END OF INPUT FILE]", "[END OF INPUT DATA]")
        if "[End of Input Data]" in text:
            logger.warning("Putting [OUTPUT DATA]")
            text = text.replace(
                "[End of Input Data]", "[End of Input Data]\n[OUTPUT DATA]"
            )

        return super().parse_text(text)


class DSheetpilingSurchargeLoad(DSeriesRepeatedGroupsWithInlineMappedProperties):
    @classmethod
    def get_list_field_names(cls) -> List[str]:
        super_field_names = super().get_list_field_names()
        super_field_names.append("point")
        return super_field_names

    @classmethod
    def get_validated_mappings(cls, generated_dict: Dict[str, str]) -> Dict[str, str]:
        name_field = generated_dict.pop("", "")
        # Verify the name field has not been replaced by "surcharge_load"
        if "surcharge_load" in generated_dict:
            name_field = generated_dict.pop("surcharge_load")
        generated_dict["name"] = name_field
        generated_dict["points"] = generated_dict.pop("point", [])
        return generated_dict


class DSheetpilingWithNumberOfRowsTable(DSeriesWrappedTableStructure):
    @classmethod
    def parse_text(cls, text):
        """These sort of tables contain the number of lines in the first row
        the rest of its structure is similar to DSeriesWrappedTableStructure.

        Args:
            text (str): Full contains containing table structure and values.

        Returns:
            DSeriesStructure: Fully parsed structure.
        """
        splitted_text = text.split("\n")
        # Skip validating for now.
        splitted_text.pop(0)
        return super().parse_text("\n".join(splitted_text))


class DSheetpilingUnwrappedTable(DSeriesStructure):
    @classmethod
    def parse_text(cls, text):
        lines = text.split("\n")
        nrow = int(lines.pop(0).split()[0])
        # Remove the line with the column names.
        lines.pop(0)
        # Count the rest of the lines.
        if not nrow == len(lines):
            raise ParserError(
                f"Error parsing for {cls}, header indicates {nrow} lines, while there are {len(lines)} lines."
            )

        return cls(**{cls.__name__.lower(): lines})


class DSheetpilingTableEntry(DSeriesStructure):
    """Parses a table entry where the latest column is actually a name (which can be composed by a few strings.)
    E.g.:
        Nr        Level        E-mod     Cross sect.    Length     YieldF   Side
        1 -10.00  2.100E+0008  1.000E-0004  10.00 500.00 -30  0.00 2 Strut
    """

    @classmethod
    def parse_text(cls, text):
        values = [value for value in text.split() if value]
        # Remove the first value (it's just the line number)
        values.pop(0)

        # In later versions __slots__ is a type hint too, function below is to ignore this key
        type_hints = get_type_hints(cls)
        if "__slots__" in type_hints:
            type_hints.pop("__slots__")

        number_of_fields = len(type_hints)
        name_field = " ".join(
            name_value for name_value in values[number_of_fields - 1 :] if name_value
        )
        rest_fields = values[0 : number_of_fields - 1]
        rest_fields.insert(0, name_field)

        return cls(**dict(zip(type_hints.keys(), rest_fields)))
