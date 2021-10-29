from typing import Any, Dict, List, Optional

from geolib.geometry.one import Point
from geolib.models import BaseDataClass
from geolib.models.internal import Bool

from .internal import CPT as InternalCPT
from .internal import ExcavationType, InterpretationType, Layer
from .internal import Profile as InternalProfile
from .internal import ReductionCoreResistanceEnum, TimeOrderType


class CPT(BaseDataClass):
    """TODO To be expanded/generalized in GEOLib+

    measure_data need to be provided as a list of dicts::

        [{
            "z": float,  # negative
            "qc": float,
        }]

    Note that `timeorder_type` will force all other
    CPTs in the same model to the same `timeorder_type`.
    """

    cptname: str
    groundlevel: float
    depthrange: float = 0.10  # minimum layer thickness
    measured_data: List[Dict[str, float]]

    excavation_type: ExcavationType = ExcavationType.BEFORE
    timeorder_type: TimeOrderType = TimeOrderType.CPT_EXCAVATION_INSTALL

    interpretation_model: InterpretationType = InterpretationType.NEN_RULE
    interpretation_model_stressdependent: Bool = Bool.FALSE

    # GEF related values
    pre_excavation: float = 987654321.000
    void_value_depth: float = 987654321.000
    void_value_cone_resistance: float = 987654321.000
    void_value_pore_water_pressure: float = 987654321.000
    void_value_sleeve_friction: float = 987654321.000
    void_value_friction_number: float = 987654321.000
    void_value_equivalent_electronic_qc: float = 987000000.000000

    def to_profile(self, method, **kwargs) -> "Profile":
        """TODO GEOLib+ Interpret CPT by `method` to generate a Profile."""
        pass

    def _to_internal(self) -> InternalCPT:
        kwargs = self.dict()
        kwargs["measured_data"] = {"data": kwargs["measured_data"]}
        return InternalCPT(**kwargs)


class Excavation(BaseDataClass):
    """Excavation class.

    Note that using an excavation level will
    override all previous set excavation levels in the same model."""

    reduction_of_core_resistance: ReductionCoreResistanceEnum = (
        ReductionCoreResistanceEnum.SAFE
    )
    excavation_level: float
    excavation_width_infinite: Bool = Bool.TRUE
    excavation_length_infinite: Bool = Bool.TRUE
    distance_edge_pile_to_excavation_boundary: float = 0.0  # only valid for BEGEMANN


class Profile(BaseDataClass):
    """Generic profile class.

    Layers need to be provided as a list of dicts::

        [{
            "name": str,
            "material": str,
            "top_level": float  # [m]
            "excess_pore_pressure_top": float = 0.0  # [kN/m3]
            "excess_pore_pressure_bottom": float = 0.0  # [kN/m3]
            "ocr_value": float = 1.0  # [-]
            "reduction_core_resistance": int = 0  # [%]
        },]

    """

    name: str
    location: Point
    phreatic_level: float
    pile_tip_level: float
    cpt: CPT
    excavation: Optional[Excavation] = None
    overconsolidation_ratio: float = 1.0
    top_of_positive_skin_friction: float = 0.0
    bottom_of_negative_skin_friction: float = 0.0
    expected_ground_level_settlement: float = 0.0
    placement_depth_of_foundation: float = 0.0
    concentration_value_frohlich: int = 3
    top_tension_zone: float = 0.0
    # Any, as combined int, float will become int
    layers: List[Dict[str, Any]]

    def _to_internal(self, matching_cpt) -> InternalProfile:
        kwargs = self.dict(exclude={"cpt", "excavation", "location"})

        kwargs["matching_cpt"] = matching_cpt

        if self.excavation is not None:
            kwargs.update(self.excavation.dict())

        kwargs["x_coordinate"] = self.location.x
        kwargs["y_coordinate"] = self.location.y

        kwargs["layers"] = [Layer(**d) for d in self.layers]

        return InternalProfile(**kwargs)
