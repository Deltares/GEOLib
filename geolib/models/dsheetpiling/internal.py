import logging
import warnings
from abc import ABCMeta
from enum import Enum, IntEnum
from inspect import cleandoc
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from geolib._compat import IS_PYDANTIC_V2

if IS_PYDANTIC_V2:
    from pydantic import Field, StringConstraints
    from typing_extensions import Annotated
else:
    from pydantic import confloat, conint, conlist, constr

import geolib.models.dsheetpiling.constructions as constructions
from geolib.geometry import Point
from geolib.models import BaseDataClass
from geolib.models.dseries_parser import (
    DSerieListStructure,
    DSeriesInlineMappedProperties,
    DSeriesInlineReversedProperties,
    DSeriesNoParseSubStructure,
    DSeriesRepeatedGroupedProperties,
    DSeriesStructure,
    DSeriesStructureCollection,
    DSeriesTableStructure,
    DSeriesUnmappedNameProperties,
    DSeriesWrappedTableStructure,
    DSerieVersion,
)
from geolib.utils import make_newline_validator

from .calculation_options import (
    CalculationOptionsPerStage as CalculationOptionsPerStageExternal,
)
from .dsheetpiling_structures import (
    DSeriesPilingDumpParserStructure,
    DSeriesPilingParserStructure,
    DSheetpilingSurchargeLoad,
    DSheetpilingTableEntry,
    DSheetpilingUnwrappedTable,
    DSheetpilingWithNumberOfRowsTable,
)
from .dsheetpiling_validator import DSheetPilingValidator
from .internal_partial_factors import (
    PartialFactorsCurI,
    PartialFactorsCurIi,
    PartialFactorsCurIii,
    PartialFactorsEc7BESet1,
    PartialFactorsEc7BESet2,
    PartialFactorsEc7Nl0,
    PartialFactorsEc7Nl1,
    PartialFactorsEc7Nl2,
    PartialFactorsEc7Nl3,
    PartialFactorsEurocodeDa1Set1,
    PartialFactorsEurocodeDa1Set2,
    PartialFactorsEurocodeDa2,
    PartialFactorsEurocodeDa3,
)
from .settings import (
    CalculationType,
    CurveSettings,
    DesignType,
    DistributionType,
    EarthPressureCoefficients,
    GrainType,
    HorizontalBehaviorType,
    LambdaType,
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    LoadTypeFavourableUnfavourable,
    LoadTypeFavourableUnfavourableMoment,
    LoadTypePermanentVariable,
    ModelType,
    ModulusReactionType,
    ModulusSubgradeReaction,
    PartialFactorCalculationType,
    PartialFactorSetCUR,
    PartialFactorSetEC,
    PartialFactorSetEC7NADBE,
    PartialFactorSetEC7NADNL,
    PartialFactorSetVerifyEC,
    PassiveSide,
    SheetPilingElementMaterialType,
    Side,
    SinglePileLoadOptions,
    SoilTypeModulusSubgradeReaction,
    VerifyType,
)

logger = logging.getLogger(__name__)


_DEFAULT_WATER_LEVEL_NAME: str = "New Water Level"
_DEFAULT_SOIL_PROFILE_NAME: str = "New Profile"
_DEFAULT_SURFACE_NAME: str = "New Surface"
_DEFAULT_SHEET_PILING_ELEMENT_NAME: str = "New element"
_DEFAULT_UNIT_WEIGHT_WATER: float = 9.81
_DEFAULT_PRE_STRESS: float = 0.0

_DEFAULT_SOIL_VERSION: int = 1010
_DEFAULT_SHEETPILING_VERSION: int = 1033

REQ_RUN_LINES = 2


class Model(DSeriesInlineReversedProperties):
    model: ModelType = ModelType.SHEET_PILING
    method: LateralEarthPressureMethod = LateralEarthPressureMethod.MIXED
    verification: bool = False
    pile_load_option: bool = False
    pile_load_by_user: bool = False
    probabilistic: bool = False
    check_vertical_balance: bool = True
    trildens_calculation: bool = True
    diepwand_calculation: bool = False
    elastic_calculation: bool = True
    wooden_sheetpiling: bool = False


class Version(DSerieVersion):
    soil: int = _DEFAULT_SOIL_VERSION
    d__sheet_piling: int = _DEFAULT_SHEETPILING_VERSION


class VersionExternals(DSeriesInlineMappedProperties):
    dgscptipcalc____dll: str = "21.3.1.35380"
    dgscptipui____dll: str = "21.3.1.35380"


