from enum import Enum, IntEnum

from pydantic import conint

from geolib.models import BaseDataClass


class LateralEarthPressureMethod(IntEnum):
    """The method for input of the lateral earth pressure ratio"""

    MIXED = 2
    KA_KO_KP = 0
    C_PHI_DELTA = 1


class LateralEarthPressureMethodStage(IntEnum):
    """The method for input of the lateral earth pressure ratio"""

    KA_KO_KP = 1
    C_PHI_DELTA = 2

    @staticmethod
    def get_stage_type_from_method(method_value: LateralEarthPressureMethod,):
        pair_dictionary = {
            LateralEarthPressureMethod.KA_KO_KP: LateralEarthPressureMethodStage.KA_KO_KP,
            LateralEarthPressureMethod.C_PHI_DELTA: LateralEarthPressureMethodStage.C_PHI_DELTA,
        }
        return pair_dictionary.get(method_value)


class ModelType(IntEnum):
    """Represents the model types from D-Sheet Piling using the same integer values used in the application.

    The Model type determines the kind of calculation that's performed on the construction.
    """

    SHEET_PILING = 0
    SINGLE_PILE = 1
    DIAPHRAGM_WALL = 2


class SinglePileLoadOptions(Enum):
    """Load options for the Single Pile"""

    LOADED_BY_FORCES = "forces"
    LOADED_BY_USER_DEFINED_DISPLACEMENTS = "user_defined_displacements"
    LOADED_BY_CALCULATED_DISPLACEMENTS = "calculated_displacements"


class PassiveSide(IntEnum):
    """Class to determine passive side."""

    DSHEETPILING_DETERMINED = 0
    LEFT = 1
    RIGHT = 2


class DistributionType(IntEnum):
    """Distribution type for probability analysis"""

    NONE = 0
    UNIFORM = 1
    NORMAL = 2
    LOG_NORMAL = 3
    EXPONENTIAL = 4


class Side(IntEnum):
    """Defines the two sides of a wall"""

    LEFT = 1
    RIGHT = 2
    BOTH = 3


class SheetPilingElementMaterialType(IntEnum):
    """Materials settings for sheet pile elements"""

    UserDefined = 0
    Steel = 1
    Concrete = 2
    # This is not implemented in the UI but it is possible input in the D-Series code
    Wood = 3
    Synthetic = 4
    Combined = 5


class CalculationType(IntEnum):
    """ Calculation type for D-SheetPiling"""

    STANDARD = 0
    DESIGN_SHEETPILING_LENGTH = 1
    VERIFY_SHEETPILING = 2
    CHARACTERISTIC_KRANZ_ANCHOR_STRENGTH = 3
    OVERALL_STABILITY = 4
    RELIABILITY_ANALYSIS = 5


class DesignType(IntEnum):
    REPRESENTATIVE = 0
    CUR = 1
    EC7GENERAL = 2
    EC7NL = 3
    EC7BE = 4
    UNKNOWN = 5  # option is not available for the latest version of D-Sheet piling


class PartialFactorSetEC(IntEnum):
    DA1SET1 = 0
    DA1SET2 = 1
    DA2 = 2
    DA3 = 3


class PartialFactorSetEC7NADNL(IntEnum):
    RC0 = 0
    RC1 = 1
    RC2 = 2
    RC3 = 3


class PartialFactorSetEC7NADB(IntEnum):
    SET1 = 0
    SET2 = 1


class PartialFactorSetCUR(IntEnum):
    UNKNOWN = -1
    CLASSI = 0
    CLASSII = 1
    CLASSIII = 2


class PartialFactorCalculationType(IntEnum):
    METHODA = 0
    METHODB = 1


class VerifyType(IntEnum):
    CUR = 0
    EC7GENERAL = 1
    EC7NL = 2
    EC7BE = 3
    UNKNOWN = 4


class PartialFactorSetVerifyEC(IntEnum):
    DA1 = 0
    DA2 = 1
    DA3 = 2


class SoilTypeModulusSubgradeReaction(IntEnum):
    GRAVEL = 0
    SAND = 1
    LOAM = 2
    CLAY = 3
    PEAT = 4


class GrainType(IntEnum):
    FINE = 0
    COARSE = 1


class ModulusSubgradeReaction(IntEnum):
    MENARD = 0
    MANUAL = 1


class EarthPressureCoefficients(IntEnum):
    MANUAL = 0
    BRINCHHANSEN = 1


class LambdaType(IntEnum):
    MANUAL = 0
    MULLERBRESLAU = 1
    KOTTER = 2


class HorizontalBehaviorType(IntEnum):
    STIFF = 1
    ELASTIC = 2
    FOUNDATION = 3


class ModulusReactionType(Enum):
    """
    The Secant definition is based on the stress-displacement diagram according to CUR 166 of subgrade reaction.
    This diagram always uses three branches, with intersections at 50, 80 and 100 % of Ka−Kp
    The slope of the different branches is defined indirectly, via the three secant moduli at the intersection points.

    The Tangent (D-SheetPiling Classic) definition is based on a user-defined number of branches (number of curves),
    with the slope  of  each  branch  defined  directly  by  the  tangent  modulus
    """

    TANGENT = 0
    SECANT = 1


class CurveSettings(BaseDataClass):
    modulus_reaction_type: ModulusReactionType = ModulusReactionType.SECANT
    use_unloading_reloading_curve: bool = False
    curve_number: conint(ge=1, le=4) = 3


class LoadTypeFavourableUnfavourable(IntEnum):
    DSHEETPILING_DETERMINED = 0
    FAVOURABLE = 1
    UNFAVOURABLE = 2


class LoadTypeFavourableUnfavourableMoment(IntEnum):
    FAVOURABLE = 1
    UNFAVOURABLE = 2


class LoadTypePermanentVariable(IntEnum):
    PERMANENT = 0
    VARIABLE = 1
