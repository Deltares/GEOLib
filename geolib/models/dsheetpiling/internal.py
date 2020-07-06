import logging
import warnings
from abc import ABCMeta
from enum import Enum, IntEnum
from inspect import cleandoc
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from pydantic import BaseModel as DataClass
from pydantic import PositiveFloat, confloat, conint, constr, conlist

import geolib.models.dsheetpiling.constructions as constructions
from geolib.geometry import Point
from geolib.models.dseries_parser import (
    DSeriesStructure,
    DSeriesStructureCollection,
    DSeriesNoParseSubStructure,
    DSerieListStructure,
    DSeriesInlineMappedProperties,
    DSeriesUnmappedNameProperties,
)

from .calculation_options import (
    CalculationOptionsPerStage as CalculationOptionsPerStageExternal,
)
from .dsheetpiling_structures import (
    DSeriesPilingDumpParserStructure,
    DSeriesPilingParserStructure,
    DSheetpilingSurchargeLoad,
)
from .dsheetpiling_validator import DSheetPilingValidator
from .internal_partial_factors import (
    PartialFactorsCurI,
    PartialFactorsCurIi,
    PartialFactorsCurIii,
    PartialFactorsEc7BSet1,
    PartialFactorsEc7BSet2,
    PartialFactorsEc7Nl0,
    PartialFactorsEc7Nl1,
    PartialFactorsEc7Nl2,
    PartialFactorsEc7Nl3,
    PartialFactorsEc7SeVk1,
    PartialFactorsEc7SeVk2,
    PartialFactorsEc7SeVk3,
    PartialFactorsEurocodeDa1Set1,
    PartialFactorsEurocodeDa1Set2,
    PartialFactorsEurocodeDa2,
    PartialFactorsEurocodeDa3,
)
from .settings import (
    CalculationType,
    DesignPartialFactorSet,
    DesignType,
    DistributionType,
    EuroCodePartialFactorSet,
    LateralEarthPressureMethod,
    ModelType,
    PartialFactorCalculationType,
    PartialFactorSetEC7NADB,
    PartialFactorSetEC7NADNL,
    PassiveSide,
    SheetPilingElementMaterialType,
    Side,
    SoilTypeModulusSubgradeReaction,
    GrainType,
    ModulusSubgradeReaction,
    EarthPressureCoefficients,
    SinglePileLoadOptions,
    VerifyEurocodePartialFactorSet,
    VerifyType,
    LambdaType,
    HorizontalBehaviorType,
)
from .dsheetpiling_validator import DSheetPilingValidator

_DEFAULT_WATER_LEVEL_NAME: str = "New Water Level"
_DEFAULT_SURFACE_NAME: str = "New Surface"
_DEFAULT_UNIT_WEIGHT_WATER: float = 9.81
_DEFAULT_PRE_STRESS: float = 0.0

_DEFAULT_SOIL_VERSION = 1007
_DEFAULT_SHEETPILING_VERSION = 1026


class Model(DSeriesNoParseSubStructure):
    model: ModelType = ModelType.SHEET_PILING
    method: LateralEarthPressureMethod = LateralEarthPressureMethod.MIXED
    verification: bool = False
    ec7se_visible: bool = False
    pile_load_option: SinglePileLoadOptions = SinglePileLoadOptions.LOADED_BY_FORCES
    probabilistic: bool = False
    check_vertical_balance: bool = True
    trildens_calculation: bool = True
    diepwand_calculation: bool = False
    elastic_calculation: bool = True
    wooden_sheetpiling: bool = False


class Version(DSeriesInlineMappedProperties):
    soil: int = _DEFAULT_SOIL_VERSION
    d__sheet_piling: int = _DEFAULT_SHEETPILING_VERSION

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.soil < _DEFAULT_SOIL_VERSION
            or self.d__sheet_piling < _DEFAULT_SHEETPILING_VERSION
        ):
            logging.warning(f"This version of input files are unsupported.")


class VersionExternals(DSeriesInlineMappedProperties):
    dgscptipcalc____dll: str = "19.1.1.23469"
    dgscptipui____dll: str = "19.1.1.23469"


