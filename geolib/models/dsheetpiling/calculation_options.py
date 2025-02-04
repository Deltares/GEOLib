from abc import ABCMeta

from pydantic import Field
from typing_extensions import Annotated

from geolib.models import BaseDataClass

from .settings import (
    AssessmentTypeEC7NL,
    CalculationType,
    DesignType,
    PartialFactorCalculationType,
    PartialFactorSetCUR,
    PartialFactorSetEC,
    PartialFactorSetEC7NADBE,
    PartialFactorSetEC7NADNL,
    PartialFactorSetVerifyEC,
    RiskClassEC7BE,
    VerifyType,
)


class CalculationOptionsPerStage(BaseDataClass):
    """Calculation options are needed when a verification calculation is performed with method B.
    The user can specify a different partial factor set for each of the stages. This input is optional
    when another type of calculation is performed.
    Arguments:
     anchor_factor: multiplication factor for the anchor stiffness.
     partial_factor_set: partial factor sets corresponding to different code annexes.
    """

    anchor_factor: float = 1
    partial_factor_set: (
        PartialFactorSetEC7NADBE | PartialFactorSetCUR | PartialFactorSetEC7NADNL | None
    ) = None


class CalculationOptions(BaseDataClass, metaclass=ABCMeta):
    """Base class for all calculation options.

    Arguments:
     calc_first_stage_initial: This option determines equal neutral stresses at both sides, for initially non-horizontal surfaces or initial surcharges.
     calc_minor_nodes_on: Select either the faster, classic, coarse element determination (False) of active and passive pressures, or the more accurate fine element determination(True).
     calc_reduce_deltas:  Set on True for reduction of the wall friction angles according to CUR 166 for the calculation of the passive earth pressure coefficients of Culmann method.
     input_calculation_type: select the type of calculation that is going to be performed.
     ec7_nl_assessment_type: Select the assessment type for a calculation with EC7-NL. This option is used only by the GUI in User Defined Partial Factors window.

    """

    calc_first_stage_initial: bool = False
    calc_minor_nodes_on: bool = False
    calc_reduce_deltas: bool = False  # editable if C,phi, delta is selected
    input_calculation_type: CalculationType = CalculationType.STANDARD
    is_vibration_calculation: bool = False
    ec7_nl_assessment_type: AssessmentTypeEC7NL = AssessmentTypeEC7NL.NewConstruction

    @property
    def calculation_properties(
        self,
    ) -> (
        "StandardCalculationOptions | DesignSheetpilingLengthCalculationOptions | VerifyCalculationOptions | KranzAnchorStrengthCalculationOptions | OverallStabilityCalculationOptions | ReliabilityAnalysisCalculationOptions"
    ):
        _calculation_properties_map = {
            CalculationType.STANDARD: StandardCalculationOptions,
            CalculationType.DESIGN_SHEETPILING_LENGTH: DesignSheetpilingLengthCalculationOptions,
            CalculationType.VERIFY_SHEETPILING: VerifyCalculationOptions,
            CalculationType.CHARACTERISTIC_KRANZ_ANCHOR_STRENGTH: KranzAnchorStrengthCalculationOptions,
            CalculationType.OVERALL_STABILITY: OverallStabilityCalculationOptions,
            CalculationType.RELIABILITY_ANALYSIS: ReliabilityAnalysisCalculationOptions,
        }
        return _calculation_properties_map[self.input_calculation_type]()


class ReliabilityAnalysisCalculationOptions(CalculationOptions):
    """Reliability analysis calculation selected in Start Calculation
    window."""

    input_calculation_type: CalculationType = CalculationType.RELIABILITY_ANALYSIS


class OverallStabilityCalculationOptions(CalculationOptions):
    """Overall stability calculation selected in Start Calculation window.

    Arguments:
     cur_stability_stage: Id of the stage to be checked. This id refers to D-SheetPiling so the first stage in D-SheetPiling has an input of 0.
     overall_stability_type: which type of calculation is going to be performed
     stability_eurocode_partial_factor_set: partial factor set selected for the EC7 General calculation
     stability_ec7_nl_partial_factor_set: partial factor set selected for the EC7 NL calculation
     stability_ec7_be_partial_factor_set: partial factor set selected for the EC7 BE calculation
     stability_cur_partial_factor_set: partial factor set selected for the CUR calculation
     stability_export: Set on True to generate an input file with STI format which can be opened with D-Geo Stability
    """

    input_calculation_type: CalculationType = CalculationType.OVERALL_STABILITY
    cur_stability_stage: Annotated[int, Field(ge=0)] = 0
    overall_stability_type: DesignType = DesignType.REPRESENTATIVE
    stability_eurocode_partial_factor_set: PartialFactorSetEC = PartialFactorSetEC.DA1SET1
    stability_ec7_nl_partial_factor_set: PartialFactorSetEC7NADNL = (
        PartialFactorSetEC7NADNL.RC0
    )
    overall_stability_ec7_be_partial_factor_set: PartialFactorSetEC7NADBE = (
        PartialFactorSetEC7NADBE.RC1SET1
    )
    stability_cur_partial_factor_set: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI
    stability_export: bool = False


class KranzAnchorStrengthCalculationOptions(CalculationOptions):
    """Kranz anchor strength calculation selected in Start Calculation
    window.

    Arguments:
     cur_anchor_force_stage: Id of the stage to be checked. This id refers to D-SheetPiling so the first stage in D-SheetPiling has an input of 0.
    """

    input_calculation_type: CalculationType = (
        CalculationType.CHARACTERISTIC_KRANZ_ANCHOR_STRENGTH
    )
    cur_anchor_force_stage: Annotated[int, Field(ge=0)] = 0


