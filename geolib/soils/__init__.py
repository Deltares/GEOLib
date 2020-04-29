from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.color import Color

from geolib.utils import snake_to_camel, camel_to_snake


class PersistableStochasticParameter(BaseModel):
    """
    Stochastic parameters class
    """

    is_probabilistic: Optional[bool] = None
    mean: Optional[float] = None
    standard_deviation: Optional[float] = None
    low_characteristic_value: Optional[float] = None
    high_characteristic_value: Optional[float] = None
    low_design_value: Optional[float] = None
    high_design_value: Optional[float] = None


class ShearStrengthModelTypePhreaticLevel(Enum):
    """
    Shear Strength Model Type
    """

    C_PHI = "CPhi"
    NONE = "None"
    SU = "Su"


class MohrCoulombParameters(BaseModel):
    """
    Mohr Coulomb parameters class
    """

    cohesion: Optional[float] = None
    cohesion_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    dilatancy_angle: Optional[float] = None
    dilatancy_angle_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    friction_angle: Optional[float] = None
    friction_angle_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    friction_angle_interface: Optional[float] = None
    friction_angle_interface_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    cohesion_and_friction_angle_correlated: Optional[bool] = None


class UndrainedParameters(BaseModel):
    """
    Undrained shear strength parameters class
    """

    shear_strength_ratio: Optional[float] = None
    shear_strength_ratio_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    strength_increase_exponent: Optional[float] = None
    strength_increase_exponent_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    s_and_m_correlated: Optional[bool] = None
    undrained_shear_strength: Optional[float] = None
    undrained_shear_strength_top: Optional[float] = None
    undrained_shear_strength_bottom: Optional[float] = None
    undrained_shear_strength_bearing_capacity_factor: Optional[float] = None


class BjerrumParameters(BaseModel):
    """
    Bjerrum parameters class
    """

    compression_input_type: Optional[Enum] = None
    reloading_ratio: Optional[float] = None
    reloading_ratio_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    primary_compression_ratio: Optional[float] = None
    primary_compression_ratio_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    correlation_reload_primary_compression_ratio: Optional[float] = None
    reloading_index: Optional[float] = None
    reloading_index_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    primary_compression_index: Optional[float] = None
    primary_compression_index_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None


class IsotacheParameters(BaseModel):
    pass


class KoppejanParameters(BaseModel):
    pass


class StorageParameters(BaseModel):
    pass


class SoilWeightParameters(BaseModel):
    pass


class SoilClassificationParameters(BaseModel):
    """
    Soil classification class
    """

    initial_void_ratio: Optional[float] = None
    initial_void_ratio_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    min_void_ratio: Optional[float] = None
    max_void_ratio: Optional[float] = None
    porosity: Optional[float] = None
    porosity_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    relative_density: Optional[float] = None
    d_50: Optional[float] = None
    grain_type: Optional[Enum] = None


class SoilStiffnessParameters(BaseModel):
    pass


class SoilParameters(BaseModel):
    """
    Soil Parameters class
    """

    mohr_coulomb_parameters: Optional[MohrCoulombParameters] = None
    undrained_parameters: Optional[UndrainedParameters] = None
    bjerrum_parameters: Optional[BjerrumParameters] = None
    isotache_parameters: Optional[IsotacheParameters] = None
    koppejan_parameters: Optional[KoppejanParameters] = None
    storage_parameters: Optional[StorageParameters] = None
    soil_weight_parameters: Optional[SoilWeightParameters] = None
    soil_classification_parameters: Optional[SoilClassificationParameters] = None
    soil_stiffness_parameters: Optional[SoilStiffnessParameters] = None


class HorizontalBehaviour(BaseModel):
    """
    Horizontal behaviour class
    """

    pass


class ConeResistance(BaseModel):
    """
    Cone resistance class
    """

    max_cone_resistance_type: Optional[Enum] = None
    max_cone_resistance: Optional[float] = None
    pass


class StateType(Enum):
    """
    todo Decide if we want to keep state in soil class
    """

    POP = "POP"
    OCR = "OCR"
    yield_stress = "yield_stress"


class StatePoint(BaseModel):
    """
    todo Decide if we want to keep state in soil class
    """

    state_point_id: Optional[str] = None
    state_layer_id: Optional[str] = None
    state_point_type: Optional[StateType] = None
    state_point_is_probabilistic: Optional[bool] = None
    yield_stress_layer: Optional[float] = None
    yield_stress_layer_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    ocr_layer: Optional[float] = None
    ocr_layer_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    pop_layer: Optional[float] = None
    pop_layer_stochastic_parameter: Optional[PersistableStochasticParameter] = None


class StateLine(BaseModel):
    """
    todo Decide if we want to keep state in soil class
    todo decide if we want cross-dependency to geometry class
    """

    from geolib.geometry import Point

    state_line_points: Optional[List[Point]]
    pass


class SoilState(BaseModel):
    """
    todo Decide if we want to keep state in soil class
    """

    use_equivalent_age: Optional[bool] = None
    equivalent_age: Optional[float] = None
    state_points: Optional[StatePoint] = None
    state_lines: Optional[StateLine] = None


class ConstitutiveModels(BaseModel):
    """
    Constitutive models class
    """

    shear_strength_model_above_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    shear_strength_model_below_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    settlement_model: Optional[Enum] = None


class Soil(BaseModel):
    """Soil Material class."""

    id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    color: Optional[Color] = None
    soil_parameters: Optional[SoilParameters] = None
    horizontal_behaviour: Optional[HorizontalBehaviour] = None
    cone_resistance: Optional[ConeResistance] = None
    use_tension: Optional[bool] = None
    use_probabilistic_defaults: Optional[bool] = None
    soil_type_nl: Optional[str] = None
    soil_type_be: Optional[str] = None
    soil_state: Optional[SoilState] = None
    drainage_type: Optional[Enum] = None
    constitutive_model: Optional[ConstitutiveModels] = None

    cohesion: Optional[float] = None
    cohesion_and_friction_angle_correlated: Optional[bool] = None
    cohesion_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    dilatancy: Optional[float] = None
    dilatancy_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    friction_angle: Optional[float] = None
    friction_angle_stochastic_parameter: Optional[PersistableStochasticParameter] = None
    is_probabilistic: Optional[bool] = None
    shear_strength_model_type_above_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    shear_strength_model_type_below_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    shear_strength_ratio: Optional[float] = None
    shear_strength_ratio_and_shear_strength_exponent_correlated: Optional[bool] = None
    shear_strength_ratio_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    strength_increase_exponent: Optional[float] = None
    strength_increase_exponent_stochastic_parameter: Optional[
        PersistableStochasticParameter
    ] = None
    volumetric_weight_above_phreatic_level: Optional[float] = None
    volumetric_weight_below_phreatic_level: Optional[float] = None