class Soil(DSeriesUnmappedNameProperties):
    name: str = "default soil"
    soilcolor: int = 9764853
    soilsoiltype: SoilTypeModulusSubgradeReaction = SoilTypeModulusSubgradeReaction.SAND
    soilgraintype: GrainType = GrainType.FINE
    soilgamdry: confloat(ge=0, le=100) = 0.01
    soilgamwet: confloat(ge=0, le=100) = 0.01
    soilrelativedensity: confloat(ge=0, le=100) = 0
    soilemodmenard: confloat(ge=0.01, le=1000000) = 0.01
    soilcohesion: confloat(ge=0, le=1000000000) = 0
    soilphi: confloat(ge=-89, le=89) = 0
    soildelta: confloat(ge=0, le=89) = 0.00
    soilcutop: float = 0  # fixed value
    soilcubottom: float = 0  # fixed value
    soilcubearingcapacityfactor: float = 4.10  # fixed value
    soilocr: confloat(ge=0, le=1000) = 1.00
    soildrained: int = 0  # fixed value
    soilpermeabkx: confloat(ge=0.00000000001, le=1000000) = 0.0001
    soilstdcohesion: confloat(ge=0, le=100000000) = 0.00
    soilstdphi: confloat(ge=0, le=100000000) = 0.00
    soildistcohesion: DistributionType = DistributionType.NONE
    soildistphi: DistributionType = DistributionType.NONE
    soilla: confloat(ge=0, le=1000) = 0
    soilln: confloat(ge=0, le=1000) = 0.01
    soillp: confloat(ge=0, le=1000) = 0.01
    soilusemenard: ModulusSubgradeReaction = ModulusSubgradeReaction.MANUAL
    soilusebrinchhansen: EarthPressureCoefficients = EarthPressureCoefficients.MANUAL
    soilshellfactor: confloat(ge=1, le=1000) = 1.00
    soillambdatype: LambdaType = LambdaType.MANUAL
    soillam1: confloat(ge=0, le=100) = 50
    soillam2: confloat(ge=0, le=100) = 80
    soillam3: confloat(ge=0, le=100) = 90
    soilkb0: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilkb1: confloat(ge=0.01, le=10000000000) = 5.00000e00
    soilkb2: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilkb3: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilkb4: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilko0: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilko1: confloat(ge=0.01, le=10000000000) = 5.00000e00
    soilko2: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilko3: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilko4: confloat(ge=0.01, le=10000000000) = 1.00000e04
    soilcurkb1: confloat(ge=0.01, le=10000000000) = 2.00000e03
    soilcurkb2: confloat(ge=0.01, le=10000000000) = 8.00000e02
    soilcurkb3: confloat(ge=0.01, le=10000000000) = 5.00000e02
    soilcurko1: confloat(ge=0.01, le=10000000000) = 2.00000e03
    soilcurko2: confloat(ge=0.01, le=10000000000) = 8.00000e02
    soilcurko3: confloat(ge=0.01, le=10000000000) = 5.00000e02
    soilhorizontalbehaviourtype: HorizontalBehaviorType = HorizontalBehaviorType.ELASTIC
    soilelasticity: float = 1.00000e03  # fixed value
    soildefaultelasticity: int = 1  # fixed value


class SoilCollection(DSeriesStructureCollection):
    soil: List[Soil] = []

    def add_soil_if_unique(self, soil) -> None:
        for added_soil in self.soil:
            if soil.name == added_soil.name:
                raise NameError(f"Soil with name {soil.name} already exists.")
        self.soil.append(soil)
        return soil

    def find_soil_id(self, key) -> int:
        for i, soil in enumerate(self.soil):
            if soil.name == key:
                return i
        raise KeyError(f"Soil with {key} not present.")

    def __getitem__(self, key) -> Soil:
        if isinstance(key, int):
            return self.soil[key]
        elif isinstance(key, str):
            for soil in self.soil:
                if soil.name == key:
                    return soil
            raise KeyError(key)


