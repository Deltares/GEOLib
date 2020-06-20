import logging
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel as DataClass

from geolib.models.dseries_parser import (
    DSeriesKeyValueSubStructure,
    DSeriesListSubStructure,
    DSeriesNameKeyValueSubStructure,
    DSeriesStructure,
    DSheetOutputStructure,
)

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

DataClass.Config.arbitrary_types_allowed = True


class Version(DSeriesKeyValueSubStructure):
    soil: int = 1005
    d__sheet_piling: int = 1018


class VersionExternals(DSeriesKeyValueSubStructure):
    dgscptipcalc____dll: str = "19.1.1.23469"
    dgscptipui____dll: str = "19.1.1.23469"


class Soil(DSeriesNameKeyValueSubStructure):
    # TODO Convert from str types to actual type
    name: str = "default soil"
    soilcolor: int = 9764853
    soilsoiltype: str = 2
    soilgraintype: str = 0
    soilgamdry: float = 1.50
    soilgamwet: float = 1.80
    soilrelativedensity: float = 72.5
    soilemodmenard: float = 0.01
    soilcohesion: float = 100.00
    soilphi: float = 40.00
    soildelta: float = 0.00
    soilcutop: float = 0.00
    soilcubottom: float = 0.00
    soilcubearingcapacityfactor: float = 4.10
    soilocr: float = 1.00
    soildrained: str = 0
    soilpermeabkx: float = 1.00000e-03
    soilstdcohesion: float = 0.00
    soilstdphi: float = 0.00
    soildistcohesion: str = 3
    soildistphi: str = 3
    soilla: float = 0.10
    soilln: float = 5.00
    soillp: float = 17.00
    soilusemenard: str = 1
    soilusebrinchhansen: str = 1
    soilshellfactor: float = 1.00
    soillambdatype: str = 0
    soillam1: str = 50
    soillam2: str = 80
    soillam3: str = 90
    soilkb0: float = 1.00000e04
    soilkb1: float = 5.00000e00
    soilkb2: float = 1.00000e04
    soilkb3: float = 1.00000e04
    soilkb4: float = 1.00000e04
    soilko0: float = 1.00000e04
    soilko1: float = 5.00000e00
    soilko2: float = 1.00000e04
    soilko3: float = 1.00000e04
    soilko4: float = 1.00000e04
    soilcurkb1: float = 2.00000e03
    soilcurkb2: float = 8.00000e02
    soilcurkb3: float = 5.00000e02
    soilcurko1: float = 2.00000e03
    soilcurko2: float = 8.00000e02
    soilcurko3: float = 5.00000e02
    soilhorizontalbehaviourtype: str = 2
    soilelasticity: float = 1.00000e03
    soildefaultelasticity: str = 1


class SoilCollection(DSeriesListSubStructure):
    soil: List[Soil] = []


class CalculationOptions(DSeriesStructure):
    # TODO Set type from sting to actual type
    calcfirststageinitial: str = 0
    calcminornodeson: str = 1
    calcreducedeltas: str = 1
    calcempiricalfactorstresstype: str = 0
    inputcalculationtype: str = 0
    calcautolambdason: str = 1
    designstage: str = 0
    designpilelengthfrom: str = 0.00
    designpilelengthto: str = 0.00
    designpilelengthdecrement: str = 0.00
    designpilelengthnew: str = 1
    designtype: str = 0
    designeurocodepartialfactorset: str = 0
    designpartialfactorsetec7nadnl: str = 1
    designec7nlmethod: str = 0
    designpartialfactorsetec7nadb: str = 0
    designec7bmethod: str = 0
    designpartialfactorset: str = 0
    designcurmethod: str = 0
    designpartialfactorsetec7nadse: str = 0
    designec7semethod: str = 0
    verifytype: str = 0
    eurocodepartialfactorset: str = 0
    eurocodeoverallstability: str = 0
    ec7nlmethod: str = 0
    ec7nloverallpartialfactorset: str = 1
    ec7nloverallanchorfactor: str = 1.000
    ec7nadnloverallstability: str = 0
    ec7boverallstability: str = 0
    nbmethod: str = 0
    curmethod: str = 0
    curoverallpartialfactorset: str = 0
    curoverallanchorfactor: str = 1.000
    curoverallstability: str = 0
    ec7semethod: str = 0
    ec7seoverallpartialfactorset: str = 0
    ec7nadseoverallstability: str = 0
    curanchorforcestage: str = 0
    curstabilitystage: str = 0
    overallstabilitytype: str = 0
    stabilityeurocodepartialfactorset: str = 0
    stabilityec7nlpartialfactorset: str = 1
    stabilityec7bpartialfactorset: str = 0
    stabilitycurpartialfactorset: str = 0
    stabilityec7separtialfactorset: str = 0
    overallstabilitydrained: str = 1

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


class DSheetPilingInputStructure(DSeriesStructure):
    """Representation of complete .foi file."""

    version: Version = Version()
    version_externals: VersionExternals = VersionExternals()
    soil_collection: SoilCollection = SoilCollection()
    run_identification: str = ""
    model: str = ""
    cpt_list: str = ""
    sheet_piling: str = ""
    combined_wall: str = ""
    vertical_balance: str = ""
    settlement_by_vibration_params: str = ""
    horizontal_line_loads: str = ""
    water: str = ""
    earth_quake: str = ""
    soil_profiles: str = ""
    surfaces: str = ""
    waterlevels: str = ""
    construction_stages: str = ""
    calculation_options_per_stage: str = ""
    calculation_options: CalculationOptions = CalculationOptions()
    probabilistic_calculation_options: str = ""
    probabilistic_control_parameters: str = ""


class DSheetPilingOutputStructure(DSheetOutputStructure):
    input_data: str
    calculation_type: str
    sheetpile_elements: str
    points_on_sheetpile: str
    construction_stage: str
    resume: str
