import logging
from typing import Set

from geolib.models.validators import BaseValidator

logger = logging.getLogger(__name__)


class DStabilityValidator(BaseValidator):
    """Validator for DStability structure.

    Has access to self.ds from parent class.
    Will run all is_valid_ functions to check for validity."""

    def is_valid_stages(self) -> bool:
        """Number of stages should be the same:"""
        lengths_set = set()
        valid = True
        for key, value in (
            (k, v) for k, v in self.ds.dict().items() if "result" not in k
        ):  # Results not required for stage validity.
            if isinstance(value, list):
                lengths_set.add(len(value))
                if len(lengths_set) > 1:
                    logger.error(
                        f"{self.is_valid_stages.__doc__} {key} has different number of stages: {len(value)}."
                    )
                    valid = False
                    break

        return valid

    def is_valid_layer_loads(self) -> bool:
        """Each layer load must have a consolidation degree for each soil layer"""
        for stage_id, _ in enumerate(self.ds.stages):
            soil_layer_ids: Set[str] = {
                layer.LayerId for layer in self.ds.soillayers[stage_id].SoilLayers
            }

            layer_load_layer_ids: Set[str] = set()
            for layer_load in self.ds.loads[stage_id].LayerLoads:
                layer_load_layer_ids.add(layer_load.LayerId)

                consolidation_layer_id_references: Set[str] = set()
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