class CalculationOptions(DSeriesStructure):
    # TODO these first values are not used for single pile
    calcfirststageinitial: bool = False
    calcminornodeson: bool = False
    calcreducedeltas: bool = False
    calcempiricalfactorstresstype: int = 0  # fixed value
    inputcalculationtype: CalculationType = CalculationType.STANDARD
    isvibrationcalculation: bool = False
    allowableanchorforcecalculationtype: bool = False
    # available when c, phi , delta is selected for as a model
    calcautolambdason: bool = True
    # design sheet pile length calculation
    designstage: conint(ge=0) = 0
    designpilelengthfrom: confloat(ge=1, le=100) = 1
    designpilelengthto: confloat(ge=1, le=100) = 1
    designpilelengthdecrement: confloat(ge=0.01, le=10) = 0.01
    designpilelengthnew: int = 1  # fixed value
    designtype: DesignType = DesignType.REPRESENTATIVE
    designeurocodepartialfactorset: EuroCodePartialFactorSet = EuroCodePartialFactorSet.DA1SET1
    designpartialfactorsetec7nadnl: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    designec7nlmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designpartialfactorsetec7nadb: PartialFactorSetEC7NADB = PartialFactorSetEC7NADB.SET1
    designec7bmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designpartialfactorset: DesignPartialFactorSet = DesignPartialFactorSet.CLASSI
    designcurmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designpartialfactorsetec7nadse: int = 0  # fixed value
    designec7semethod: int = 0  # fixed value
    # verify sheet piling calculation
    verifytype: VerifyType = VerifyType.CUR
    eurocodepartialfactorset: VerifyEurocodePartialFactorSet = VerifyEurocodePartialFactorSet.DA1
    eurocodeoverallstability: bool = False
    ec7nlmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    ec7nloverallpartialfactorset: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    ec7nloverallanchorfactor: confloat(ge=0.001, le=1000) = 1
    ec7nadnloverallstability: bool = False
    ec7boverallstability: bool = False
    nbmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    curmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    curoverallpartialfactorset: DesignPartialFactorSet = DesignPartialFactorSet.CLASSI
    curoverallanchorfactor: confloat(ge=0.001, le=1000) = 1
    curoverallstability: bool = False
    ec7semethod: int = 0  # fixed value
    ec7seoverallpartialfactorset: int = 0  # fixed value
    ec7nadseoverallstability: int = 0  # fixed value
    # Characteristic Kranz Anchor Strength calculation
    curanchorforcestage: conint(ge=0) = 0
    # Overall stability calculation
    curstabilitystage: conint(ge=0) = 0
    overallstabilitytype: DesignType = DesignType.REPRESENTATIVE
    stabilityeurocodepartialfactorset: EuroCodePartialFactorSet = EuroCodePartialFactorSet.DA1SET1
    stabilityec7nlpartialfactorset: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    stabilityec7bpartialfactorset: PartialFactorSetEC7NADB = PartialFactorSetEC7NADB.SET1
    stabilitycurpartialfactorset: DesignPartialFactorSet = DesignPartialFactorSet.CLASSI
    stabilityec7separtialfactorset: int = 0  # fixed value
    overallstabilitydrained: int = 1  # fixed value

    # These are all subgroups (key=value)
    partial_factors_eurocode_da1_set1: PartialFactorsEurocodeDa1Set1 = PartialFactorsEurocodeDa1Set1()
    partial_factors_eurocode_da1_set2: PartialFactorsEurocodeDa1Set2 = PartialFactorsEurocodeDa1Set2()
    partial_factors_eurocode_da2: PartialFactorsEurocodeDa2 = PartialFactorsEurocodeDa2()
    partial_factors_eurocode_da3: PartialFactorsEurocodeDa3 = PartialFactorsEurocodeDa3()
    partial_factors_ec7_nl_0: PartialFactorsEc7Nl0 = PartialFactorsEc7Nl0()
    partial_factors_ec7_nl_1: PartialFactorsEc7Nl1 = PartialFactorsEc7Nl1()
    partial_factors_ec7_nl_2: PartialFactorsEc7Nl2 = PartialFactorsEc7Nl2()
    partial_factors_ec7_nl_3: PartialFactorsEc7Nl3 = PartialFactorsEc7Nl3()
    partial_factors_ec7_b_set1: PartialFactorsEc7BSet1 = PartialFactorsEc7BSet1()
    partial_factors_ec7_b_set2: PartialFactorsEc7BSet2 = PartialFactorsEc7BSet2()
    partial_factors_cur_i: PartialFactorsCurI = PartialFactorsCurI()
    partial_factors_cur_ii: PartialFactorsCurIi = PartialFactorsCurIi()
    partial_factors_cur_iii: PartialFactorsCurIii = PartialFactorsCurIii()
    partial_factors_ec7_se_vk1: PartialFactorsEc7SeVk1 = PartialFactorsEc7SeVk1()
    partial_factors_ec7_se_vk2: PartialFactorsEc7SeVk2 = PartialFactorsEc7SeVk2()
    partial_factors_ec7_se_vk3: PartialFactorsEc7SeVk3 = PartialFactorsEc7SeVk3()


