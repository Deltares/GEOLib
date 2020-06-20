from enum import Enum, IntEnum
from typing import List, Optional

from pydantic import BaseModel
from pydantic.color import Color

from geolib.utils import snake_to_camel, camel_to_snake
from geolib.geometry.one import Point


class DistributionType(IntEnum):
    Undefined = 0
    Normal = 2
    LogNormal = 3
    Deterministic = 4


class StochasticParameter(BaseModel):
    """
    Stochastic parameters class
    """

    is_probabilistic: bool = False
    mean: Optional[float] = None
    standard_deviation: Optional[float] = 0
    distribution_type: Optional[DistributionType] = DistributionType.Normal
    correlation_coefficient: Optional[float] = None
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

    cohesion: Optional[StochasticParameter] = StochasticParameter()
    dilatancy_angle: Optional[float] = None
    dilatancy_angle_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    friction_angle: Optional[float] = None
    friction_angle_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    friction_angle_interface: Optional[float] = None
    friction_angle_interface_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    cohesion_and_friction_angle_correlated: Optional[bool] = None


class UndrainedParameters(BaseModel):
    """
    Undrained shear strength parameters class
    """

    shear_strength_ratio: Optional[float] = None
    shear_strength_ratio_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    strength_increase_exponent: Optional[float] = None
    strength_increase_exponent_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    s_and_m_correlated: Optional[bool] = None
    undrained_shear_strength: Optional[float] = None
    undrained_shear_strength_top: Optional[float] = None
    undrained_shear_strength_bottom: Optional[float] = None
    undrained_shear_strength_bearing_capacity_factor: Optional[float] = None
    vertical_consolidation_coefficient: Optional[
        StochasticParameter
    ] = StochasticParameter()


class BjerrumParameters(BaseModel):
    """
    Bjerrum parameters class
    """

    compression_input_type: Optional[Enum] = None
    reloading_ratio: Optional[float] = None
    reloading_ratio_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    primary_compression_ratio: Optional[float] = None
    primary_compression_ratio_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    correlation_reload_primary_compression_ratio: Optional[float] = None
    reloading_index: Optional[float] = None
    reloading_index_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    primary_compression_index: Optional[float] = None
    primary_compression_index_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    coef_secondary_compression_Ca: Optional[StochasticParameter] = StochasticParameter()
    reloading_swelling_RR: Optional[StochasticParameter] = StochasticParameter()
    compression_ratio_CR: Optional[StochasticParameter] = StochasticParameter()
    reloading_swelling_index_Cr: Optional[StochasticParameter] = StochasticParameter()
    compression_index_Cc: Optional[StochasticParameter] = StochasticParameter()


class PreconType(IntEnum):
    Undefined = -1
    OverconsolidationRatio = 0
    PreconsolidationPressure = 1
    PreoverburdenPressure = 2


class IsotacheParameters(BaseModel):
    precon_isotache_type: Optional[PreconType] = None
    reloading_swelling_constant_a: Optional[
        StochasticParameter
    ] = None  # SoilStdPriCompIndex
    primary_compression_constant_b: Optional[
        StochasticParameter
    ] = None  # SoilStdSecCompIndex
    secondary_compression_constant_c: Optional[
        StochasticParameter
    ] = None  # SoilStdSecCompRate


class KoppejanParameters(BaseModel):
    precon_koppejan_type: Optional[PreconType] = None
    preconsolidation_pressure: Optional[StochasticParameter] = StochasticParameter()
    soil_ap_as_approximation_by_Cp_Cs: Optional[bool] = False
    primary_Cp: Optional[StochasticParameter] = StochasticParameter()
    primary_Cp_point: Optional[StochasticParameter] = StochasticParameter()
    secular_Cs: Optional[StochasticParameter] = StochasticParameter()
    secular_Cs_point: Optional[StochasticParameter] = StochasticParameter()
    primary_Ap: Optional[StochasticParameter] = StochasticParameter()
    primary_Asec: Optional[StochasticParameter] = StochasticParameter()


class StorageTypes(IntEnum):
    vertical_consolidation_coefficient = 0
    constant_permeability = 1
    strain_dependent_permeability = 2


class StorageParameters(BaseModel):
    vertical_permeability: Optional[StochasticParameter] = StochasticParameter()
    permeability_horizontal_factor: Optional[StochasticParameter] = StochasticParameter()
    storage_type: Optional[StorageTypes]
    permeability_strain_type: Optional[StochasticParameter] = StochasticParameter(
        mean=1e15
    )


class SoilWeightParameters(BaseModel):
    saturated_weight: Optional[StochasticParameter] = StochasticParameter()
    unsaturated_weight: Optional[StochasticParameter] = StochasticParameter()


class CompressionParameters(BaseModel):
    OCR: Optional[StochasticParameter] = StochasticParameter()
    POP: Optional[StochasticParameter] = StochasticParameter()


class SoilClassificationParameters(BaseModel):
    """
    Soil classification class
    """

    initial_void_ratio: Optional[StochasticParameter] = StochasticParameter()
    min_void_ratio: Optional[float] = None
    max_void_ratio: Optional[float] = None
    porosity: Optional[float] = None
    porosity_stochastic_parameter: Optional[StochasticParameter] = StochasticParameter()
    relative_density: Optional[float] = None
    d_50: Optional[float] = None
    grain_type: Optional[Enum] = None


class SoilStiffnessParameters(BaseModel):
    """TODO Why is this class empty?"""