class Soil(DSeriesUnmappedNameProperties):
    if IS_PYDANTIC_V2:
        name: Annotated[
            str, StringConstraints(min_length=1, max_length=25)
        ] = "default soil"
        soilcolor: int = 9764853
        soilsoiltype: SoilTypeModulusSubgradeReaction = (
            SoilTypeModulusSubgradeReaction.SAND
        )
        soilgraintype: GrainType = GrainType.FINE
        soilgamdry: Annotated[float, Field(ge=0, le=100)] = 0.01
        soilgamwet: Annotated[float, Field(ge=0, le=100)] = 0.01
        soilrelativedensity: Annotated[float, Field(ge=0, le=100)] = 0
        soilemodmenard: Annotated[float, Field(ge=0.01, le=1000000)] = 0.01
        soilcohesion: Annotated[float, Field(ge=0, le=1000000000)] = 0
        soilphi: Annotated[float, Field(ge=-89, le=89)] = 0
        soildelta: Annotated[float, Field(ge=-80, le=89)] = 0.00
        soilisdeltaangleautomaticallycalculated: bool = False
        soilocr: Annotated[float, Field(ge=0, le=1000)] = 1.00
        soilpermeabkx: Annotated[float, Field(ge=0.00000000001, le=1000000)] = 0.0001
        soilstdcohesion: Annotated[float, Field(ge=0, le=100000000)] = 0.00
        soilstdphi: Annotated[float, Field(ge=0, le=100000000)] = 0.00
        soildistcohesion: DistributionType = DistributionType.NONE
        soildistphi: DistributionType = DistributionType.NONE
        soilla: Annotated[float, Field(ge=0, le=1000)] = 0
        soilln: Annotated[float, Field(ge=0, le=1000)] = 0.01
        soillp: Annotated[float, Field(ge=0, le=1000)] = 0.01
        soilusemenard: ModulusSubgradeReaction = ModulusSubgradeReaction.MANUAL
        soilusebrinchhansen: EarthPressureCoefficients = EarthPressureCoefficients.MANUAL
        soilshellfactor: Annotated[float, Field(ge=1, le=1000)] = 1.00
        soillambdatype: LambdaType = LambdaType.MANUAL
        soillam1: Annotated[float, Field(ge=0, le=100)] = 50
        soillam2: Annotated[float, Field(ge=0, le=100)] = 80
        soillam3: Annotated[float, Field(ge=0, le=100)] = 90
        soilkb0: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilkb1: Annotated[float, Field(ge=0.01, le=10000000000)] = 5.00000e00
        soilkb2: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilkb3: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilkb4: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilko0: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilko1: Annotated[float, Field(ge=0.01, le=10000000000)] = 5.00000e00
        soilko2: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilko3: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilko4: Annotated[float, Field(ge=0.01, le=10000000000)] = 1.00000e04
        soilcurkb1: Annotated[float, Field(ge=0.01, le=10000000000)] = 2.00000e03
        soilcurkb2: Annotated[float, Field(ge=0.01, le=10000000000)] = 8.00000e02
        soilcurkb3: Annotated[float, Field(ge=0.01, le=10000000000)] = 5.00000e02
        soilcurko1: Annotated[float, Field(ge=0.01, le=10000000000)] = 2.00000e03
        soilcurko2: Annotated[float, Field(ge=0.01, le=10000000000)] = 8.00000e02
        soilcurko3: Annotated[float, Field(ge=0.01, le=10000000000)] = 5.00000e02
        soilhorizontalbehaviourtype: HorizontalBehaviorType = (
            HorizontalBehaviorType.ELASTIC
        )
        soilelasticity: float = 1.00000e03  # fixed value
        soildefaultelasticity: int = 1  # fixed value
    else:
        name: constr(min_length=1, max_length=25) = "default soil"
        soilcolor: int = 9764853
        soilsoiltype: SoilTypeModulusSubgradeReaction = (
            SoilTypeModulusSubgradeReaction.SAND
        )
        soilgraintype: GrainType = GrainType.FINE
        soilgamdry: confloat(ge=0, le=100) = 0.01
        soilgamwet: confloat(ge=0, le=100) = 0.01
        soilrelativedensity: confloat(ge=0, le=100) = 0
        soilemodmenard: confloat(ge=0.01, le=1000000) = 0.01
        soilcohesion: confloat(ge=0, le=1000000000) = 0
        soilphi: confloat(ge=-89, le=89) = 0
        soildelta: confloat(ge=-80, le=89) = 0.00
        soilisdeltaangleautomaticallycalculated: bool = False
        soilocr: confloat(ge=0, le=1000) = 1.00
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
        soilhorizontalbehaviourtype: HorizontalBehaviorType = (
            HorizontalBehaviorType.ELASTIC
        )
        soilelasticity: float = 1.00000e03  # fixed value
        soildefaultelasticity: int = 1  # fixed value


class SoilCollection(DSeriesStructureCollection):
    soil: List[Soil] = []

    @property
    def soil_names(self) -> Set[str]:
        return {soil.name for soil in self.soil}

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


class SoilLayer(DSeriesNoParseSubStructure):
    top_of_layer: float
    soil: str
    water_pressure_top: float
    water_pressure_bottom: float


class SoilProfile(DSeriesNoParseSubStructure):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=25)]
    else:
        name: constr(min_length=1, max_length=25)
    layers: List[SoilLayer]
    coordinate: Point


class SoilProfiles(DSeriesNoParseSubStructure):
    soil_profiles: List[SoilProfile] = []
    if IS_PYDANTIC_V2:
        curve_number: Annotated[int, Field(ge=1, le=4)] = 3
    else:
        curve_number: conint(ge=1, le=4) = 3
    use_unloading_reloading_curve: bool = False
    modulus_reaction_type: int = ModulusReactionType.SECANT.value

    @property
    def soil_profile_names(self) -> Set[str]:
        return {soil_profile.name for soil_profile in self.soil_profiles}

    @property
    def referenced_soil_names(self) -> Set[str]:
        return {layer.soil for profile in self.soil_profiles for layer in profile.layers}


class CalculationOptions(DSeriesStructure):
    # TODO these first values are not used for single pile
    calcfirststageinitial: bool = False
    calcminornodeson: bool = False
    calcreducedeltas: bool = False
    inputcalculationtype: CalculationType = CalculationType.STANDARD
    isvibrationcalculation: bool = False
    allowableanchorforcecalculationtype: bool = False
    # available when c, phi , delta is selected for as a model
    calcautolambdason: bool = True
    # design sheet pile length calculation
    if IS_PYDANTIC_V2:
        designstage: Annotated[int, Field(ge=0)] = 0
        designpilelengthfrom: Annotated[float, Field(ge=1, le=100)] = 1
        designpilelengthto: Annotated[float, Field(ge=1, le=100)] = 1
        designpilelengthdecrement: Annotated[float, Field(ge=0.01, le=10)] = 0.01
    else:
        designstage: conint(ge=0) = 0
        designpilelengthfrom: confloat(ge=1, le=100) = 1
        designpilelengthto: confloat(ge=1, le=100) = 1
        designpilelengthdecrement: confloat(ge=0.01, le=10) = 0.01
    designpilelengthnew: int = 1  # fixed value
    designtype: DesignType = DesignType.REPRESENTATIVE
    designeurocodepartialfactorset: PartialFactorSetEC = PartialFactorSetEC.DA1SET1
    designpartialfactorsetec7nadnl: PartialFactorSetEC7NADNL = (
        PartialFactorSetEC7NADNL.RC0
    )
    designec7nlmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designec7bmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designpartialfactorsetec7nadbe: PartialFactorSetEC7NADBE = (
        PartialFactorSetEC7NADBE.SET1
    )
    designec7bemethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    designpartialfactorset: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI
    designcurmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    # verify sheet piling calculation
    verifytype: VerifyType = VerifyType.CUR
    eurocodepartialfactorset: PartialFactorSetVerifyEC = PartialFactorSetVerifyEC.DA1
    eurocodeoverallstability: bool = False
    ec7nlmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    ec7nloverallpartialfactorset: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    if IS_PYDANTIC_V2:
        ec7nloverallanchorfactor: Annotated[float, Field(ge=0.001, le=1000)] = 1
    else:
        ec7nloverallanchorfactor: confloat(ge=0.001, le=1000) = 1
    ec7nadnloverallstability: bool = False
    ec7beoverallstability: bool = False
    ec7bemethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    nbmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    curmethod: PartialFactorCalculationType = PartialFactorCalculationType.METHODA
    curoverallpartialfactorset: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI
    if IS_PYDANTIC_V2:
        curoverallanchorfactor: Annotated[float, Field(ge=0.001, le=1000)] = 1
    else:
        curoverallanchorfactor: confloat(ge=0.001, le=1000) = 1
    curoverallstability: bool = False
    if IS_PYDANTIC_V2:
        # Characteristic Kranz Anchor Strength calculation
        curanchorforcestage: Annotated[int, Field(ge=0)] = 0
        # Overall stability calculation
        curstabilitystage: Annotated[int, Field(ge=0)] = 0
    else:
        # Characteristic Kranz Anchor Strength calculation
        curanchorforcestage: conint(ge=0) = 0
        # Overall stability calculation
        curstabilitystage: conint(ge=0) = 0
    overallstabilitytype: DesignType = DesignType.REPRESENTATIVE
    stabilityexport: bool = False
    stabilityeurocodepartialfactorset: PartialFactorSetEC = PartialFactorSetEC.DA1SET1
    stabilityec7nlpartialfactorset: PartialFactorSetEC7NADNL = (
        PartialFactorSetEC7NADNL.RC0
    )
    stabilityec7bepartialfactorset: PartialFactorSetEC7NADBE = (
        PartialFactorSetEC7NADBE.SET1
    )
    stabilitycurpartialfactorset: PartialFactorSetCUR = PartialFactorSetCUR.CLASSI

    # These are all subgroups (key=value)
    partial_factors_eurocode_da1_set1: PartialFactorsEurocodeDa1Set1 = (
        PartialFactorsEurocodeDa1Set1()
    )
    partial_factors_eurocode_da1_set2: PartialFactorsEurocodeDa1Set2 = (
        PartialFactorsEurocodeDa1Set2()
    )
    partial_factors_eurocode_da2: PartialFactorsEurocodeDa2 = PartialFactorsEurocodeDa2()
    partial_factors_eurocode_da3: PartialFactorsEurocodeDa3 = PartialFactorsEurocodeDa3()
    partial_factors_ec7_nl_0: PartialFactorsEc7Nl0 = PartialFactorsEc7Nl0()
    partial_factors_ec7_nl_1: PartialFactorsEc7Nl1 = PartialFactorsEc7Nl1()
    partial_factors_ec7_nl_2: PartialFactorsEc7Nl2 = PartialFactorsEc7Nl2()
    partial_factors_ec7_nl_3: PartialFactorsEc7Nl3 = PartialFactorsEc7Nl3()
    partial_factors_ec7_be_set1: PartialFactorsEc7BESet1 = PartialFactorsEc7BESet1()
    partial_factors_ec7_be_set2: PartialFactorsEc7BESet2 = PartialFactorsEc7BESet2()
    partial_factors_cur_i: PartialFactorsCurI = PartialFactorsCurI()
    partial_factors_cur_ii: PartialFactorsCurIi = PartialFactorsCurIi()
    partial_factors_cur_iii: PartialFactorsCurIii = PartialFactorsCurIii()