class SheetPileElement(DSeriesUnmappedNameProperties):
    name: constr(min_length=1, max_length=50) = " "
    sheetpilingelementmaterialtype: SheetPilingElementMaterialType = SheetPilingElementMaterialType.Steel
    sheetpilingelementei: confloat(ge=0.001, le=1e12) = 100000
    sheetpilingelementwidth: confloat(ge=0, le=1000) = 1
    sheetpilingelementlevel: confloat(ge=-10000, le=10000) = -10
    sheetpilingelementheight: confloat(ge=10, le=100000) = 400
    sheetpilingelementcoatingarea: confloat(ge=0.01, le=10) = 1.35
    sheetpilingpilewidth: confloat(ge=0, le=100000) = 0
    sheetpilingelementsectionarea: confloat(ge=10, le=100000) = 170
    sheetpilingelementresistingmoment: confloat(ge=0, le=100000) = 0
    sheetpilingelementreductionfactorei: confloat(ge=0.01, le=10) = 1
    sheetpilingelementnote: constr(min_length=0, max_length=20) = ""
    sheetpilingelementmaxcharacteristicmoment: confloat(ge=0, le=100000) = 0
    sheetpilingelementmaxplasticcharacteristicmoment: confloat(ge=0, le=100000) = 0
    sheetpilingelementkmod: confloat(ge=0.01, le=1) = 0.01
    sheetpilingelementmaterialfactor: confloat(ge=0.01, le=10) = 0.01
    ssheetpilingelementreductionfactormaxmoment: confloat(ge=0.01, le=10) = 1
    diaphragmwallissymmetric: confloat(ge=0, le=1) = 0
    diaphragmwallposeielastoplastic1: confloat(ge=0, le=100000) = 0
    diaphragmwallnegeielastoplastic1: confloat(ge=0, le=100000) = 0
    diaphragmwallposmomelastic: confloat(ge=0, le=1000000000000) = 100000
    diaphragmwallnegmomelastic: confloat(ge=0, le=100000) = 0
    diaphragmwallposmomplastic: confloat(ge=0, le=100000) = 0
    diaphragmwallnegmomplastic: confloat(ge=0, le=100000) = 0
    diaphragmwallposeielastoplastic2: confloat(ge=0, le=100000) = 0
    diaphragmwallposmomelastoplastic: confloat(ge=0, le=100000) = 0
    diaphragmwallnegeielastoplastic2: confloat(ge=0, le=100000) = 0
    diaphragmwallnegmomelastoplastic: confloat(ge=0, le=100000) = 0
    woodensheetpilingelemente: confloat(ge=0.001, le=1000000000000) = 100000
    woodensheetpilingelementcharacflexuralstrength: confloat(ge=0, le=100000) = 0
    woodensheetpilingelementksys: confloat(ge=0.01, le=10) = 1.15
    woodensheetpilingelementkdef: confloat(ge=0.01, le=10) = 1
    woodensheetpilingelementpsi2eff: confloat(ge=0, le=10) = 1
    woodensheetpilingelementmaterialfactor: confloat(ge=0.01, le=10) = 1.3
    woodensheetpilingelementkmodfshort: confloat(ge=0.01, le=10) = 0.65
    woodensheetpilingelementkmodflong: confloat(ge=0.01, le=10) = 0.5
    woodensheetpilingelementkmode: confloat(ge=0.01, le=10) = 0.8

    def __init__(self, *args, **kwargs) -> "SheetPileElement":
        default_dict = dict(self.__fields__)
        for field, value in kwargs.items():
            if value is None:
                kwargs[field] = default_dict[field].default
        super().__init__(*args, **kwargs)

    def update_arguments_if_invalid_input(self) -> None:
        """This function updates sheetpilingelementkmod and
        result_dict_gamma_m_value according to the
        sheetpilingelementmaterialtype inputed by the user.

        For some types the user can define their own parameters and for
        some others default values are defined.
        """
        # k-mod value
        result_dict_k_mod_value = {
            0: self.sheetpilingelementkmod,
            1: 1.0,
            2: 1.0,
            3: 1.0,
            4: self.sheetpilingelementkmod,
            5: self.sheetpilingelementkmod,
        }
        if (
            self.sheetpilingelementkmod
            is not result_dict_k_mod_value[self.sheetpilingelementmaterialtype.value]
        ):
            self.sheetpilingelementkmod = result_dict_k_mod_value[
                self.sheetpilingelementmaterialtype.value
            ]
            warnings.warn(
                "Inputed value for kmod was not valid and was change to "
                + str(self.sheetpilingelementkmod),
                ImportWarning,
            )
        # gammma_m value
        result_dict_gamma_m_value = {
            0: self.sheetpilingelementmaterialfactor,
            1: 1.0,
            2: 1.1,
            3: 1.0,
            4: 1.2,
            5: self.sheetpilingelementmaterialfactor,
        }
        if (
            self.sheetpilingelementmaterialfactor
            is not result_dict_gamma_m_value[self.sheetpilingelementmaterialtype.value]
        ):
            self.sheetpilingelementmaterialfactor = result_dict_gamma_m_value[
                self.sheetpilingelementmaterialtype.value
            ]
            warnings.warn(
                "Inputed value for material factor was not valid and was change to "
                + str(self.sheetpilingelementmaterialfactor),
                ImportWarning,
            )


class SheetPiling(DSeriesStructureCollection):
    sheetpiling: List[SheetPileElement] = []
    leveltopsheetpiling: confloat(ge=-10000, le=10000) = None
    lengthsheetpiling: confloat(gt=0) = None

    def update_length_of_sheet_pile(self):
        """The length should be finally calculated as the distance between the
        toplevel and the Section bottom level."""
        # last element appended will define the length of the sheet pile
        newlevel = self.sheetpiling[-1].sheetpilingelementlevel
        # check that this is the shallowest level. If not raise error
        for element in range(len(self.sheetpiling)):
            if newlevel > self.sheetpiling[element].sheetpilingelementlevel:
                raise ValueError(
                    "Value not strictly decreasing for element "
                    + self.sheetpiling[-1].name
                )
        self.lengthsheetpiling = self.leveltopsheetpiling - newlevel
        self.lengthsheetpiling = self.leveltopsheetpiling - newlevel

    def update_level_top_sheet_pile(self, top_level: Union[Point, Any]):
        """ Updates level if the level is not defined. Should inform the user if the top is not defined."""
        # user has inputted a value
        if top_level:
            # user has arleady defined this value this should be done only once
            if self.leveltopsheetpiling:
                raise Exception("Top pile level was arleady determined.")
            # the value is not defined and the user is defining it for the first time
            else:
                self.leveltopsheetpiling = top_level.y
        else:
            if not (self.leveltopsheetpiling):
                # User did not make an effort to define the value needed
                raise Exception("Top pile level should be defined.")


