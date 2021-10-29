from enum import Enum, IntEnum
from math import isfinite
from typing import List, Optional, Union

from pydantic import validator

from geolib.geometry.one import Point
from geolib.models import BaseDataClass

from .soil_utils import Color


class SoilBaseModel(BaseDataClass):
    class Config:
        extra = "forbid"

    @validator("*")
    def fail_on_infinite(cls, v, values, field):
        if isinstance(v, float) and not isfinite(v):
            raise ValueError(
                "Only finite values are supported, don't use nan, -inf or inf."
            )
        return v


class DistributionType(IntEnum):
    Undefined = 0
    Normal = 2
    LogNormal = 3
    Deterministic = 4


class StochasticParameter(SoilBaseModel):
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
    Shear Strength Model Type. These types represent the
    shear strength model that can be found in the UI of
    the D-Stability program.
    """

    MOHR_COULOMB = "Mohr_Coulomb"
    NONE = "None"
    SHANSEP = "SHANSEP"
    SUTABLE = "SuTable"

    def transform_shear_strength_model_type_to_internal(self):
        from geolib.models.dstability.internal import (
            ShearStrengthModelTypePhreaticLevelInternal,
        )

        transformation_dict = {
            "Mohr_Coulomb": ShearStrengthModelTypePhreaticLevelInternal.C_PHI,
            "None": ShearStrengthModelTypePhreaticLevelInternal.NONE,
            "SHANSEP": ShearStrengthModelTypePhreaticLevelInternal.SU,
            "SuTable": ShearStrengthModelTypePhreaticLevelInternal.SUTABLE,
        }
        return transformation_dict[self.value]


class MohrCoulombParameters(SoilBaseModel):
    """
    Mohr Coulomb parameters class
    """

    cohesion: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    dilatancy_angle: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    friction_angle: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    friction_angle_interface: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    cohesion_and_friction_angle_correlated: Optional[bool] = None


class SuTablePoint(SoilBaseModel):
    su: float = None
    stress: float = None


class UndrainedParameters(SoilBaseModel):
    """
    Undrained shear strength parameters class. This class includes the SU Table and SHANSEP model variables included in D-Stability.
    """

    shear_strength_ratio: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    shear_strength_ratio_and_shear_strength_exponent_correlated: Optional[bool] = None
    strength_increase_exponent: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    s_and_m_correlated: Optional[bool] = None
    undrained_shear_strength: Optional[float] = None
    undrained_shear_strength_top: Optional[float] = None
    undrained_shear_strength_bottom: Optional[float] = None
    undrained_shear_strength_bearing_capacity_factor: Optional[float] = None
    su_table: Optional[List[SuTablePoint]] = None
    probabilistic_su_table: Optional[bool] = None
    su_table_variation_coefficient: Optional[float] = None

    def to_su_table_points(self):
        from geolib.models.dstability.internal import PersistableSuTablePoint

        su_table = None
        if self.su_table is not None:
            su_table = []
            for su_point in self.su_table:
                su_table.append(
                    PersistableSuTablePoint(
                        EffectiveStress=su_point.stress, Su=su_point.su
                    )
                )
        return su_table


class BjerrumParameters(SoilBaseModel):
    """
    Bjerrum parameters class

    input_type_is_comp_ratio: [bool] is true when compression input mode is "compression ratio", false when compression
                                     input mode is "Compression index"
    If input_type_is_comp_ratio is true, the following parameters are used as input:
            reloading_swelling_RR
            compression_ratio_CR
            coef_secondary_compression_Ca

    If input_type_is_comp_ratio is false, the following parameters are used as input:
            reloading_swelling_index_Cr
            compression_index_Cc
            coef_secondary_compression_Ca
    """

    input_type_is_comp_ratio: Optional[bool] = None
    reloading_ratio: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    primary_compression_ratio: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    correlation_reload_primary_compression_ratio: Optional[float] = None
    reloading_index: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    primary_compression_index: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    coef_secondary_compression_Ca: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    reloading_swelling_RR: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    compression_ratio_CR: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    reloading_swelling_index_Cr: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    compression_index_Cc: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()


class StateType(Enum):
    POP = "POP"
    OCR = "OCR"
    YIELD_STRESS = "yield_stress"


class IsotacheParameters(SoilBaseModel):
    precon_isotache_type: Optional[StateType] = None
    reloading_swelling_constant_a: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()  # SoilStdPriCompIndex
    primary_compression_constant_b: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()  # SoilStdSecCompIndex
    secondary_compression_constant_c: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()  # SoilStdSecCompRate


class KoppejanParameters(SoilBaseModel):
    precon_koppejan_type: Optional[StateType] = None
    preconsolidation_pressure: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    soil_ap_as_approximation_by_Cp_Cs: Optional[bool] = False
    primary_Cp: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    primary_Cp_point: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    secular_Cs: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    secular_Cs_point: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    primary_Ap: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    primary_Asec: Optional[Union[float, StochasticParameter]] = StochasticParameter()


class StorageTypes(IntEnum):
    vertical_consolidation_coefficient = 0
    constant_permeability = 1
    strain_dependent_permeability = 2


class StorageParameters(SoilBaseModel):
    """
    In this case vertical_permeability has a unit of [m/day]. In GUI
    of the D-Settlement this value is displayed as [m/s].
    """

    vertical_permeability: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    permeability_horizontal_factor: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    horizontal_permeability: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    storage_type: Optional[StorageTypes]
    permeability_strain_type: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter(mean=1e15)
    vertical_consolidation_coefficient: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()


class SoilWeightParameters(SoilBaseModel):
    saturated_weight: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    unsaturated_weight: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()


class GrainType(IntEnum):
    FINE = 0
    COARSE = 1


class SoilClassificationParameters(SoilBaseModel):
    """
    Soil classification class
    """

    initial_void_ratio: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    min_void_ratio: Optional[float] = None
    max_void_ratio: Optional[float] = None
    porosity: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    relative_density: Optional[float] = None
    d_50: Optional[float] = None
    grain_type: Optional[
        GrainType
    ] = GrainType.FINE  # TODO this must refer to a intenum class


class SoilStiffnessParameters(SoilBaseModel):
    emod_menard: Optional[float] = None


class ModulusSubgradeReaction(IntEnum):
    MENARD = 0
    MANUAL = 1


class LambdaType(IntEnum):
    MANUAL = 0
    MULLERBRESLAU = 1
    KOTTER = 2


class SubgradeReactionParameters(SoilBaseModel):
    modulus_subgrade_reaction_type: Optional[ModulusSubgradeReaction] = None
    lambda_type: Optional[LambdaType] = None
    tangent_secant_1: Optional[float] = None
    tangent_secant_2: Optional[float] = None
    tangent_secant_3: Optional[float] = None
    k_o_top: Optional[float] = None
    k_1_top: Optional[float] = None
    k_2_top: Optional[float] = None
    k_3_top: Optional[float] = None
    k_4_top: Optional[float] = None
    k_o_bottom: Optional[float] = None
    k_1_bottom: Optional[float] = None
    k_2_bottom: Optional[float] = None
    k_3_bottom: Optional[float] = None
    k_4_bottom: Optional[float] = None
    k_1_top_side: Optional[float] = None
    k_2_top_side: Optional[float] = None
    k_3_top_side: Optional[float] = None
    k_1_bottom_side: Optional[float] = None
    k_2_bottom_side: Optional[float] = None
    k_3_bottom_side: Optional[float] = None


class EarthPressureCoefficientsType(IntEnum):
    MANUAL = 0
    BRINCHHANSEN = 1


class EarthPressureCoefficients(SoilBaseModel):
    earth_pressure_coefficients_type: Optional[
        EarthPressureCoefficientsType
    ] = EarthPressureCoefficientsType.BRINCHHANSEN
    active: Optional[float] = None
    neutral: Optional[float] = None
    passive: Optional[float] = None


class HorizontalBehaviourType(IntEnum):
    Stiff = 1
    Elastic = 2
    Foundation = 3


class HorizontalBehaviour(SoilBaseModel):
    """
    Horizontal behaviour class
    """

    horizontal_behavior_type: Optional[HorizontalBehaviourType] = None
    soil_elasticity: Optional[float] = None
    soil_default_elasticity: Optional[bool] = None


class ConeResistance(SoilBaseModel):
    """
    Cone resistance class
    """

    max_cone_resistance_type: Optional[Enum] = None
    max_cone_resistance: Optional[float] = None


class StatePoint(SoilBaseModel):
    state_point_id: Optional[str] = None
    state_layer_id: Optional[str] = None
    state_point_type: Optional[StateType] = None
    state_point_is_probabilistic: Optional[bool] = None


class StateLine(SoilBaseModel):
    """
    TODO Decide if we want to keep state in soil class
    TODO decide if we want cross-dependency to geometry class
    """

    state_line_points: Optional[List[Point]]


class SoilState(SoilBaseModel):
    use_equivalent_age: Optional[bool] = None
    equivalent_age: Optional[float] = None
    state_points: Optional[StatePoint] = None
    state_lines: Optional[StateLine] = None

    yield_stress_layer: Optional[
        Union[float, StochasticParameter]
    ] = StochasticParameter()
    ocr_layer: Optional[Union[float, StochasticParameter]] = StochasticParameter()
    pop_layer: Optional[Union[float, StochasticParameter]] = StochasticParameter()


class SoilType(IntEnum):
    GRAVEL = 0
    SAND = 1
    LOAM = 2
    CLAY = 3
    PEAT = 4
    SANDY_LOAM = 5


class Soil(SoilBaseModel):
    """Soil Material."""

    id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    color: Color = Color("grey")

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

    horizontal_behaviour: Optional[HorizontalBehaviour] = HorizontalBehaviour()
    cone_resistance: Optional[ConeResistance] = ConeResistance()
    use_tension: Optional[bool] = None
    use_probabilistic_defaults: Optional[bool] = False
    soil_type_settlement_by_vibrations: Optional[SoilType] = SoilType.SAND
    soil_type_nl: Optional[SoilType] = SoilType.SAND
    soil_type_be: Optional[SoilType] = SoilType.SAND
    soil_state: Optional[SoilState] = SoilState()
    shear_strength_model_above_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    shear_strength_model_below_phreatic_level: Optional[
        ShearStrengthModelTypePhreaticLevel
    ] = None
    is_drained: Optional[bool] = None
    is_probabilistic: Optional[bool] = None

    earth_pressure_coefficients: Optional[
        EarthPressureCoefficients
    ] = EarthPressureCoefficients()
    subgrade_reaction_parameters: Optional[
        SubgradeReactionParameters
    ] = SubgradeReactionParameters()
    shell_factor: Optional[float] = None

    @staticmethod
    def set_stochastic_parameters(input_class: object):
        """
        Converts float to stochastic parameter, where the mean is set as the input float value
        Args:
            input_class:

        Returns:

        """

        try:
            class_dict = input_class.dict()
        except AttributeError:
            return input_class

        for field in input_class.__fields__:
            parameter = input_class.__fields__[field]
            if isinstance(parameter.default, StochasticParameter):
                if isinstance(class_dict[field], float):
                    setattr(
                        input_class, field, StochasticParameter(mean=class_dict[field])
                    )

        return input_class

    def set_all_stochastic_parameters(self):
        """
        Loop over all fields in soil class, and converts floats to stochastic parameters if necessary

        Returns:

        """
        for field in self.__fields__:
            self.set_stochastic_parameters(self.__getattribute__(field))

    @staticmethod
    def __transfer_soil_dict_to_model(soil_dict, model_soil):
        """
        Transfers items from soil dictionary to model if the item is not None
        Args:
            soil_dict: soil dictionary
            model_soil: internal soil in model

        Returns:

        """
        for key, value in dict(
            soil_dict
        ).items():  # override default values with those of the soil
            if key in dict(model_soil).keys() and value is not None:
                setattr(model_soil, key, value)
        return model_soil

    def __to_dstability_stochastic_parameter(
        self, stochastic_parameter: StochasticParameter
    ):
        from geolib.models.dstability.internal import (
            PersistableStochasticParameter as DStabilityStochasticParameter,
        )

        kwargs = {
            "IsProbabilistic": stochastic_parameter.is_probabilistic,
            "Mean": stochastic_parameter.mean,
            "StandardDeviation": stochastic_parameter.standard_deviation,
        }

        return self.__transfer_soil_dict_to_model(kwargs, DStabilityStochasticParameter())

    def __to_su_table(self):
        from geolib.models.dstability.internal import PersistableSuTable

        kwargs = {
            "StrengthIncreaseExponent": self.undrained_parameters.strength_increase_exponent.mean,
            "StrengthIncreaseExponentStochasticParameter": self.__to_dstability_stochastic_parameter(
                stochastic_parameter=self.undrained_parameters.strength_increase_exponent
            ),
            "IsSuTableProbabilistic": self.undrained_parameters.probabilistic_su_table,
            "SuTableVariationCoefficient": self.undrained_parameters.su_table_variation_coefficient,
            "SuTablePoints": self.undrained_parameters.to_su_table_points(),
        }
        return self.__transfer_soil_dict_to_model(kwargs, PersistableSuTable())

    def _to_dstability(self):
        from geolib.models.dstability.internal import PersistableSoil as DStabilitySoil

        self.set_all_stochastic_parameters()

        if self.shear_strength_model_above_phreatic_level is not None:
            shear_strength_model_above_phreatic_level = (
                self.shear_strength_model_above_phreatic_level.transform_shear_strength_model_type_to_internal()
            )
        else:
            shear_strength_model_above_phreatic_level = (
                self.shear_strength_model_above_phreatic_level
            )
        if self.shear_strength_model_below_phreatic_level is not None:
            shear_strength_model_below_phreatic_level = (
                self.shear_strength_model_below_phreatic_level.transform_shear_strength_model_type_to_internal()
            )
        else:
            shear_strength_model_below_phreatic_level = (
                self.shear_strength_model_below_phreatic_level
            )

        kwargs = {
            "Id": self.id,
            "Name": self.name,
            "Code": self.code,
            "Cohesion": self.mohr_coulomb_parameters.cohesion.mean,
            "CohesionStochasticParameter": self.__to_dstability_stochastic_parameter(
                self.mohr_coulomb_parameters.cohesion
            ),
            "FrictionAngle": self.mohr_coulomb_parameters.friction_angle.mean,
            "FrictionAngleStochasticParameter": self.__to_dstability_stochastic_parameter(
                self.mohr_coulomb_parameters.friction_angle
            ),
            "CohesionAndFrictionAngleCorrelated": self.mohr_coulomb_parameters.cohesion_and_friction_angle_correlated,
            "Dilatancy": self.mohr_coulomb_parameters.dilatancy_angle.mean,
            "DilatancyStochasticParameter": self.__to_dstability_stochastic_parameter(
                self.mohr_coulomb_parameters.dilatancy_angle
            ),
            "ShearStrengthRatio": self.undrained_parameters.shear_strength_ratio.mean,
            "ShearStrengthRatioStochasticParameter": self.__to_dstability_stochastic_parameter(
                self.undrained_parameters.shear_strength_ratio
            ),
            "StrengthIncreaseExponent": self.undrained_parameters.strength_increase_exponent.mean,
            "StrengthIncreaseExponentStochasticParameter": self.__to_dstability_stochastic_parameter(
                self.undrained_parameters.strength_increase_exponent
            ),
            "ShearStrengthRatioAndShearStrengthExponentCorrelated": self.undrained_parameters.shear_strength_ratio_and_shear_strength_exponent_correlated,
            "VolumetricWeightAbovePhreaticLevel": self.soil_weight_parameters.unsaturated_weight.mean,
            "VolumetricWeightBelowPhreaticLevel": self.soil_weight_parameters.saturated_weight.mean,
            "IsProbabilistic": self.is_probabilistic,
            "ShearStrengthModelTypeAbovePhreaticLevel": shear_strength_model_above_phreatic_level,
            "ShearStrengthModelTypeBelowPhreaticLevel": shear_strength_model_below_phreatic_level,
            "SuTable": self.__to_su_table(),
        }

        return self.__transfer_soil_dict_to_model(kwargs, DStabilitySoil())

    def _to_dfoundations(self):
        self.set_all_stochastic_parameters()

        from geolib.models.dfoundations.internal_soil import Soil as DFoundationSoil

        return DFoundationSoil(
            name=self.name,
            soilcolor=self.color.to_internal(),
            soilsoiltype=self.soil_type_nl,
            soilbelgiansoiltype=self.soil_type_be,
            soilgamdry=self.soil_weight_parameters.unsaturated_weight.mean,
            soilgamwet=self.soil_weight_parameters.saturated_weight.mean,
            soilinitialvoidratio=self.soil_classification_parameters.initial_void_ratio.mean,
            soildiameterd50=self.soil_classification_parameters.d_50,
            soilminvoidratio=self.soil_classification_parameters.min_void_ratio,
            soilmaxvoidratio=self.soil_classification_parameters.max_void_ratio,
            soilcohesion=self.mohr_coulomb_parameters.cohesion.mean,
            soilphi=self.mohr_coulomb_parameters.friction_angle.mean,
            soilcu=self.undrained_parameters.undrained_shear_strength,
            soilmaxconeresisttype=self.cone_resistance.max_cone_resistance_type,
            soilmaxconeresist=self.cone_resistance.max_cone_resistance_type,
            soilusetension=self.use_tension,
            soilca=self.bjerrum_parameters.coef_secondary_compression_Ca.mean,
            soilccindex=self.bjerrum_parameters.compression_index_Cc.mean,
        )

    @staticmethod
    def __state_type_to_dsettlement(state_type: StateType):
        from geolib.models.dsettlement.internal_soil import (
            PreconType as DSettlementPreconsolidationType,
        )

        if state_type is None:
            dsettlement_state_type = DSettlementPreconsolidationType.UNDEFINED
        elif state_type == state_type.OCR:
            dsettlement_state_type = DSettlementPreconsolidationType.OCR
        elif state_type == state_type.YIELD_STRESS:
            dsettlement_state_type = (
                DSettlementPreconsolidationType.PRECONSOLIDATION_PRESSURE
            )
        elif state_type == state_type.POP:
            dsettlement_state_type = DSettlementPreconsolidationType.POP
        else:
            return None

        return dsettlement_state_type

    def _to_dsettlement(self):
        from geolib.models.dsettlement.internal_soil import (
            SoilInternal as DSettlementSoil,
        )

        self.set_all_stochastic_parameters()

        kwargs = {
            "name": self.name,
            "soilcolor": self.color.to_internal(),
            "soilgamdry": self.soil_weight_parameters.unsaturated_weight.mean,
            "soilgamwet": self.soil_weight_parameters.saturated_weight.mean,
            "soilinitialvoidratio": self.soil_classification_parameters.initial_void_ratio.mean,
            "soilcohesion": self.mohr_coulomb_parameters.cohesion.mean,
            "soilphi": self.mohr_coulomb_parameters.friction_angle.mean,
            "soilpreconisotachetype": self.__state_type_to_dsettlement(
                self.isotache_parameters.precon_isotache_type
            ),
            "soilpreconkoppejantype": self.__state_type_to_dsettlement(
                self.koppejan_parameters.precon_koppejan_type
            ),
            "soiluseequivalentage": self.soil_state.use_equivalent_age,
            "soilequivalentage": self.soil_state.equivalent_age,
            "soilpc": self.soil_state.yield_stress_layer.mean,
            "soilocr": self.soil_state.ocr_layer.mean,
            "soilpop": self.soil_state.pop_layer.mean,
            "soillimitstress": None,
            "soildrained": self.is_drained,
            "soilapasapproximationbycpcs": self.koppejan_parameters.soil_ap_as_approximation_by_Cp_Cs,
            "soilcv": self.storage_parameters.vertical_consolidation_coefficient.mean,
            "soilpermeabilityver": self.storage_parameters.vertical_permeability.mean,
            "soilpermeabilityhorfactor": self.storage_parameters.permeability_horizontal_factor.mean,
            "soilstoragetype": self.storage_parameters.storage_type,
            "soilpermeabilitystrainmodulus": self.storage_parameters.permeability_strain_type.mean,
            "soiluseprobdefaults": self.use_probabilistic_defaults,
            "soilstdgamdry": self.soil_weight_parameters.unsaturated_weight.standard_deviation,
            "soilstdgamwet": self.soil_weight_parameters.saturated_weight.standard_deviation,
            "soilstdcv": self.storage_parameters.vertical_consolidation_coefficient.standard_deviation,
            "soilstdpc": self.soil_state.yield_stress_layer.standard_deviation,
            "soilstdpricompindex": self.isotache_parameters.reloading_swelling_constant_a.standard_deviation,
            "soilstdseccompindex": self.isotache_parameters.primary_compression_constant_b.standard_deviation,
            "soilstdseccomprate": self.isotache_parameters.secondary_compression_constant_c.standard_deviation,
            "soilstdocr": self.soil_state.ocr_layer.standard_deviation,
            "soilstdpermeabilityver": self.storage_parameters.vertical_permeability.standard_deviation,
            "soilstdpop": self.soil_state.pop_layer.standard_deviation,
            "soilstdpermeabilityhorfactor": self.storage_parameters.permeability_horizontal_factor.standard_deviation,
            "soilstdinitialvoidratio": self.soil_classification_parameters.initial_void_ratio.standard_deviation,
            "soilstdpermeabilitystrainmodulus": None,
            "soilstdlimitstress": None,
            "soilstdcp": self.koppejan_parameters.primary_Cp.standard_deviation,
            "soilstdcp1": self.koppejan_parameters.primary_Cp_point.standard_deviation,
            "soilstdcs": self.koppejan_parameters.secular_Cs.standard_deviation,
            "soilstdcs1": self.koppejan_parameters.secular_Cs_point.standard_deviation,
            "soilstdap": self.koppejan_parameters.primary_Ap.standard_deviation,
            "soilstdasec": self.koppejan_parameters.primary_Asec.standard_deviation,
            "soilstdcar": None,
            "soilstdca": self.bjerrum_parameters.coef_secondary_compression_Ca.standard_deviation,
            "soilstdrratio": self.bjerrum_parameters.reloading_swelling_RR.standard_deviation,
            "soilstdcratio": self.bjerrum_parameters.compression_ratio_CR.standard_deviation,
            "soilstdsratio": None,
            "soilstdcrindex": self.bjerrum_parameters.reloading_swelling_index_Cr.standard_deviation,
            "soilstdccindex": self.bjerrum_parameters.compression_index_Cc.standard_deviation,
            "soilstdcswindex": None,
            "soildistgamdry": self.soil_weight_parameters.unsaturated_weight.distribution_type,
            "soildistgamwet": self.soil_weight_parameters.saturated_weight.distribution_type,
            "soildistcv": self.storage_parameters.vertical_consolidation_coefficient.distribution_type,
            "soildistdpc": self.koppejan_parameters.preconsolidation_pressure.distribution_type,
            "soildistpricompindex": self.isotache_parameters.reloading_swelling_constant_a.distribution_type,
            "soildistseccompindex": self.isotache_parameters.primary_compression_constant_b.distribution_type,
            "soildistseccomprate": self.isotache_parameters.secondary_compression_constant_c.distribution_type,
            "soildistocr": self.soil_state.ocr_layer.distribution_type,
            "soildistpermeabilityver": self.storage_parameters.vertical_permeability.distribution_type,
            "soildistpop": self.soil_state.pop_layer.distribution_type,
            "soildistpermeabilityhorfactor": self.storage_parameters.permeability_horizontal_factor.distribution_type,
            "soildistinitialvoidratio": self.soil_classification_parameters.initial_void_ratio.distribution_type,
            "soildistpermeabilitystrainmodulus": self.storage_parameters.permeability_strain_type.distribution_type,
            "soildistlimitstress": None,
            "soildistcp": self.koppejan_parameters.primary_Cp.distribution_type,
            "soildistcp1": self.koppejan_parameters.primary_Cp_point.distribution_type,
            "soildistcs": self.koppejan_parameters.secular_Cs.distribution_type,
            "soildistcs1": self.koppejan_parameters.secular_Cs_point.distribution_type,
            "soildistap": self.koppejan_parameters.primary_Ap.distribution_type,
            "soildistasec": self.koppejan_parameters.primary_Asec.distribution_type,
            "soildistcar": None,
            "soildistca": self.bjerrum_parameters.coef_secondary_compression_Ca.distribution_type,
            "soildistrratio": self.bjerrum_parameters.reloading_swelling_RR.distribution_type,
            "soildistcratio": self.bjerrum_parameters.compression_ratio_CR.distribution_type,
            "soildistsratio": None,
            "soildistcrindex": self.bjerrum_parameters.reloading_swelling_index_Cr.distribution_type,
            "soildistccindex": self.bjerrum_parameters.compression_index_Cc.distribution_type,
            "soildistcswindex": None,
            "soilcorcpcp1": self.koppejan_parameters.primary_Cp.correlation_coefficient,
            "soilcorcscp1": self.koppejan_parameters.secular_Cs.correlation_coefficient,
            "soilcorcs1cp1": self.koppejan_parameters.secular_Cs_point.correlation_coefficient,
            "soilcorapcp1": self.koppejan_parameters.primary_Ap.correlation_coefficient,
            "soilcoraseccp1": self.koppejan_parameters.primary_Asec.correlation_coefficient,
            "soilcorcrindexccindex": self.bjerrum_parameters.reloading_swelling_index_Cr.correlation_coefficient,
            "soilcorrratiocratio": self.bjerrum_parameters.reloading_swelling_RR.correlation_coefficient,
            "soilcorcaccindexorcratio": self.bjerrum_parameters.coef_secondary_compression_Ca.correlation_coefficient,
            "soilcorpricompindexseccompindex": self.isotache_parameters.reloading_swelling_constant_a.correlation_coefficient,
            "soilcorseccomprateseccompindex": self.isotache_parameters.secondary_compression_constant_c.correlation_coefficient,
            "soilcp": self.koppejan_parameters.primary_Cp.mean,
            "soilcp1": self.koppejan_parameters.primary_Cp_point.mean,
            "soilcs": self.koppejan_parameters.secular_Cs.mean,
            "soilcs1": self.koppejan_parameters.secular_Cs_point.mean,
            "soilap": self.koppejan_parameters.primary_Ap.mean,
            "soilasec": self.koppejan_parameters.primary_Asec.mean,
            "soilcar": None,
            "soilca": self.bjerrum_parameters.coef_secondary_compression_Ca.mean,
            "soilcompratio": self.bjerrum_parameters.input_type_is_comp_ratio,
            "soilrratio": self.bjerrum_parameters.reloading_swelling_RR.mean,
            "soilcratio": self.bjerrum_parameters.compression_ratio_CR.mean,
            "soilsratio": None,
            "soilcrindex": self.bjerrum_parameters.reloading_swelling_index_Cr.mean,
            "soilccindex": self.bjerrum_parameters.compression_index_Cc.mean,
            "soilcswindex": None,
            "soilpricompindex": self.isotache_parameters.reloading_swelling_constant_a.mean,
            "soilseccompindex": self.isotache_parameters.primary_compression_constant_b.mean,
            "soilseccomprate": self.isotache_parameters.secondary_compression_constant_c.mean,
            "soilhorizontalbehaviourtype": self.horizontal_behaviour.soil_elasticity,
            "soilelasticity": self.horizontal_behaviour.soil_default_elasticity,
            "soildefaultelasticity": self.horizontal_behaviour.soil_default_elasticity,
        }

        return self.__transfer_soil_dict_to_model(kwargs, DSettlementSoil())

    def _to_dsheetpiling(self):
        # Only import it here to prevent circular import errors
        from geolib.models.dsheetpiling.internal import Soil as DSheetPilingSoil
        from geolib.models.dsheetpiling.settings import (
            EarthPressureCoefficients,
            SoilTypeModulusSubgradeReaction,
        )

        self.set_all_stochastic_parameters()

        return DSheetPilingSoil(
            name=self.name,
            soilcolor=self.color.to_internal(),
            soilsoiltype=SoilTypeModulusSubgradeReaction(
                self.soil_type_settlement_by_vibrations.value
            ),
            soilgraintype=self.soil_classification_parameters.grain_type,
            soilgamdry=self.soil_weight_parameters.unsaturated_weight.mean,
            soilgamwet=self.soil_weight_parameters.saturated_weight.mean,
            soilrelativedensity=self.soil_classification_parameters.relative_density,
            soilemodmenard=self.soil_stiffness_parameters.emod_menard,
            soilcohesion=self.mohr_coulomb_parameters.cohesion.mean,
            soilphi=self.mohr_coulomb_parameters.friction_angle.mean,
            soildelta=self.mohr_coulomb_parameters.friction_angle_interface.mean,
            soilocr=self.soil_state.ocr_layer.mean,
            soilpermeabkx=self.storage_parameters.horizontal_permeability.mean,
            soilstdcohesion=self.mohr_coulomb_parameters.cohesion.standard_deviation,
            soilstdphi=self.mohr_coulomb_parameters.friction_angle.standard_deviation,
            soildistcohesion=self.mohr_coulomb_parameters.cohesion.distribution_type,
            soildistphi=self.mohr_coulomb_parameters.friction_angle.distribution_type,
            soilla=self.earth_pressure_coefficients.active,
            soilln=self.earth_pressure_coefficients.neutral,
            soillp=self.earth_pressure_coefficients.passive,
            soilusemenard=self.subgrade_reaction_parameters.modulus_subgrade_reaction_type,
            soilusebrinchhansen=EarthPressureCoefficients(
                self.earth_pressure_coefficients.earth_pressure_coefficients_type.value
            ),
            soilshellfactor=self.shell_factor,
            soillambdatype=self.subgrade_reaction_parameters.lambda_type,
            soillam1=self.subgrade_reaction_parameters.tangent_secant_1,
            soillam2=self.subgrade_reaction_parameters.tangent_secant_2,
            soillam3=self.subgrade_reaction_parameters.tangent_secant_3,
            soilkb0=self.subgrade_reaction_parameters.k_o_top,
            soilkb1=self.subgrade_reaction_parameters.k_1_top,
            soilkb2=self.subgrade_reaction_parameters.k_2_top,
            soilkb3=self.subgrade_reaction_parameters.k_3_top,
            soilkb4=self.subgrade_reaction_parameters.k_4_top,
            soilko0=self.subgrade_reaction_parameters.k_o_bottom,
            soilko1=self.subgrade_reaction_parameters.k_1_bottom,
            soilko2=self.subgrade_reaction_parameters.k_2_bottom,
            soilko3=self.subgrade_reaction_parameters.k_3_bottom,
            soilko4=self.subgrade_reaction_parameters.k_4_bottom,
            soilcurkb1=self.subgrade_reaction_parameters.k_1_top_side,
            soilcurkb2=self.subgrade_reaction_parameters.k_2_top_side,
            soilcurkb3=self.subgrade_reaction_parameters.k_3_top_side,
            soilcurko1=self.subgrade_reaction_parameters.k_1_bottom_side,
            soilcurko2=self.subgrade_reaction_parameters.k_2_bottom_side,
            soilcurko3=self.subgrade_reaction_parameters.k_3_bottom_side,
            soilhorizontalbehaviourtype=self.horizontal_behaviour.horizontal_behavior_type,
        )
