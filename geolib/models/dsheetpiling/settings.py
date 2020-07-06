from enum import Enum, IntEnum


class LateralEarthPressureMethod(IntEnum):
    """The method for input of the lateral earth pressure ratio"""

    MIXED = 0
    KA_KO_KP = 1
    C_PHI_DELTA = 2


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
    """" Calculation type for D-SheetPiling"""

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


class EuroCodePartialFactorSet(IntEnum):
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


class DesignPartialFactorSet(IntEnum):
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


class VerifyEurocodePartialFactorSet(IntEnum):
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
    BRINCHHANSEN = 0
    MANUAL = 1


class LambdaType(IntEnum):
    MANUAL = 0
    MULLERBRESLAU = 1
    KOTTER = 2


class HorizontalBehaviorType(IntEnum):
    STIFF = 1
    ELASTIC = 2
    FOUNDATION = 3