class Anchor(DSeriesNoParseSubStructure):
    name: constr(min_length=1, max_length=50)
    level: float = 0
    e_modulus: confloat(gt=0) = 2.1e8
    cross_section: Optional[confloat(gt=0)] = 1e-3
    wall_height_kranz: Optional[confloat(gt=0)] = 0.00
    length: Optional[confloat(gt=0)] = 1
    angle: Optional[confloat(gt=0)] = 0.00
    yield_force: Optional[confloat(gt=0)] = 0.00
    side: Side = Side.RIGHT


class Anchors(DSerieListStructure):
    """Container for Anchor"""

    anchors: List[Anchor] = []

    @property
    def anchor_names(self) -> Set[str]:
        return {anchor.name for anchor in self.anchors}


class AnchorOrStrutPresstressReference(DataClass):
    """Used in the ConstructionStage to identify anchor and assign a prestress"""

    name: str
    pre_stress: confloat(ge=0) = _DEFAULT_PRE_STRESS


class Strut(DSeriesNoParseSubStructure):
    name: constr(min_length=1, max_length=50)
    level: float = 0
    e_modulus: confloat(gt=0) = 2.1e8
    cross_section: Optional[confloat(gt=0)] = 1e-4
    length: Optional[confloat(gt=0)] = 1
    angle: Optional[confloat(gt=0)] = 0.00
    buckling_force: Optional[confloat(gt=0)] = 0.00
    side: Side = Side.RIGHT


class Struts(DSerieListStructure):
    """Container for Strut"""

    struts: List[Strut] = []

    @property
    def strut_names(self) -> Set[str]:
        return {strut.name for strut in self.struts}


class ConstructionStage(DSeriesUnmappedNameProperties):
    name: constr(min_length=1, max_length=50)
    displacement_top_sheet_piling: float = 0
    passive_side: PassiveSide = PassiveSide.DSHEETPILING_DETERMINED
    method_left: LateralEarthPressureMethod = LateralEarthPressureMethod.KA_KO_KP
    method_right: LateralEarthPressureMethod = LateralEarthPressureMethod.KA_KO_KP
    water_level_left: str = _DEFAULT_WATER_LEVEL_NAME
    water_level_right: str = _DEFAULT_WATER_LEVEL_NAME
    head_level: Optional[float] = None
    surface_left: str = _DEFAULT_SURFACE_NAME
    surface_right: str = _DEFAULT_SURFACE_NAME
    soil_profile_left: Optional[List] = None
    soil_profile_right: Optional[List] = None
    anchors: List[AnchorOrStrutPresstressReference] = []
    struts: List[AnchorOrStrutPresstressReference] = []
    spring_supports: List = []
    rigid_supports: List = []
    uniform_loads: List = []
    surcharge_loadss_left: List = []
    surcharge_loadss_right: List = []
    horizontal_line_loads: List = []
    moment_loads: List = []
    normal_forces: List = []


class ConstrutionStages(DSeriesStructureCollection):
    stages: List[ConstructionStage] = []

    @property
    def stage_names(self) -> Set[str]:
        return {stage.name for stage in self.stages}


class WaterLevel(DSeriesNoParseSubStructure):
    name: constr(min_length=1, max_length=50)
    level: float
    distribution_type: DistributionType = DistributionType.NONE
    standard_deviation: float = 0.0


class WaterLevels(DSeriesNoParseSubStructure):
    levels: List[WaterLevel] = []

    @property
    def water_level_names(self) -> Set[str]:
        return {water_level.name for water_level in self.levels}


class StageOptions(DSeriesInlineMappedProperties):
    """ Representation of [STAGE] block."""

    stagepartialfactorsetcur: DesignPartialFactorSet = DesignPartialFactorSet.UNKNOWN
    stageverify: int = 0
    stageanchorfactor: confloat(ge=0.001, le=1000) = 1
    stagepartialfactorsetec7nadnl: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    stageverifyec7nadnl: int = 0
    stageanchorfactorec7nadnl: confloat(ge=0.001, le=1000) = 1
    stageverifyec7nadb: int = 0
    stagepartialfactorsetec7nadse: int = 0  # fixed value
    stageverifyec7nadse: int = 0  # fixed value


class CalculationOptionsPerStage(DSeriesStructureCollection):
    """ Representation of [CALCULATION OPTIONS PER STAGE] block."""

    stageoptions: List[StageOptions] = [StageOptions()]


