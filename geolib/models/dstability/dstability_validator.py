import logging

from geolib.models.validators import BaseValidator

logger = logging.getLogger(__name__)


class DStabilityValidator(BaseValidator):
    """Validator for DStability structure.

    Has access to self.ds from parent class.
    Will run all is_valid_ functions to check for validity."""

    def is_valid_stages(self) -> bool:
        """Number of stages should be the same:"""

        stage_count = 0
        for scenario in self.ds.scenarios:
            for _ in scenario.Stages:
                stage_count += 1

        lengths_set = set()
        valid = True
        model_dump = self.ds.model_dump()
        for key, value in (
            (k, v)
            for k, v in model_dump.items()
            if "result" not in k
            and "scenarios" not in k
            and "calculationsettings" not in k
        ):  # Results not required for stage validity.
            if isinstance(value, list):
                lengths_set.add(len(value))
                if len(value) > stage_count:
                    logger.error(
                        f"{self.is_valid_stages.__doc__} {key} has different number of stages: {len(value)}."
                    )
                    valid = False
                    break

        return valid

    def is_valid_layer_loads(self) -> bool:
        """Each layer load must have a consolidation degree for each soil layer"""
        for scenario_index, _ in enumerate(self.ds.scenarios):
            for stage_index, _ in enumerate(self.ds.scenarios[scenario_index].Stages):
                soil_layer_ids: set[str] = {
                    layer.LayerId
                    for layer in self.ds._get_soil_layers(
                        scenario_index, stage_index
                    ).SoilLayers
                }

                if len(soil_layer_ids) == 0:
                    return True

                layer_load_layer_ids: set[str] = set()
                for layer_load in self.ds._get_loads(
                    scenario_index, stage_index
                ).LayerLoads:
                    layer_load_layer_ids.add(layer_load.LayerId)

                    consolidation_layer_id_references: set[str] = set()
                    for consolidation in layer_load.Consolidations:
                        consolidation_layer_id_references.add(consolidation.LayerId)
                        if consolidation.LayerId is None:
                            return False
                    if soil_layer_ids - consolidation_layer_id_references != set(
                        [layer_load.LayerId]
                    ):  # All other soillayer ids are included except the soillayers own id.
                        return False
                if layer_load_layer_ids != soil_layer_ids:
                    return False
        return True
