import logging

from geolib.models.validators import BaseValidator

logger = logging.getLogger(__name__)


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
                if "profile" in key and not isinstance(value, str):
                    if value not in self.ds.soil_profiles.soil_profile_names:
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
            error = f"Number of stages defined is {len(self.ds.construction_stages.stages)} which is not the same as {len(self.ds.calculation_options_per_stage.stageoptions)}"
            logger.warning(error)
            raise ValueError(error)

        return True

    def is_valid_soil_profiles(self) -> bool:
        """All soils in soil profiles should be defined in the soil collection"""
        if isinstance(self.ds.soil_profiles, str):
            return True  # Resultings from parsing input file.
        soil_names = self.ds.soil_collection.soil_names
        referenced_soil_names = self.ds.soil_profiles.referenced_soil_names
        if not referenced_soil_names.issubset(soil_names):
            raise ValueError(
                f"The following soils were not found in soil collection: {', '.join(referenced_soil_names - soil_names)}"
            )
        return True