class UniformLoad(DSeriesUnmappedNameProperties):
    name: str
    uniformloadleft: float
    uniformloadright: float
    uniformloadpermanent: float
    uniformloadfavourable: float
    uniformloadstandarddeviationleft: float
    uniformloadstandarddeviationright: float
    uniformloaddistleft: int
    uniformloaddistright: int


class UniformLoads(DSeriesStructureCollection):
    loads: List[UniformLoad] = []


class SurchargePoint(DSeriesInlineMappedProperties):
    surchargeloaddistance: float
    surchargeloadvalue: float


class SurchargeLoad(DSheetpilingSurchargeLoad):
    name: str = ""
    points: List[SurchargePoint] = []
    surchargeloadpermanent: int
    surchargeloadfavourable: int
    surchargeloadstandarddeviation: float
    surchargeloaddistribution: int


class SurchargeLoads(DSeriesStructureCollection):
    loads: List[SurchargeLoad] = []


class Surface(DSeriesNoParseSubStructure):  # TODO determine structure
    name: constr(min_length=1, max_length=50)
    points: conlist(Point, min_items=1)
    points: conlist(dict, min_items=1)
    distribution_type: DistributionType = DistributionType.NONE
    std: confloat(ge=0.0) = 0.0


class Surfaces(DSeriesNoParseSubStructure):  # TODO GroupList should be suitable?
    surfaces: List[Surface] = []

    @property
    def surface_names(self) -> Set[str]:
        return {surface.name for surface in self.surfaces}