class SheetPileElement(DSeriesUnmappedNameProperties):
    if IS_PYDANTIC_V2:
        name: Annotated[
            str, StringConstraints(min_length=1, max_length=50)
        ] = _DEFAULT_SHEET_PILING_ELEMENT_NAME
        sheetpilingelementmaterialtype: SheetPilingElementMaterialType = (
            SheetPilingElementMaterialType.Steel
        )
        sheetpilingelementei: Annotated[float, Field(ge=0.001, le=1e12)] = 100000
        sheetpilingelementwidth: Annotated[float, Field(ge=0, le=1000)] = 1
        sheetpilingelementlevel: Annotated[float, Field(ge=-10000, le=10000)] = -10
        sheetpilingelementheight: Annotated[int, Field(ge=10, le=100000)] = 400
        sheetpilingpilewidth: Annotated[float, Field(ge=0, le=100000)] = 0
        sheetpilingelementsectionarea: Annotated[int, Field(ge=10, le=100000)] = 170
        sheetpilingelementresistingmoment: Annotated[int, Field(ge=0, le=100000)] = 0
        sheetpilingelementreductionfactorei: Annotated[float, Field(ge=0.01, le=10)] = 1
        sheetpilingelementnote: Annotated[
            str, StringConstraints(min_length=0, max_length=20)
        ] = ""
        sheetpilingelementmaxcharacteristicmoment: Annotated[
            float, Field(ge=0, le=100000)
        ] = 0
        sheetpilingelementmaxplasticcharacteristicmoment: Annotated[
            float, Field(ge=0, le=100000)
        ] = 0
        sheetpilingelementkmod: Annotated[float, Field(ge=0.01, le=1)] = 0.01
        sheetpilingelementmaterialfactor: Annotated[float, Field(ge=0.01, le=10)] = 0.01
        ssheetpilingelementreductionfactormaxmoment: Annotated[
            float, Field(ge=0.01, le=10)
        ] = 1
        diaphragmwallissymmetric: Annotated[int, Field(ge=0, le=1)] = 0
        diaphragmwallposeielastoplastic1: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallnegeielastoplastic1: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallposmomelastic: Annotated[
            float, Field(ge=0, le=1000000000000)
        ] = 100000
        diaphragmwallnegmomelastic: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallposmomplastic: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallnegmomplastic: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallposeielastoplastic2: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallposmomelastoplastic: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallnegeielastoplastic2: Annotated[float, Field(ge=0, le=100000)] = 0
        diaphragmwallnegmomelastoplastic: Annotated[float, Field(ge=0, le=100000)] = 0
        woodensheetpilingelemente: Annotated[
            float, Field(ge=0.001, le=1000000000000)
        ] = 100000
        woodensheetpilingelementcharacflexuralstrength: Annotated[
            float, Field(ge=0, le=100000)
        ] = 0
        woodensheetpilingelementksys: Annotated[float, Field(ge=0.01, le=10)] = 1.15
        woodensheetpilingelementkdef: Annotated[float, Field(ge=0.01, le=10)] = 1
        woodensheetpilingelementpsi2eff: Annotated[float, Field(ge=0, le=10)] = 1
        woodensheetpilingelementmaterialfactor: Annotated[
            float, Field(ge=0.01, le=10)
        ] = 1.3
        woodensheetpilingelementkmodfshort: Annotated[float, Field(ge=0.01, le=10)] = 0.65
        woodensheetpilingelementkmodflong: Annotated[float, Field(ge=0.01, le=10)] = 0.5
        woodensheetpilingelementkmode: Annotated[float, Field(ge=0.01, le=10)] = 0.8
    else:
        name: constr(min_length=1, max_length=50) = _DEFAULT_SHEET_PILING_ELEMENT_NAME
        sheetpilingelementmaterialtype: SheetPilingElementMaterialType = (
            SheetPilingElementMaterialType.Steel
        )
        sheetpilingelementei: confloat(ge=0.001, le=1e12) = 100000
        sheetpilingelementwidth: confloat(ge=0, le=1000) = 1
        sheetpilingelementlevel: confloat(ge=-10000, le=10000) = -10
        sheetpilingelementheight: conint(ge=10, le=100000) = 400
        sheetpilingpilewidth: confloat(ge=0, le=100000) = 0
        sheetpilingelementsectionarea: conint(ge=10, le=100000) = 170
        sheetpilingelementresistingmoment: conint(ge=0, le=100000) = 0
        sheetpilingelementreductionfactorei: confloat(ge=0.01, le=10) = 1
        sheetpilingelementnote: constr(min_length=0, max_length=20) = ""
        sheetpilingelementmaxcharacteristicmoment: confloat(ge=0, le=100000) = 0
        sheetpilingelementmaxplasticcharacteristicmoment: confloat(ge=0, le=100000) = 0
        sheetpilingelementkmod: confloat(ge=0.01, le=1) = 0.01
        sheetpilingelementmaterialfactor: confloat(ge=0.01, le=10) = 0.01
        ssheetpilingelementreductionfactormaxmoment: confloat(ge=0.01, le=10) = 1
        diaphragmwallissymmetric: conint(ge=0, le=1) = 0
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
        if IS_PYDANTIC_V2:
            default_dict = dict(self.model_fields)
        else:
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
    if IS_PYDANTIC_V2:
        sheetpiling: Annotated[List[SheetPileElement], Field(min_length=1)] = [
            SheetPileElement()
        ]
        leveltopsheetpiling: Annotated[float, Field(ge=-10000, le=10000)] = 0.0
        lengthsheetpiling: Annotated[float, Field(gt=0)] = 10
    else:
        sheetpiling: conlist(SheetPileElement, min_items=1) = [SheetPileElement()]
        leveltopsheetpiling: confloat(ge=-10000, le=10000) = 0.0
        lengthsheetpiling: confloat(gt=0) = 10


