from geolib.models import BaseValidator
import logging
from typing import Set


class DSheetPilingValidator(BaseValidator):
    """Validator for DSheetpiling internal structure.

    Raises:
        ValueError: When the internal datastructure is not valid including a message why.

    Has access to self.ds from parent class.
    Will run all is_valid_ functions to check for validity.
    """

    def is_valid_stages(self) -> bool:
        """
        When adding stages, some values are populated with None.
        These should be replaced before serializing.
        """
        for i, stage in enumerate(self.ds.construction_stages.stages):
            for key, value in dict(stage).items():
                if value is None:
                    raise ValueError(
                        f"All attributes must be populated; stage {i}-{stage.name} has None value for {key}"
                    )
                if "water_level" in key and not isinstance(value, str):
                    if value not in self.ds.waterlevels.water_level_names:
                        raise ValueError(
                            f"{key}-{value} in stage {i}-{stage.name} is not defined in internal data structure"
                        )
                    continue
                if "surface" in key and not isinstance(value, str):
                    if value not in self.ds.surfaces.surface_names:
                        raise ValueError(
                            f"{key}-{value} in stage {i}-{stage.name} is not defined in internal data structure"
                        )
                    continue
                if key == "anchors":
                    for anchor in value:
                        if anchor["name"] not in self.ds.anchors.anchor_names:
                            raise ValueError(
                                f"{key}-{value} in stage {i}-{stage.name} is not defined in internal data structure"
                            )
                    continue
                if key == "struts":
                    for strut in value:
                        if strut["name"] not in self.ds.struts.strut_names:
                            raise ValueError(
                                f"{key}-{value} in stage {i}-{stage.name} is not defined in internal data structure"
                            )
                    continue
        if len(self.ds.construction_stages.stages) != len(
            self.ds.calculation_options_per_stage.stageoptions
        ):
            raise ValueError(
                f"Number of stages defined is {len(self.ds.construction_stages.stages)} which is not the same as {len(self.ds.calculation_options_per_stage.stageoptions)}"
            )

        return True