class DSheetPilingInputStructure(DSeriesStructure):
    """Representation of complete .shi file."""

    soil_collection: SoilCollection = SoilCollection()
    run_identification: str = ""
    model: Union[str, Model] = Model()
    cpt_list: str = cleandoc(
        """
        [CPT LIST]
        Count=0
        [END OF CPT LIST]
        """
    )
    sheet_piling: Union[str, SheetPiling] = SheetPiling()
    combined_wall: str = ""
    vertical_balance: str = ""
    settlement_by_vibration_params: str = ""
    horizontal_line_loads: Optional[str] = ""
    uniform_loads: Optional[UniformLoads] = None
    surcharge_loads: Optional[SurchargeLoads] = None
    water: str = ""
    earth_quake: str = ""
    soil_profiles: str = ""
    surfaces: Union[str, Surfaces] = cleandoc(
        f"""
        [SURFACES]
        1 Number of surfaces 
        1     1 {_DEFAULT_SURFACE_NAME}
        0.00  Standard deviation
        2  Distribution type
        Nr     X-coord     Value
        1       0.00       0.00
        [END OF SURFACES]
        """
    )
    water: str = f"  {_DEFAULT_UNIT_WEIGHT_WATER}  Unit weight of water"
    waterlevels: Union[WaterLevels, str] = cleandoc(
        f"""
          1 Number of Waterlevels 
          3 Number of Data per Waterlevel 
        {_DEFAULT_WATER_LEVEL_NAME}
              0.00
              0.00
                 2

        """
    )
    construction_stages: Union[str, ConstrutionStages] = ""
    calculation_options_per_stage: CalculationOptionsPerStage = CalculationOptionsPerStage()
    calculation_options: CalculationOptions = CalculationOptions()
    probabilistic_calculation_options: str = cleandoc(
        """
        [PROBABILISTIC CALCULATION OPTIONS]
        ZFunctionType=1
        ZFunctionMobilisation=100.00
        ZFunctionMoment=0.00
        ZFunctionAnchorForce=0.00
        ZFunctionAnchor=-1
        [END OF PROBABILISTIC CALCULATION OPTIONS]
        """
    )
    probabilistic_control_parameters: str = cleandoc(
        """
        [PROBABILISTIC CONTROL PARAMETERS]
        IterationFactor=1.000
        IterationNumber=15
        CriteriaLimit1=0.010000
        CriteriaLimit2=0.010000
        ReliabilityStage=0
        [END OF PROBABILISTIC CONTROL PARAMETERS]
        """
    )

    # TODO Check these fields whether they have to occur or not
    soil_displacements: Optional[str]
    rigid_supports: Optional[str]
    spring_supports: Optional[str]

    anchors: Union[
        str, Anchors, None
    ] = None  # When no anchors in the model, this block is not present in the .shi file.
    struts: Union[
        str, Struts, None
    ] = None  # When no struts in the model, this block is not present in the .shi file.

    @property
    def is_valid(self) -> bool:
        return self._validator().is_valid

    def has_stage(self, stage_id: int) -> bool:
        try:
            self.construction_stages.stages[stage_id]
            return True
        except IndexError:
            return False

    def _validator(self) -> DSheetPilingValidator:
        return DSheetPilingValidator(self)

    def set_model(self, **kwargs) -> None:
        kwargs = self._filter_none_values_from_key_value_dict(kwargs)
        self.model = Model(**kwargs)

        # TODO Singlepile model is a won't have, raise error here?

        if self.model.method != LateralEarthPressureMethod.MIXED:
            for stage in self.construction_stages.stages:
                stage.method_left = self.model.method
                stage.method_right = self.model.method

    def set_calculation_options(self, **kwargs) -> None:
        kwargs = self._filter_none_values_from_key_value_dict(kwargs)
        # here add function that turns kwargs from snake case to pascal case
        kwargs = self._from_snake_to_pascal_case(kwargs)
        self.calculation_options = CalculationOptions(**kwargs)

    def add_calculation_options_per_stage(
        self, input_calc_options: CalculationOptionsPerStageExternal, stage_id: int,
    ) -> None:
        _map_external_to_internal_values = {
            VerifyType.CUR: {
                "stagepartialfactorsetcur": input_calc_options.partial_factor_set,
                "stageverify": stage_id,
                "stageanchorfactor": input_calc_options.anchor_factor,
            },
            VerifyType.EC7NL: {
                "stagepartialfactorsetec7nadnl": input_calc_options.partial_factor_set,
                "stageverifyec7nadnl": stage_id,
                "stageanchorfactorec7nadnl": input_calc_options.anchor_factor,
            },
            VerifyType.EC7BE: {"stageverifyec7nadb": stage_id},
        }
        stageoptions = StageOptions(
            **_map_external_to_internal_values[self.calculation_options.verifytype]
        )
        self.calculation_options_per_stage.stageoptions[stage_id] = stageoptions

    def add_stage(
        self,
        name: str,
        pile_top_displacement: Optional[float],
        passive_side: Optional[PassiveSide],
        method_left: Optional[LateralEarthPressureMethod],
        method_right: Optional[LateralEarthPressureMethod],
    ) -> None:
        if isinstance(self.construction_stages, str):
            self.construction_stages = ConstrutionStages()
        if name in self.construction_stages.stage_names:
            raise ValueError(
                f"Stage name {name} already present: all stage names must be unique"
            )

        method_left = self._get_validated_lateral_earth_pressure_method(method_left)
        method_right = self._get_validated_lateral_earth_pressure_method(method_right)
        self._validate_lateral_earth_pressure_methods_for_single_pile_model(
            method_left, method_right
        )

        kwargs = self._filter_none_values_from_key_value_dict(
            {
                "name": name,
                "displacement_top_sheet_piling": pile_top_displacement,
                "passive_side": passive_side,
                "method_left": method_left,
                "method_right": method_right,
            }
        )
        self.construction_stages.stages.append(ConstructionStage(**kwargs))
        # defaults for calculation options should be initialised here
        self.calculation_options_per_stage.stageoptions.append(StageOptions())

    def _get_validated_lateral_earth_pressure_method(
        self, stage_method: Optional[LateralEarthPressureMethod]
    ) -> LateralEarthPressureMethod:
        """
        When no stage_method is provided, returns the method set in the model options.
        Raises ValueError if method is not compatible with method set on model."""
        if not isinstance(self.model, Model):
            raise ValueError(f"Model is a string; set model first")
        if stage_method is None:
            return self.model.method
        if stage_method == LateralEarthPressureMethod.MIXED:
            raise ValueError(
                f"Mixed method cannot be passed directly to stage. Use {LateralEarthPressureMethod.KA_KO_KP} or {LateralEarthPressureMethod.C_PHI_DELTA}"
            )
        error = ValueError(
            f"stage_method {stage_method} is not compatible with method on model {self.model.method}"
        )
        if (
            self.model.method == LateralEarthPressureMethod.KA_KO_KP
            and stage_method == LateralEarthPressureMethod.C_PHI_DELTA
        ):
            raise error
        if (
            self.model.method == LateralEarthPressureMethod.C_PHI_DELTA
            and stage_method == LateralEarthPressureMethod.KA_KO_KP
        ):
            raise error
        return stage_method

    def _validate_lateral_earth_pressure_methods_for_single_pile_model(
        self,
        method_left: LateralEarthPressureMethod,
        method_right: LateralEarthPressureMethod,
    ) -> None:
        if not isinstance(self.model, Model):
            raise ValueError(f"Model is a string; set model first")
        if self.model.model == ModelType.SINGLE_PILE:
            if method_left != method_right:
                raise ValueError(
                    f"For the Single Pile Model the left and right method must be the same. Received: left {method_left} and right {method_right}"
                )

    def _filter_none_values_from_key_value_dict(self, dict_: Dict) -> Dict:
        # This way defaults can be defined only in the internal.
        return {k: v for k, v in dict_.items() if v is not None}

    def _from_snake_to_pascal_case(self, dict_: Dict) -> Dict:
        return {k.replace("_", ""): v for k, v in dict_.items()}

    def add_water_level(self, stage_id: int, water_level: WaterLevel, side: Side) -> None:
        # Add water level to water levels
        if isinstance(self.waterlevels, str):
            self.waterlevels = WaterLevels()
        if water_level.name not in self.waterlevels.water_level_names:
            self.waterlevels.levels.append(water_level)

        # Add water level to stages.
        if side == Side.LEFT:
            self.construction_stages.stages[stage_id].water_level_left = water_level.name
        elif side == Side.RIGHT:
            self.construction_stages.stages[stage_id].water_level_right = water_level.name
        else:
            raise ValueError(f"Provide a Side, received {side}")

    def add_surface(self, stage_id: int, surface: Surface, side: Side) -> None:
        # Add surface to surfaces
        if isinstance(self.surfaces, str):
            self.surfaces = Surfaces()
        if surface.name not in self.surfaces.surface_names:
            self.surfaces.surfaces.append(surface)

        # Add surface to stages.
        if side == Side.BOTH:
            self.construction_stages.stages[stage_id].surface_left = surface.name
            self.construction_stages.stages[stage_id].surface_right = surface.name
        elif side == Side.LEFT:
            self.construction_stages.stages[stage_id].surface_left = surface.name
        elif side == Side.RIGHT:
            self.construction_stages.stages[stage_id].surface_right = surface.name
        else:
            raise ValueError(f"Provide a Side, received {side}")

    def add_element_in_sheet_piling(
        self, sheet: Any, location_top: Optional[Point] = None,
    ) -> None:
        self.sheet_piling.update_level_top_sheet_pile(location_top)
        try:
            sheet = sheet._to_internal()
        except AttributeError:
            raise ValueError(f"Invalid argument, expected sheet, got {type(sheet)}")
        sheet.update_arguments_if_invalid_input()
        self.sheet_piling.sheetpiling.append(sheet)
        self.sheet_piling.update_length_of_sheet_pile()

    def add_support(
        self, stage_id: int, support: Union[Anchor], pre_stress: Optional[float]
    ) -> None:
        if isinstance(support, Anchor):
            self._add_anchor(stage_id, support, pre_stress)
        elif isinstance(support, Strut):
            self._add_strut(stage_id, support, pre_stress)
        else:
            raise ValueError(f"Unsupported support type: {support}")

    def _add_anchor(
        self, stage_id: int, anchor: Anchor, pre_tension: Optional[float]
    ) -> None:
        if isinstance(self.anchors, str) or self.anchors is None:
            self.anchors = Anchors()
        if anchor.name not in self.anchors.anchor_names:
            self.anchors.anchors.append(anchor)

        self.construction_stages.stages[stage_id].anchors.append(
            AnchorOrStrutPresstressReference(
                name=anchor.name, pre_stress=pre_tension or _DEFAULT_PRE_STRESS
            )
        )

    def _add_strut(
        self, stage_id: int, strut: Strut, pre_compression: Optional[float]
    ) -> None:
        if isinstance(self.struts, str) or self.struts is None:
            self.struts = Struts()
        if strut.name not in self.struts.strut_names:
            self.struts.struts.append(strut)

        self.construction_stages.stages[stage_id].struts.append(
            AnchorOrStrutPresstressReference(
                name=strut.name, pre_stress=pre_compression or _DEFAULT_PRE_STRESS
            )
        )


