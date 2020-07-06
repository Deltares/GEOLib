import logging
from typing import Tuple, List, Dict
from geolib.models.dseries_parser import (
    DSeriesStructure,
    DSeriesUnmappedNameProperties,
    DSeriesRepeatedGroupsWithInlineMappedProperties,
    DSerieParser,
    get_line_property_value,
)


class DSeriesPilingDumpParserStructure(DSeriesStructure):
    @classmethod
    def parse_text(cls, text: str):
        if "[ECHO OF MSHEET INPUT]" in text:
            logging.warning("Replacing headers to create [DUMPFILE]")
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
            logging.warning("Putting [INPUT DATA]")
            text = text.replace("[SOIL COLLECTION]", "[INPUT DATA]\n[SOIL COLLECTION]")
        if "[END OF INPUT FILE]" in text:
            text = text.replace("[END OF INPUT FILE]", "[END OF INPUT DATA]")
        if "[End of Input Data]" in text:
            logging.warning("Putting [OUTPUT DATA]")
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