class Anchor(DSheetpilingTableEntry):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: float = 0
        e_modulus: Annotated[float, Field(gt=0)] = 2.1e8
        cross_section: Optional[Annotated[float, Field(gt=0)]] = 1e-3
        wall_height_kranz: Optional[Annotated[float, Field(ge=0)]] = 0.00
        length: Optional[Annotated[float, Field(gt=0)]] = 1
        angle: Optional[float] = 0.00
        yield_force: Optional[Annotated[float, Field(ge=0)]] = 0.00
        side: Side = Side.RIGHT
    else:
        name: constr(min_length=1, max_length=50)
        level: float = 0
        e_modulus: confloat(gt=0) = 2.1e8
        cross_section: Optional[confloat(gt=0)] = 1e-3
        wall_height_kranz: Optional[confloat(ge=0)] = 0.00
        length: Optional[confloat(gt=0)] = 1
        angle: Optional[float] = 0.00
        yield_force: Optional[confloat(ge=0)] = 0.00
        side: Side = Side.RIGHT


class Anchors(DSheetpilingUnwrappedTable):
    """Container for Anchor."""

    anchors: List[Anchor] = []

    @property
    def anchor_names(self) -> Set[str]:
        return {anchor.name for anchor in self.anchors}


class AnchorOrStrutPresstressReference(BaseDataClass):
    """Used in the ConstructionStage to identify anchor and assign a
    prestress."""

    name: str
    if IS_PYDANTIC_V2:
        pre_stress: Annotated[float, Field(ge=0)] = _DEFAULT_PRE_STRESS
    else:
        pre_stress: confloat(ge=0) = _DEFAULT_PRE_STRESS


class Strut(DSheetpilingTableEntry):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: float = 0
        e_modulus: Annotated[float, Field(gt=0)] = 2.1e8
        cross_section: Optional[Annotated[float, Field(gt=0)]] = 1e-4
        length: Optional[Annotated[float, Field(gt=0)]] = 1
        angle: Optional[float] = 0.00
        buckling_force: Optional[Annotated[float, Field(ge=0)]] = 0.00
        side: Side = Side.RIGHT
    else:
        name: constr(min_length=1, max_length=50)
        level: float = 0
        e_modulus: confloat(gt=0) = 2.1e8
        cross_section: Optional[confloat(gt=0)] = 1e-4
        length: Optional[confloat(gt=0)] = 1
        angle: Optional[float] = 0.00
        buckling_force: Optional[confloat(ge=0)] = 0.00
        side: Side = Side.RIGHT


class Struts(DSheetpilingUnwrappedTable):
    """Container for Strut."""

    struts: List[Strut] = []

    @property
    def strut_names(self) -> Set[str]:
        return {strut.name for strut in self.struts}


class ConstructionStage(DSeriesUnmappedNameProperties):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
    displacement_top_sheet_piling: float = 0
    passive_side: PassiveSide = PassiveSide.DSHEETPILING_DETERMINED
    method_left: LateralEarthPressureMethodStage = (
        LateralEarthPressureMethodStage.KA_KO_KP
    )
    method_right: LateralEarthPressureMethodStage = (
        LateralEarthPressureMethodStage.KA_KO_KP
    )
    water_level_left: str = _DEFAULT_WATER_LEVEL_NAME
    water_level_right: str = _DEFAULT_WATER_LEVEL_NAME
    surface_left: str = _DEFAULT_SURFACE_NAME
    surface_right: str = _DEFAULT_SURFACE_NAME
    soil_profile_left: Optional[str] = _DEFAULT_SOIL_PROFILE_NAME
    soil_profile_right: Optional[str] = _DEFAULT_SOIL_PROFILE_NAME
    anchors: List[AnchorOrStrutPresstressReference] = []
    struts: List[AnchorOrStrutPresstressReference] = []
    spring_supports: List[str] = []
    rigid_supports: List[str] = []
    uniform_loads: List[str] = []
    surcharge_loads_left: List[str] = []
    surcharge_loads_right: List[str] = []
    horizontal_line_loads: List[str] = []
    moment_loads: List[str] = []
    normal_forces: List[str] = []


class ConstructionStages(DSeriesStructureCollection):
    stages: List[ConstructionStage] = []

    @property
    def stage_names(self) -> Set[str]:
        return {stage.name for stage in self.stages}


class WaterLevel(DSeriesNoParseSubStructure):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
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
    """Representation of [STAGE] block."""

    stagepartialfactorsetcur: PartialFactorSetCUR = PartialFactorSetCUR.UNKNOWN
    stageverify: int = 0
    if IS_PYDANTIC_V2:
        stageanchorfactor: Annotated[float, Field(ge=0.001, le=1000)] = 1
    else:
        stageanchorfactor: confloat(ge=0.001, le=1000) = 1
    stagepartialfactorsetec7nadnl: PartialFactorSetEC7NADNL = PartialFactorSetEC7NADNL.RC0
    stageverifyec7nadnl: int = 0
    if IS_PYDANTIC_V2:
        stageanchorfactorec7nadnl: Annotated[float, Field(ge=0.001, le=1000)] = 1
    else:
        stageanchorfactorec7nadnl: confloat(ge=0.001, le=1000) = 1
    stageverifyec7nadbe: int = 0


class CalculationOptionsPerStage(DSeriesStructureCollection):
    """Representation of [CALCULATION OPTIONS PER STAGE] block."""

    stageoptions: List[StageOptions] = []