class DSheetPilingOutputStructure(DSeriesStructure):
    calculation_type: str

    # Sheetpile calculation
    sheetpile_elements: Optional[str]
    points_on_sheetpile: Optional[str]
    construction_stage: Optional[str]
    resume: Optional[str]

    # Vibration calculation
    settlement_by_vibration: Optional[str]

    # Verification calculation
    # TODO Split further based on A/B grouping
    overall_partial_factor_set: Optional[str]
    factors_for_verification: Optional[str]
    verify_low_mod_with_alt_passive_waterlevel: Optional[str]
    verify_moment_high_angle_of_subgr_reac: Optional[str]
    verify_anchor_force: Optional[str]
    calculation_overview: Optional[str]
    verify_moment_low_angle_of_subgr_reac: Optional[str]
    verify_high_mod_with_alt_passive_waterlevel: Optional[str]
    number_of_verifications: Optional[str]
    maximum_moment_effect_included: Optional[str]
    eurocode_belgie_set2: Optional[str]
    eurocode_belgie_set1: Optional[str]
    verify_deformation: Optional[str]
    warning_list: Optional[str]


class DSheetPilingStructure(DSeriesPilingParserStructure):
    version: Version = Version()
    version_externals: VersionExternals = VersionExternals()
    input_data: DSheetPilingInputStructure = DSheetPilingInputStructure()
    output_data: Optional[DSheetPilingOutputStructure] = None

    @property
    def is_valid(self) -> bool:
        return self.input_data.is_valid


class DSheetPilingDumpStructure(DSeriesPilingDumpParserStructure):
    dumpfile: DSheetPilingStructure
