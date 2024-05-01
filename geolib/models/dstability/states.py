"""
This module handles the three types of state types in DStability.
"""

import abc
from typing import List, Tuple

from geolib._compat import IS_PYDANTIC_V2
from geolib.models import BaseDataClass

from ...geometry.one import Point
from ...utils import snake_to_camel
from .internal import (
    InternalStateTypeEnum,
    PersistablePoint,
    PersistableStateLinePoint,
    PersistableStatePoint,
    PersistableStochasticParameter,
    PersistableStress,
)


class DStabilityObject(BaseDataClass, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def _to_internal_datastructure(self):
        raise NotImplementedError


class DStabilityStress(DStabilityObject):
    """DStability Stress

    Args:
        ocr (float): OCR value, defaults to 1.0
        pop (float): POP value, defaults to 0.0
        stochastic_parameter (PersistableStochasticParameter)
        state_type (InternalStateTypeEnum): type of state
    """

    ocr: float = 1.0
    pop: float = 0.0
    stochastic_parameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    state_type: InternalStateTypeEnum = InternalStateTypeEnum.POP

    def _to_internal_datastructure(self) -> PersistableStress:
        if IS_PYDANTIC_V2:
            data = {
                **{
                    snake_to_camel(name): value
                    for name, value in self.model_dump().items()
                }
            }
        else:
            data = {
                **{snake_to_camel(name): value for name, value in self.dict().items()}
            }
        data["PopStochasticParameter"] = data.pop("StochasticParameter")
        return PersistableStress(**data)


class DStabilityStatePoint(DStabilityObject):
    """DStability StatePoint

    Args:
        id (int): id of the statepoint
        layer_id (int): id of the layer to add the statepoint, note that the API does not check if this point is within the layer
        pop (float): POP value, defaults to 0.0
        point (Point): location of the statepoint
        stress (DStabilityStress): DStabilityStress object
        is_probabilistic (bool): is probabilistic, default to false
        label (str): label of the statepoint

    """

    id: int = -1  # this will be filled in by the datamodel, not meant for the user
    layer_id: int
    point: Point
    stress: DStabilityStress
    is_probabilistic: bool = False
    label: str = ""

    def _to_internal_datastructure(self) -> PersistableStatePoint:
        if IS_PYDANTIC_V2:
            model_dump = self.model_dump()
        else:
            model_dump = self.dict()
        data = {
            **{
                snake_to_camel(name): value
                for name, value in model_dump.items()
                if name not in {"point", "stress"}
            },
            "Point": PersistablePoint(X=self.point.x, Z=self.point.z),
            "Stress": self.stress._to_internal_datastructure(),
        }
        return PersistableStatePoint(**data)


class DStabilityStateLinePoint(DStabilityObject):
    """"""

    id: int = -1
    above: DStabilityStress
    below: DStabilityStress
    is_above_and_below_correlated: bool = False
    is_probabilistic: bool = False
    label: str = ""
    x: float

    def _to_internal_datastructure(self) -> PersistableStateLinePoint:
        if IS_PYDANTIC_V2:
            model_dump = self.model_dump()
        else:
            model_dump = self.dict()
        data = {
            **{
                snake_to_camel(name): value
                for name, value in model_dump.items()
                if name not in {"above", "below"}
            },
            "Above": self.above._to_internal_datastructure(),
            "Below": self.below._to_internal_datastructure(),
        }
        return PersistableStateLinePoint(**data)