class UniformLoad(DSeriesUnmappedNameProperties):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
    uniformloadleft: float
    uniformloadright: float
    uniformloadpermanent: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT
    uniformloadfavourable: LoadTypeFavourableUnfavourable = (
        LoadTypeFavourableUnfavourable.DSHEETPILING_DETERMINED
    )
    uniformloadstandarddeviationleft: float
    uniformloadstandarddeviationright: float
    uniformloaddistleft: DistributionType = DistributionType.NORMAL
    uniformloaddistright: DistributionType = DistributionType.NORMAL


class UniformLoads(DSeriesStructureCollection):
    loads: List[UniformLoad] = []

    @property
    def load_names(self) -> Set[str]:
        return {load.name for load in self.loads}


class SurchargePoint(DSeriesInlineMappedProperties):
    surchargeloaddistance: float
    surchargeloadvalue: float


class SurchargeLoad(DSheetpilingSurchargeLoad):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    else:
        name: constr(min_length=1, max_length=50)
    points: List[SurchargePoint] = []
    surchargeloadpermanent: LoadTypePermanentVariable = (
        LoadTypePermanentVariable.PERMANENT
    )
    surchargeloadfavourable: LoadTypeFavourableUnfavourable = (
        LoadTypeFavourableUnfavourable.DSHEETPILING_DETERMINED
    )
    surchargeloadstandarddeviation: float = 0.00
    surchargeloaddistribution: DistributionType = DistributionType.NORMAL


class SurchargeLoads(DSeriesStructureCollection):
    loads: List[SurchargeLoad] = []

    @property
    def load_names(self) -> Set[str]:
        return {load.name for load in self.loads}


class Surface(DSeriesNoParseSubStructure):  # TODO determine structure
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        points: Annotated[List[Point], Field(min_length=1)]
        points: Annotated[List[dict], Field(min_length=1)]
        distribution_type: DistributionType = DistributionType.NONE
        std: Annotated[float, Field(ge=0.0)] = 0.0
    else:
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