class StandardCalculationOptions(CalculationOptions):
    """Standard calculation selected in Start Calculation window.

    Arguments:
     calc_auto_lambdas_on: When True Automatic leaves the values of the lateral earth pressure ratios that are calculated by the Culmann (c, phi, delta) method as they are.
    """

    input_calculation_type: CalculationType = CalculationType.STANDARD
    calc_auto_lambdas_on: bool = True


class VerifyCalculationOptions(CalculationOptions):
    """Verify sheet pile calculation selected in Start Calculation window.

    Arguments:
     verify_type: Select partial factor set
     eurocode_partial_factor_set: Select partial factor set
     eurocode_overall_stability: Set to True to perform an overall stability calculation using modified values for soil properties (cohesion, friction angle and unit weight) depending on the Design approach chosen for all stages.
     ec7_nl_method: Select method of calculation according to CUR 166 design procedure
     ec7_nl_overall_partial_factor_set: Select partial factor set
     ec7_nl_overall_anchor_factor: multiplication factor for the anchor stiffness
     ec7_nad_nl_overall_stability: Set to True to perform an overall stability calculation using modified values for soil properties (cohesion, friction angle and unit weight) depending on the Design approach chosen for all stages.
     ec7_be_overall_stability: Set to True to perform an overall stability calculation using modified values for soil properties (cohesion, friction angle and unit weight) depending on the Design approach chosen for all stages.
     ec7_be_method: Select method of calculation for EC7 BE
     ec7_be_overall_risk_class: Select risk class
     cur_method: Select method of calculation according to CUR 166 design procedure
     cur_overall_partial_factor_set: Select partial factor set
     cur_overall_anchor_factor: multiplication factor for the anchor stiffness
     cur_overall_stability: Set to True to perform an overall stability calculation using modified values for soil properties (cohesion, friction angle and unit weight) depending on the Design approach chosen for all stages.
    """

    input_calculation_type: CalculationType = CalculationType.VERIFY_SHEETPILING
    verify_type: VerifyType = VerifyType.CUR
    eurocode_partial_factor_set: PartialFactorSetVerifyEC = PartialFactorSetVerifyEC.DA1
    eurocode_overall_stability: bool = False
    ec7_nl_method: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    ec7_nl_overall_partial_factor_set: PartialFactorSetEC7NADNL = (
        PartialFactorSetEC7NADNL.RC0
    )
    ec7_nl_overall_anchor_factor: Annotated[float, Field(ge=0.001, le=1000)] = 1
    ec7_nad_nl_overall_stability: bool = False
    ec7_be_overall_stability: bool = False
    ec7_be_method: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    ec7_be_overall_risk_class: RiskClassEC7BE = RiskClassEC7BE.RC2
    cur_method: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    cur_overall_partial_factor_set: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI
    cur_overall_anchor_factor: Annotated[float, Field(ge=0.001, le=1000)] = 1
    cur_overall_stability: bool = False

    @property
    def allowable_anchor_force_calculation_type(self) -> bool:
        return (self.verify_type == VerifyType.CUR) or (
            self.verify_type == VerifyType.EC7NL
        )


class DesignSheetpilingLengthCalculationOptions(CalculationOptions):
    """Design sheet pile calculation selected in Start Calculation window.

    Note that design_pile_length can show up as a different value in the GUI
    compared to what's been set in the .shi file.

    Args:
     design_stage: Id of the stage to be checked. This id refers to D-SheetPiling so the first stage in D-SheetPiling has an input of 0.
     design_pile_length_from: The starting point of the pile over which the analysis should be performed.
     design_pile_length_to: The end point of the pile over which the analysis should be performed
     design_pile_length_decrement: the Decrement in length for each analysis step.
     design_type: types of design.
     design_eurocode_partial_factor_set: Select partial factor set
     design_partial_factor_set_ec7_nad_nl: Select partial factor set
     design_ec7_nl_method: Select method of calculation according to CUR 166 design procedure
     design_ec7_be_partial_factor_set: Select partial factor set
     design_ec7_be_method: Select method of calculation according to CUR 166 design procedure
     design_partial_factor_set: Select partial factor set
     design_cur_method: Select method of calculation according to CUR 166 design procedure
    """

    input_calculation_type: CalculationType = CalculationType.DESIGN_SHEETPILING_LENGTH
    design_stage: Annotated[int, Field(ge=0)] = 0
    design_pile_length_from: Annotated[float, Field(ge=1, le=100)] = 1
    design_pile_length_to: Annotated[float, Field(ge=1, le=100)] = 1
    design_pile_length_decrement: Annotated[float, Field(ge=0.01, le=10)] = 0.01
    design_type: DesignType = DesignType.REPRESENTATIVE
    design_eurocode_partial_factor_set: PartialFactorSetEC = PartialFactorSetEC.DA1SET1
    design_partial_factor_set_ec7_nad_nl: PartialFactorSetEC7NADNL = (
        PartialFactorSetEC7NADNL.RC0
    )
    design_ec7_nl_method: PartialFactorCalculationType = (
        PartialFactorCalculationType.METHODA
    )
    design_ec7_be_partial_factor_set: PartialFactorSetEC7NADBE = (
        PartialFactorSetEC7NADBE.RC1SET1
    )
    design_ec7_be_method: PartialFactorCalculationType = (
        PartialFactorCalculationType.METHODA
    )
    design_partial_factor_set: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI
    design_cur_method: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