class SoilParameters(BaseModel):
    """
    Soil Parameters class
    """

    mohr_coulomb_parameters: Optional[MohrCoulombParameters] = MohrCoulombParameters()
    undrained_parameters: Optional[UndrainedParameters] = UndrainedParameters()
    bjerrum_parameters: Optional[BjerrumParameters] = BjerrumParameters()
    isotache_parameters: Optional[IsotacheParameters] = IsotacheParameters()
    koppejan_parameters: Optional[KoppejanParameters] = KoppejanParameters()
    storage_parameters: Optional[StorageParameters] = StorageParameters()
    soil_weight_parameters: Optional[SoilWeightParameters] = SoilWeightParameters()
    soil_classification_parameters: Optional[
        SoilClassificationParameters
    ] = SoilClassificationParameters()
    soil_stiffness_parameters: Optional[
        SoilStiffnessParameters
    ] = SoilStiffnessParameters()
    compression_parameters: Optional[CompressionParameters] = CompressionParameters()


class HorizontalBehaviourType(IntEnum):
    Stiff = 1
    Elastic = 2
    Foundation = 3


class HorizontalBehaviour(BaseModel):
    """
    Horizontal behaviour class
    """

    horizontal_behavior_type: Optional[HorizontalBehaviourType] = None
    soil_elasticity: Optional[float] = None
    soil_default_elasticity: Optional[bool] = None


class ConeResistance(BaseModel):
    """
    Cone resistance class
    """

    max_cone_resistance_type: Optional[Enum] = None
    max_cone_resistance: Optional[float] = None


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
        StochasticParameter
    ] = StochasticParameter()
    ocr_layer: Optional[float] = None
    ocr_layer_stochastic_parameter: Optional[StochasticParameter] = StochasticParameter()
    pop_layer: Optional[float] = None
    pop_layer_stochastic_parameter: Optional[StochasticParameter] = StochasticParameter


class StateLine(BaseModel):
    """
    TODO Decide if we want to keep state in soil class
    TODO decide if we want cross-dependency to geometry class
    """

    state_line_points: Optional[List[Point]]


class SoilState(BaseModel):
    """
    TODO Decide if we want to keep state in soil class
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
    soil_parameters: Optional[SoilParameters] = SoilParameters()
    horizontal_behaviour: Optional[HorizontalBehaviour] = HorizontalBehaviour()
    cone_resistance: Optional[ConeResistance] = ConeResistance()
    use_tension: Optional[bool] = None
    use_probabilistic_defaults: Optional[bool] = False
    soil_type_nl: Optional[str] = None
    soil_type_be: Optional[str] = None
    soil_state: Optional[SoilState] = SoilState()
    drainage_type: Optional[Enum] = None
    constitutive_model: Optional[ConstitutiveModels] = ConstitutiveModels()
    is_drained: Optional[bool] = False

    # ..todo:: value is dubbled defined also in soil_parameters in mohr-coloumb should be removed from here
    cohesion: Optional[float] = None
    cohesion_and_friction_angle_correlated: Optional[bool] = None
    cohesion_stochastic_parameter: Optional[StochasticParameter] = StochasticParameter()
    dilatancy: Optional[float] = None
    dilatancy_stochastic_parameter: Optional[StochasticParameter] = StochasticParameter()
    # ..todo:: value is multiply defined and should be removed
    friction_angle: Optional[float] = None
    friction_angle_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    is_probabilistic: Optional[bool] = None
    shear_strength_model_type_above_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ]
    shear_strength_model_type_below_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ]
    shear_strength_ratio: Optional[float] = None
    shear_strength_ratio_and_shear_strength_exponent_correlated: Optional[bool] = None
    shear_strength_ratio_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    strength_increase_exponent: Optional[float] = None
    strength_increase_exponent_stochastic_parameter: Optional[
        StochasticParameter
    ] = StochasticParameter()
    # ..todo:: value is multiply defined and should be removed
    volumetric_weight_above_phreatic_level: Optional[float] = None
    volumetric_weight_below_phreatic_level: Optional[float] = None

    def _to_dfoundations(self):
        from geolib.models.dfoundations.internal_soil import Soil as DFoundationSoil

        return DFoundationSoil(
            name=self.name,
            soilcolor=self.color,
            soilsoiltype=self.soil_type_nl,
            soilbelgiansoiltype=self.soil_type_be,
            soilgamdry=self.soil_parameters.soil_weight_parameters.unsaturated_weight.mean,
            soilgamwet=self.soil_parameters.soil_weight_parameters.saturated_weight.mean,
            soilinitialvoidratio=self.soil_parameters.soil_classification_parameters.initial_void_ratio.mean,
            soildiameterd50=self.soil_parameters.soil_classification_parameters.d_50,
            soilminvoidratio=self.soil_parameters.soil_classification_parameters.min_void_ratio,
            soilmaxvoidratio=self.soil_parameters.soil_classification_parameters.max_void_ratio,
            soilcohesion=self.cohesion,
            soilphi=self.friction_angle,
            soilcu=self.soil_parameters.undrained_parameters.undrained_shear_strength,
            soilmaxconeresisttype=self.cone_resistance.max_cone_resistance_type,
            soilmaxconeresist=self.cone_resistance.max_cone_resistance_type,
            soilusetension=self.use_tension,
            soilca=self.soil_parameters.bjerrum_parameters.coef_secondary_compression_Ca.mean,
            soilccindex=self.soil_parameters.bjerrum_parameters.compression_index_Cc.mean,
        )