class HorizontalLineLoad(DSeriesNoParseSubStructure):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: Annotated[float, Field(ge=-1e12, le=1e12)] = 0
        load: Annotated[float, Field(ge=-1e12, le=1e12)] = 100
    else:
        name: constr(min_length=1, max_length=50)
        level: confloat(ge=-1e12, le=1e12) = 0
        load: confloat(ge=-1e12, le=1e12) = 100
    load_type: LoadTypeFavourableUnfavourable = (
        LoadTypeFavourableUnfavourable.DSHEETPILING_DETERMINED
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class HorizontalLineLoads(DSeriesNoParseSubStructure):
    loads: List[HorizontalLineLoad] = []


class Moment(DSeriesNoParseSubStructure):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: Annotated[float, Field(ge=-1e12, le=1e12)] = 0
        load: Annotated[float, Field(ge=-1e12, le=1e12)] = 100
    else:
        name: constr(min_length=1, max_length=50)
        level: confloat(ge=-1e12, le=1e12) = 0
        load: confloat(ge=-1e12, le=1e12) = 100
    load_type: LoadTypeFavourableUnfavourableMoment = (
        LoadTypeFavourableUnfavourableMoment.FAVOURABLE
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class Moments(DSeriesNoParseSubStructure):
    loads: List[Moment] = []


class NormalForce(DSeriesNoParseSubStructure):
    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        force_at_sheet_pile_top: Annotated[float, Field(ge=-1e12, le=1e12)]
        force_at_surface_level_left_side: Annotated[float, Field(ge=-1e12, le=1e12)]
        force_at_surface_level_right_side: Annotated[float, Field(ge=-1e12, le=1e12)]
        force_at_sheet_pile_toe: Annotated[float, Field(ge=-1e12, le=1e12)]
    else:
        name: constr(min_length=1, max_length=50)
        force_at_sheet_pile_top: confloat(ge=-1e12, le=1e12)
        force_at_surface_level_left_side: confloat(ge=-1e12, le=1e12)
        force_at_surface_level_right_side: confloat(ge=-1e12, le=1e12)
        force_at_sheet_pile_toe: confloat(ge=-1e12, le=1e12)
    load_type: LoadTypeFavourableUnfavourableMoment = (
        LoadTypeFavourableUnfavourableMoment.FAVOURABLE
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class NormalForces(DSeriesNoParseSubStructure):
    loads: List[NormalForce] = []


class Support(DSeriesNoParseSubStructure):
    """Internal structure for spring and rigid supports."""

    if IS_PYDANTIC_V2:
        name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
        level: float
        rotational_stiffness: Annotated[float, Field(ge=0)]
        translational_stiffness: Annotated[float, Field(ge=0)]
    else:
        name: constr(min_length=1, max_length=50)
        level: float
        rotational_stiffness: confloat(ge=0)
        translational_stiffness: confloat(ge=0)


class SupportContainer(DSeriesNoParseSubStructure):
    supports: List[Support] = []

    @property
    def support_names(self) -> Set[str]:
        return {support.name for support in self.supports}


class VibrationPosition(DSeriesNoParseSubStructure):
    x: float
    z: float


class VibrationPositions(DSeriesNoParseSubStructure):
    positions: List[VibrationPosition] = []


class Water(DSeriesUnmappedNameProperties):
    unit_weight_of_water: float = 9.81


class DSheetPilingInputStructure(DSeriesStructure):
    """Representation of complete .shi file."""

    version: Version = Version()
    version_externals: VersionExternals = VersionExternals()
    soil_collection: SoilCollection = SoilCollection()
    run_identification: str = 2 * "\n"
    model: Model = Model()
    cpt_list: str = cleandoc(
        """
        Count=0
        """
    )
    sheet_piling: Union[str, SheetPiling] = SheetPiling()
    combined_wall: str = ""
    vertical_balance: str = cleandoc(
        """
        SheetPilingQcRep=0.000
        SheetPilingXi=1.39
        """
    )
    settlement_by_vibration_params: str = cleandoc(
        """
        SheetPilingNumberOfPilesDrilled=2
        """
    )
    horizontal_line_loads: Union[HorizontalLineLoads, str, None] = None
    uniform_loads: Optional[UniformLoads] = None
    surcharge_loads: Optional[SurchargeLoads] = None
    water: str = ""
    earth_quake: str = cleandoc(
        """
        0.00
        """
    )
    soil_profiles: Union[SoilProfiles, str] = cleandoc(
        f"""
          1 Number of spring characteristics curves
          0 1/0 : Yes/No Unloading curve
          1 1/0 : Yes/No Use Cur values

          1 Number of soil profiles 
        {_DEFAULT_SOIL_PROFILE_NAME}
               0.000 X coordinate
               0.000 Y coordinate

          1 Number of soil layers per soil profile
         Nr      Level   Wosp Top  Wosp Bott Material Name
          1       0.00       0.00       0.00 New Material

        """
    )
    surfaces: Union[str, Surfaces] = cleandoc(
        f"""
        1 Number of surfaces 
        1     1 {_DEFAULT_SURFACE_NAME}
        0.00  Standard deviation
        2  Distribution type
        Nr     X-coord     Value
        1       0.00       0.00
        """
    )
    water: Water = Water()
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
    construction_stages: Union[str, ConstructionStages] = ConstructionStages()
    calculation_options_per_stage: CalculationOptionsPerStage = (
        CalculationOptionsPerStage()
    )
    calculation_options: CalculationOptions = CalculationOptions()
    probabilistic_calculation_options: str = cleandoc(
        """
        ZFunctionType=1
        ZFunctionMobilisation=100.00
        ZFunctionMoment=0.00
        ZFunctionAnchorForce=0.00
        ZFunctionAnchor=-1
        """
    )
    probabilistic_control_parameters: str = cleandoc(
        """
        IterationFactor=1.000
        IterationNumber=15
        CriteriaLimit1=0.010000
        CriteriaLimit2=0.010000
        ReliabilityStage=0
        """
    )

    """
    When there are no anchors, struts, supports, vibration positions or soil displacements in the model,
    their respective block is not present in the .shi file.
    """
    soil_displacements: Optional[str] = None
    rigid_supports: Union[str, SupportContainer, None] = None
    spring_supports: Union[str, SupportContainer, None] = None
    moments: Union[str, Moments, None] = None
    normal_forces: Union[str, NormalForces, None] = None
    anchors: Union[str, Anchors, None] = None
    struts: Union[str, Struts, None] = None
    vibration_positions: Union[str, VibrationPositions, None] = None

    # Custom validator
    _validate_run_identification = make_newline_validator(
        "run_identification", req_newlines=REQ_RUN_LINES
    )

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
                stage.method_left = (
                    LateralEarthPressureMethodStage.get_stage_type_from_method(
                        self.model.method
                    )
                )
                stage.method_right = (
                    LateralEarthPressureMethodStage.get_stage_type_from_method(
                        self.model.method
                    )
                )

    def set_calculation_options(self, **kwargs) -> None:
        kwargs = self._filter_none_values_from_key_value_dict(kwargs)
        # here add function that turns kwargs from snake case to pascal case
        kwargs = self._from_snake_to_pascal_case(kwargs)
        self.calculation_options = CalculationOptions(**kwargs)

    def add_calculation_options_per_stage(
        self,
        input_calc_options: CalculationOptionsPerStageExternal,
        stage_id: int,
    ) -> None:
        _map_external_to_internal_values = {
            VerifyType.CUR: {
                "stagepartialfactorsetcur": input_calc_options.partial_factor_set,
                "stageverify": stage_id + 1,
                "stageanchorfactor": input_calc_options.anchor_factor,
            },
            VerifyType.EC7NL: {
                "stagepartialfactorsetec7nadnl": input_calc_options.partial_factor_set,
                "stageverifyec7nadnl": stage_id + 1,
                "stageanchorfactorec7nadnl": input_calc_options.anchor_factor,
            },
            VerifyType.EC7BE: {
                "stageverifyec7nadbe": stage_id + 1,
            },
        }
        stageoptions = StageOptions(
            **_map_external_to_internal_values[self.calculation_options.verifytype]
        )
        self.calculation_options_per_stage.stageoptions[stage_id] = stageoptions

    def set_curve_settings(self, curve_settings: CurveSettings) -> None:
        if isinstance(self.soil_profiles, str):
            self.soil_profiles = SoilProfiles()
        self.soil_profiles.curve_number = curve_settings.curve_number
        self.soil_profiles.use_unloading_reloading_curve = (
            curve_settings.use_unloading_reloading_curve
        )
        self.soil_profiles.modulus_reaction_type = (
            curve_settings.modulus_reaction_type.value
        )

    def add_stage(
        self,
        name: str,
        passive_side: PassiveSide,
        method_left: LateralEarthPressureMethodStage,
        method_right: LateralEarthPressureMethodStage,
        pile_top_displacement: Optional[float],
    ) -> None:
        if isinstance(self.construction_stages, str):
            self.construction_stages = ConstructionStages()
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
        self, stage_method: Optional[LateralEarthPressureMethodStage]
    ) -> LateralEarthPressureMethodStage:
        """When no stage_method is provided, returns the method set in the
        model options.

        Raises ValueError if method is not compatible with method set on
        model.
        """
        if not isinstance(self.model, Model):
            raise ValueError("Model is a string; set model first")
        if stage_method is None:
            return self.model.method
        error = ValueError(
            f"stage_method {stage_method} is not compatible with method on model {self.model.method}"
        )
        if (
            self.model.method.name == LateralEarthPressureMethodStage.KA_KO_KP.name
            and stage_method.name == LateralEarthPressureMethodStage.C_PHI_DELTA.name
        ):
            raise error
        if (
            self.model.method.name == LateralEarthPressureMethodStage.C_PHI_DELTA.name
            and stage_method.name == LateralEarthPressureMethodStage.KA_KO_KP.name
        ):
            raise error
        return stage_method

    def _validate_lateral_earth_pressure_methods_for_single_pile_model(
        self,
        method_left: LateralEarthPressureMethodStage,
        method_right: LateralEarthPressureMethodStage,
    ) -> None:
        if not isinstance(self.model, Model):
            raise ValueError("Model is a string; set model first")
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
        stage = self.construction_stages.stages[stage_id]
        if side == Side.BOTH:
            stage.water_level_left = stage.water_level_right = water_level.name
        elif side == Side.LEFT:
            stage.water_level_left = water_level.name
        elif side == Side.RIGHT:
            stage.water_level_right = water_level.name
        else:
            raise ValueError(f"Provide a Side, received {side}")

    def add_profile(self, stage_id: int, profile: SoilProfile, side: Side) -> None:
        # Add profile to profiles
        if isinstance(self.soil_profiles, str):
            self.soil_profiles = SoilProfiles()
        if profile.name not in self.soil_profiles.soil_profile_names:
            self.soil_profiles.soil_profiles.append(profile)

        soil_names = self.soil_collection.soil_names
        for i, layer in enumerate(profile.layers):
            if layer.soil not in soil_names:
                raise ValueError(
                    f"Soil {layer.soil} of layer {i} is not in soil collection; add soil first via model."
                )
        # Add profile to stages.
        if side == Side.BOTH:
            self.construction_stages.stages[stage_id].soil_profile_left = profile.name
            self.construction_stages.stages[stage_id].soil_profile_right = profile.name
        elif side == Side.LEFT:
            self.construction_stages.stages[stage_id].soil_profile_left = profile.name
        elif side == Side.RIGHT:
            self.construction_stages.stages[stage_id].soil_profile_right = profile.name
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

    def set_construction(
        self, top_level: float, elements: List[SheetPileElement]
    ) -> None:
        elements.sort(key=lambda element: element.sheetpilingelementlevel, reverse=True)
        for sheet in elements:
            sheet.update_arguments_if_invalid_input()
        try:
            bottom_level = elements[-1].sheetpilingelementlevel
        except IndexError:
            raise ValueError("At least one sheet should be provided")

        self.sheet_piling = SheetPiling(
            sheetpiling=elements,
            leveltopsheetpiling=top_level,
            lengthsheetpiling=top_level - bottom_level,
        )

    def add_element_in_sheet_piling(
        self,
        sheet: Any,
        location_top: Optional[Point] = None,
    ) -> None:
        self.sheet_piling.update_level_top_sheet_pile(location_top)
        try:
            sheet = sheet._to_internal()
        except AttributeError:
            raise ValueError(f"Invalid argument, expected sheet, got {type(sheet)}")
        sheet.update_arguments_if_invalid_input()
        self.sheet_piling.sheetpiling.append(sheet)
        self.sheet_piling.update_length_of_sheet_pile()

    def add_anchor(self, stage_id: int, anchor: Anchor, pre_tension: float) -> None:
        if not isinstance(self.anchors, Anchors):
            self.anchors = Anchors()
        if anchor.name not in self.anchors.anchor_names:
            self.anchors.anchors.append(anchor)

        self.construction_stages.stages[stage_id].anchors.append(
            AnchorOrStrutPresstressReference(
                name=anchor.name, pre_stress=pre_tension or _DEFAULT_PRE_STRESS
            )
        )

    def add_strut(self, stage_id: int, strut: Strut, pre_compression: float) -> None:
        if not isinstance(self.struts, Struts):
            self.struts = Struts()
        if strut.name not in self.struts.strut_names:
            self.struts.struts.append(strut)

        self.construction_stages.stages[stage_id].struts.append(
            AnchorOrStrutPresstressReference(
                name=strut.name, pre_stress=pre_compression or _DEFAULT_PRE_STRESS
            )
        )

    def add_load(
        self, load: Union[HorizontalLineLoad, Moment, NormalForce], stage_id: int
    ):
        if isinstance(load, HorizontalLineLoad):
            self.is_valid_unique_load_names(
                load_list=self.construction_stages.stages[stage_id].horizontal_line_loads,
                name=load.name,
            )
            if (
                isinstance(self.horizontal_line_loads, str)
                or self.horizontal_line_loads is None
            ):
                self.horizontal_line_loads = HorizontalLineLoads()
            if load not in self.horizontal_line_loads.loads:
                self.horizontal_line_loads.loads.append(load)
            self.construction_stages.stages[stage_id].horizontal_line_loads.append(
                load.name
            )
        elif isinstance(load, Moment):
            self.is_valid_unique_load_names(
                load_list=self.construction_stages.stages[stage_id].moment_loads,
                name=load.name,
            )
            if isinstance(self.moments, str) or self.moments is None:
                self.moments = Moments()
            if load not in self.moments.loads:
                self.moments.loads.append(load)
            self.construction_stages.stages[stage_id].moment_loads.append(load.name)
        elif isinstance(load, NormalForce):
            self.is_valid_unique_load_names(
                load_list=self.construction_stages.stages[stage_id].normal_forces,
                name=load.name,
            )
            if isinstance(self.normal_forces, str) or self.normal_forces is None:
                self.normal_forces = NormalForces()
            if load not in self.normal_forces.loads:
                self.normal_forces.loads.append(load)
            self.construction_stages.stages[stage_id].normal_forces.append(load.name)
        elif isinstance(load, UniformLoad):
            self.add_uniform_load(load=load, stage_id=stage_id)
        else:
            raise ValueError("This type of load is not yet supported")

    def add_uniform_load(self, stage_id: int, load: UniformLoad) -> None:
        self.is_valid_unique_load_names(
            load_list=self.construction_stages.stages[stage_id].uniform_loads,
            name=load.name,
        )
        if not isinstance(self.uniform_loads, UniformLoads):
            self.uniform_loads = UniformLoads()
        if load not in self.uniform_loads.loads:
            self.uniform_loads.loads.append(load)
        self.construction_stages.stages[stage_id].uniform_loads.append(load.name)

    def add_surcharge_load(self, stage_id: int, load: SurchargeLoad, side: Side) -> None:
        if not isinstance(self.surcharge_loads, SurchargeLoads):
            self.surcharge_loads = SurchargeLoads()
        if load not in self.surcharge_loads.loads:
            self.surcharge_loads.loads.append(load)
        # Add load to stages.
        stage = self.construction_stages.stages[stage_id]
        if side == Side.BOTH:
            self.is_valid_unique_load_names(
                load_list=stage.surcharge_loads_left, name=load.name
            )
            stage.surcharge_loads_left.append(load.name)
            self.is_valid_unique_load_names(
                load_list=stage.surcharge_loads_right, name=load.name
            )
            stage.surcharge_loads_right.append(load.name)
        elif side == Side.LEFT:
            self.is_valid_unique_load_names(
                load_list=stage.surcharge_loads_left, name=load.name
            )
            stage.surcharge_loads_left.append(load.name)
        elif side == Side.RIGHT:
            self.is_valid_unique_load_names(
                load_list=stage.surcharge_loads_right, name=load.name
            )
            stage.surcharge_loads_right.append(load.name)
        else:
            raise ValueError(f"Provide a Side, received {side}")

    def is_valid_unique_load_names(self, load_list: List[str], name: str) -> bool:
        """Load list should have unique names in list of loads."""
        if name in load_list:
            raise ValueError(
                f"{name} load name is duplicated. Please change the name of the load."
            )
        return True

    def add_spring_support(self, stage_id: int, support: Support) -> None:
        if not isinstance(self.spring_supports, SupportContainer):
            self.spring_supports = SupportContainer()
        if support.name not in self.spring_supports.support_names:
            self.spring_supports.supports.append(support)

        self.construction_stages.stages[stage_id].spring_supports.append(support.name)

    def add_rigid_support(self, stage_id: int, support: Support) -> None:
        if not isinstance(self.rigid_supports, SupportContainer):
            self.rigid_supports = SupportContainer()
        if support.name not in self.rigid_supports.support_names:
            self.rigid_supports.supports.append(support)

        self.construction_stages.stages[stage_id].rigid_supports.append(support.name)


class Resume(DSheetpilingWithNumberOfRowsTable):
    resume: List[Dict[str, float]]


class BreukData(DSeriesInlineReversedProperties):
    percentage_mobilized_resistance_left: float
    percentage_mobilized_resistance_right: float
    effective_left: float
    effective_right: float
    water_pressure_left: float
    water_pressure_right: float
    max_passive_effect_resistance_left: float
    max_passive_effect_resistance_right: float
    max_passive_moment_left: float
    max_passive_moment_right: float
    max_mobilized_passive_moment_left: float
    max_mobilized_passive_moment_right: float
    vertical_force_left: float
    vertical_force_right: float
    level_of_single_support: float
    node_of_single_support: float
    moment_present: float
    active_side: float


class MomentsForcesDisplacements(DSeriesWrappedTableStructure):
    momentsforcesdisplacements: List[Dict[str, float]]


class AnchorData(DSheetpilingWithNumberOfRowsTable):
    anchordata: List[Dict[str, Union[float, str]]]


class Pressures(DSheetpilingWithNumberOfRowsTable):
    pressures: List[Dict[str, Union[float, str]]]


class SideOutput(DSeriesStructure):
    calculation_method: Optional[str] = None
    water_level: Optional[str] = None
    surface: Optional[str] = None
    soil_profile_for_single_pile_model: Optional[str] = None
    soil_profile_for_sheet_piling_model: Optional[str] = None
    pressures: Optional[Pressures] = None
    force_from_layer: Optional[str] = None
    lambdas: Optional[str] = None
    slide_plane: Optional[str] = None
    vertical_balance_per_layer: Optional[str] = None


class OutputConstructionStage(DSeriesRepeatedGroupedProperties):
    anchor_data: Optional[AnchorData] = None
    hload_data: Optional[str] = None
    breuk_data: Optional[BreukData] = None
    passive_side_data: Optional[str] = None
    soil_collapse_data: Optional[str] = None
    moments_forces_displacements: Optional[MomentsForcesDisplacements] = None
    side: Optional[List[SideOutput]] = None
    uniform_load_data: Optional[str] = None
    horizontal_line_load_data: Optional[str] = None
    surcharge_data: Optional[str] = None
    normal_force_data: Optional[str] = None
    moment_data: Optional[str] = None
    support_data: Optional[str] = None
    vertical_balance_data: Optional[str] = None

    @classmethod
    def get_list_field_names(cls) -> List[str]:
        return ["side"]


class DesignLengthInfo(DSeriesWrappedTableStructure):
    designlengthinfo: List[Dict[str, float]]


class DesignLengthCalculation(DSeriesWrappedTableStructure):
    designlengthcalculation: List[Dict[str, float]]


class DesignSheetpileLength(DSeriesStructure):
    design_length_info: Optional[DesignLengthInfo] = None
    design_length_calculation: Optional[DesignLengthCalculation] = None


class PointsOnSheetpile(DSheetpilingWithNumberOfRowsTable):
    pointsonsheetpile: List[Dict[str, float]]


class CurAnchorForceResults(DSheetpilingWithNumberOfRowsTable):
    curanchorforceresults: List[Dict[str, float]]


class BaseVerificationStructureProperties(DSeriesRepeatedGroupedProperties):
    points_on_sheetpile: Optional[List[PointsOnSheetpile]] = None
    construction_stage: Optional[List[OutputConstructionStage]] = None

    @classmethod
    def get_list_field_names(cls) -> List[str]:
        return ["points_on_sheetpile", "construction_stage"]


class DSheetPilingOutputStructure(DSeriesRepeatedGroupedProperties):
    @classmethod
    def get_list_field_names(cls) -> List[str]:
        return ["points_on_sheetpile", "construction_stage"]

    @classmethod
    def parse_text(cls, text):
        return super().parse_text(text)

    calculation_type: str

    # General data
    sheet_pile_elements: Optional[str] = None
    calculated_displacements: Optional[str] = None

    # Standard, Kranz and Reliability calculation
    points_on_sheetpile: Optional[List[PointsOnSheetpile]] = None
    construction_stage: Optional[List[OutputConstructionStage]] = None

    # Design Sheet Pile Length calculation
    design_sheetpile_length: Optional[DesignSheetpileLength] = None

    # Settlement by Vibration calculation
    settlement_by_vibration: Optional[str] = None

    # Verify calculation including Overall Stability calculation
    overall_partial_factor_set: Optional[str] = None
    factors_for_overall_stability: Optional[str] = None
    overall_stability_results: Optional[str] = None

    # Verify calculation according to CUR or EC7-NL with method B
    factors_for_verification: Optional[str] = None

    # Verify calculation according to CUR or EC7-NL
    verify_step_6____5_serviceability_limit_state: Optional[
        BaseVerificationStructureProperties
    ] = None
    verify_step_6____5_multiplied_by_factor: Optional[
        BaseVerificationStructureProperties
    ] = None
    verify_step_6____1_low_modulus_of_subgrade_reaction_and_high_passive_water_level: Optional[
        BaseVerificationStructureProperties
    ] = None
    verify_step_6____2_high_modulus_of_subgrade_reaction_and_high_passive_water_level: Optional[
        BaseVerificationStructureProperties
    ] = None
    verify_step_6____3_low_modulus_of_subgrade_reaction_and_low_passive_water_level: Optional[
        BaseVerificationStructureProperties
    ] = None
    verify_step_6____4_high_modulus_of_subgrade_reaction_and_low_passive_water_level: Optional[
        BaseVerificationStructureProperties
    ] = None
    cur_anchor_force_results: Optional[CurAnchorForceResults] = None

    # Verify calculation according to EC7-BE or EC7-General
    verify_deformation_serviceability_limit_state: Optional[
        BaseVerificationStructureProperties
    ] = None
    eurocode_1_set_1: Optional[BaseVerificationStructureProperties] = None
    eurocode_1_set_2: Optional[BaseVerificationStructureProperties] = None
    eurocode_2: Optional[BaseVerificationStructureProperties] = None
    eurocode_3: Optional[BaseVerificationStructureProperties] = None
    eurocode_belgium_set_1: Optional[BaseVerificationStructureProperties] = None
    eurocode_belgium_set_2: Optional[BaseVerificationStructureProperties] = None

    # Kranz calculation
    angles_kranz_calculation: Optional[str] = None
    kranz_calculation: Optional[str] = None
    kranz_diagram_results: Optional[str] = None

    # Resumes
    resume: Optional[Resume] = None
    anchors_and_struts_resume: Optional[str] = None
    supports_resume: Optional[str] = None
    maximum_anchor_force: Optional[str] = None
    maximum_summary_results: Optional[str] = None
    warnings: Optional[str] = None
    errors: Optional[str] = None


class DSheetPilingStructure(DSeriesPilingParserStructure):
    input_data: DSheetPilingInputStructure = DSheetPilingInputStructure()
    output_data: Optional[DSheetPilingOutputStructure] = None

    @property
    def is_valid(self) -> bool:
        return self.input_data.is_valid


class DSheetPilingDumpStructure(DSeriesPilingDumpParserStructure):
    dumpfile: DSheetPilingStructure
