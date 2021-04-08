from random import randint
from typing import Callable, Type

import pytest

from geolib.models.dfoundations.dfoundations_structures import DFoundationsTableWrapper
from geolib.models.dfoundations.internal import (
    CPT,
    CPTList,
    CPTMeasureData,
    DFoundationsCalculationParametersBearingPilesEC7,
    DFoundationsCalculationWarnings,
    DFoundationsDumpfileOutputStructure,
    DFoundationsGlobalNenResults,
    DFoundationsNenPileResults,
    DFoundationsNenPileResultsTable,
    DFoundationsStructure,
    DFoundationsVerificationResults,
    Layer,
    Profile,
    Profiles,
)


class TestInternalInputDFoundations:
    @pytest.mark.integrationtest
    def test_given_single_layer_text_when_parse_then_structure_parsed(self):
        # 1. Define test data.
        layer_name = "Layer (1)"
        material = 9
        top_level = 0.5
        excess_top = 0
        excess_bottom = 0
        ocr = 1
        reduction = 0
        text_to_parse = (
            ""
            + f"{layer_name}\n"
            + f"{material} : Material = Material (1)\n"
            + f"{top_level} : Top level [m]\n"
            + f"{excess_top} : Excess pore pressure at top [kN/m3]\n"
            + f"{excess_bottom} : Excess pore pressure at bottom [kN/m3]\n"
            + f"{ocr} : OCR value [-]\n"
            + f"{reduction} : Reduction of cone resistance [%]"
        )

        # 2. Run test.
        parsed_layer = Layer.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_layer
        assert parsed_layer.name == layer_name
        assert parsed_layer.material == material
        assert parsed_layer.top_level == top_level
        assert parsed_layer.excess_pore_pressure_top == excess_top
        assert parsed_layer.excess_pore_pressure_bottom == excess_bottom
        assert parsed_layer.ocr_value == ocr
        assert parsed_layer.reduction_core_resistance == reduction

    @pytest.mark.integrationtest
    def test_given_single_profile_text_when_parse_then_structure_parsed(self):
        # 1. Define test data.
        text_to_parse = (
            ""
            + "FUGBEN 1\n"
            + "0 : Matching CPT = FUGBEN 1\n"
            + "2.50 : X coordinate [m]\n"
            + "15.00 : Y coordinate [m]\n"
            + "-1.00 : Phreatic level [m]\n"
            + "-24.00 : Pile tip level [m]\n"
            + "1.00 : Overconsolidation ratio of bearing layer [m]\n"
            + "-17.00 : Top of positive skin friction zone [m]\n"
            + "-6.50 : Bottom of negative skin friction zone [m]\n"
            + "0.00 : Expected ground level settlement [m]\n"
            + "0.00 : Placement depth of foundation element [m]\n"
            + "3 : Concentration value according to Frohlich [-]\n"
            + "0.00 : Top of tension zone [m]\n"
            + "2 : Reduction type of cone resistance = Manual\n"
            + "-6.50 : Excavation level [m]\n"
            + "1 : Excavation width infinite = TRUE\n"
            + "1 : Excavation length infinite = TRUE\n"
            + "0.00 : Distance edge pile to excavation boundary [m]\n"
            + "1 : Number of layers\n"
            + "Layer (1)\n"
            + "9 : Material = Material (1)\n"
            + "0.500 : Top level [m]\n"
            + "0.00 : Excess pore pressure at top [kN/m3]\n"
            + "0.00 : Excess pore pressure at bottom [kN/m3]\n"
            + "1.00 : OCR value [-]\n"
            + "0 : Reduction of cone resistance [%]"
        )

        # 2. Run test.
        parsed_profile = Profile.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_profile
        assert parsed_profile.name == "FUGBEN 1"
        assert len(parsed_profile.layers) == 1

    @pytest.mark.integrationtest
    def test_given_single_profile_text_when_parse_profiles_then_structure_parsed(self):
        # 1. Define test data.
        text_to_parse = (
            ""
            + "1 = number of items\n"
            + "FUGBEN1\n"
            + "0 : Matching CPT = FUGBEN1\n"
            + "2.50 : X coordinate [m]\n"
            + "15.00 : Y coordinate [m]\n"
            + "-1.00 : Phreatic level [m]\n"
            + "-24.00 : Pile tip level [m]\n"
            + "1.00 : Overconsolidation ratio of bearing layer [m]\n"
            + "-17.00 : Top of positive skin friction zone [m]\n"
            + "-6.50 : Bottom of negative skin friction zone [m]\n"
            + "0.00 : Expected ground level settlement [m]\n"
            + "0.00 : Placement depth of foundation element [m]\n"
            + "3 : Concentration value according to Frohlich [-]\n"
            + "0.00 : Top of tension zone [m]\n"
            + "2 : Reduction type of cone resistance = Manual\n"
            + "-6.50 : Excavation level [m]\n"
            + "1 : Excavation width infinite = TRUE\n"
            + "1 : Excavation length infinite = TRUE\n"
            + "0.00 : Distance edge pile to excavation boundary [m]\n"
            + "1 : Number of layers\n"
            + "Layer (1)\n"
            + "9 : Material = Material (1)\n"
            + "0.500 : Top level [m]\n"
            + "0.00 : Excess pore pressure at top [kN/m3]\n"
            + "0.00 : Excess pore pressure at bottom [kN/m3]\n"
            + "1.00 : OCR value [-]\n"
            + "0 : Reduction of cone resistance [%]"
        )

        # 2. Run test.
        parsed_profiles = Profiles.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_profiles
        assert len(parsed_profiles.profiles) == 1
        profile = parsed_profiles.profiles[0]
        assert len(profile.layers) == 1

    @pytest.mark.unittest
    def test_default_soils_generated(self):
        from geolib.models.dfoundations.internal_soil import Soil

        soils = Soil.default_soils()
        assert len(soils) == 56

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "model, soilgamdryvalue",
        [
            pytest.param(
                "TENSION_PILES",
                17,
                id="Tension default soils",
            ),
            pytest.param(
                "BEARING_PILES",
                18,
                id="Bearing default soils",
            ),
        ],
    )
    def test_default_soils_generated_model_specific(self, model, soilgamdryvalue):
        from geolib.models.dfoundations.internal_soil import Soil

        soils = Soil.default_soils(model=model)
        assert len(soils) == 56
        assert soils[0].name == "BClay, clean, moderate"
        assert soils[0].soilgamdry == soilgamdryvalue

    @pytest.mark.unittest
    def test_default_soils_generated_unknown_model(self):
        from geolib.models.dfoundations.internal_soil import Soil

        soils = Soil.default_soils(model="Belgian")
        assert len(soils) == 0

    @pytest.mark.integrationtest
    def test_given_single_cpt_text_when_parse_cpt_then_structure_parsed(self):
        # 1. Define test data.
        text_to_parse = (
            ""
            + "[CPTNAME]\nFUGBEN1\n[END OF CPTNAME]\n"
            + "[PROJECT NAME]\nUnknown\n[END OF PROJECT NAME]\n"
            + "[PROJECTID]\n \n[END OF PROJECTID]\n"
            + "[PROJECT NUMBER]\n \n[END OF PROJECT NUMBER]\n"
            + "[PROJECT SUBNUMBER]\n \n[END OF PROJECT SUBNUMBER]\n"
            + "[LOCATION NAME]\nUnknown\n[END OF LOCATION NAME]\n"
            + "[CLIENT NAME]\nUnknown\n[END OF CLIENT NAME]\n"
            + "[COMPANYID]\nUnknown\n[END OF COMPANYID]\n"
            + "[FILEDATE]\n2001-11-01\n[END OF FILEDATE]\n"
            + "[FILEOWNER]\nUnknown\n[END OF FILEOWNER]\n"
            + "[GEF VERSION]\nUnknown\n[END OF GEF VERSION]\n"
            + "[PROCEDURECODE]\nUnknown\n[END OF PROCEDURECODE]\n"
            + "[ObjectID]\n0\n[END OF ObjectID]\n"
            + "[STARTDATE]\n2001-11-01\n[END OF STARTDATE]\n"
            + "[STARTTIME]\n \n[END OF STARTTIME]\n"
            + "[EXCAVATION TYPE]\n1 : Before\n[END OF EXCAVATION TYPE]\n"
            + "[TIMEORDER TYPE]\n1 : CPT - Excavation - Install\n[END OF TIMEORDER TYPE]\n"
            + "[CPT TYPE]\n1 : Electronic CPT\n[END OF CPT TYPE]\n"
            + "[USAGE CONE VALUE]\n0 : Mechanical qc required\n[END OF USAGE CONE VALUE]\n"
            + "[XY COORDINATE SYSTEM]\nUnknown\n[END OF XY COORDINATE SYSTEM]\n"
            + "[XWORLD]\n  987654321.000\n[END OF XWORLD]\n"
            + "[XWORLD ACCURACY]\n987654321.00000\n[END OF XWORLD ACCURACY]\n"
            + "[YWORLD]\n  987654321.000\n[END OF YWORLD]\n"
            + "[YWORLD ACCURACY]\n987654321.00000\n[END OF YWORLD ACCURACY]\n"
            + "[GROUNDLEVEL]\n          0.500\n[END OF GROUNDLEVEL]\n"
            + "[GROUNDLEVEL ACCURACY]\n987654321.00000\n[END OF GROUNDLEVEL ACCURACY]\n"
            + "[GROUNDLEVEL WAS MEASURED]\n1 : False\n[END OF GROUNDLEVEL WAS MEASURED]\n"
            + "[LEVELTEXT]\n \n[END OF LEVELTEXT]\n"
            + "[PRE EXCAVATION]\n  987654321.000\n[END OF PRE EXCAVATION]\n"
            + "[WATERLEVEL]\n  987654321.000\n[END OF WATERLEVEL]\n"
            + "[XLOCAL]\n          2.500\n[END OF XLOCAL]\n"
            + "[YLOCAL]\n         15.000\n[END OF YLOCAL]\n"
            + "[LOCAL X CROSSSECTION]\n          0.000\n[END OF LOCAL X CROSSSECTION]\n"
            + "[INTERPRETATION MODEL]\n0\n[END OF INTERPRETATION MODEL]\n"
            + "[INTERPRETATION MODEL STRESSDEPENDENT]\n0 : False\n[END OF INTERPRETATION MODEL STRESSDEPENDENT]\n"
            + "[DEPTHRANGE]\n          0.100\n[END OF DEPTHRANGE]\n"
            + "[GRAPH MAX PERCENTAGE]\n  10\n[END OF GRAPH MAX PERCENTAGE]\n"
            + "[GRAPH WIDTH]\n         10.000\n[END OF GRAPH WIDTH]\n"
            + "[GRAPH LINEWIDTH]\n   1\n[END OF GRAPH LINEWIDTH]\n"
            + "[GRAPH BORDERWIDTH]\n   1\n[END OF GRAPH BORDERWIDTH]\n"
            + "[GRAPH BORDERCOLOR]\n              0\n[END OF GRAPH BORDERCOLOR]\n"
            + "[GRAPH FRICTIONCOLOR]\n       16711680\n[END OF GRAPH FRICTIONCOLOR]\n"
            + "[GRAPH QCCOLOR]\n            255\n[END OF GRAPH QCCOLOR]\n"
            + "[GRAPH PLANE COLOR]\n              0\n[END OF GRAPH PLANE COLOR]\n"
            + "[GRAPH FIT FOR SIZE]\n0 : True\n[END OF GRAPH FIT FOR SIZE]\n"
            + "[GRAPH FIT SYMBOL FOR SIZE]\n0 : True\n[END OF GRAPH FIT SYMBOL FOR SIZE]\n"
            + "[GRAPH SYMBOL SIZE]\n          1.000\n[END OF GRAPH SYMBOL SIZE]\n"
            + "[VOID VALUE DEPTH]\n  987654321.000\n[END OF VOID VALUE DEPTH]\n"
            + "[VOID VALUE CONE RESISTANCE]\n  987654321.000\n[END OF VOID VALUE CONE RESISTANCE]\n"
            + "[VOID VALUE PORE WATER PRESSURE]\n987654321.000000\n[END OF VOID VALUE PORE WATER PRESSURE]\n"
            + "[VOID VALUE SLEEVE FRICTION]\n987654321.000000\n[END OF VOID VALUE SLEEVE FRICTION]\n"
            + "[VOID VALUE FRICTION NUMBER]\n987654321.000000\n[END OF VOID VALUE FRICTION NUMBER]\n"
            + "[VOID VALUE EQUIVALENT ELECTRONIC QC]\n987000000.000000\n[END OF VOID VALUE EQUIVALENT ELECTRONIC QC]\n"
            + "[MEASURED DATA]\n[TABLE]\n"
            + "[COLUMN INDICATION]\nz\nqc\n[END OF COLUMN INDICATION]\n"
            + "[DATA]\n"
            + "0.500        2.000\n"
            + "4.200        2.400\n"
            + "[END OF DATA]\n"
            + "[END OF TABLE]\n [END OF MEASURED DATA]"
        )
        # 2. Run test.
        parsed_cpt = CPT.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_cpt
        assert isinstance(parsed_cpt.measured_data, CPTMeasureData)
        assert len(parsed_cpt.measured_data.data) == 2


class TestInternalOutputDFoundations:
    @staticmethod
    def get_group_text(text: str) -> str:
        return "\n".join(text.split("\n")[1:-1])

    # region Fixtures
    input_data = "[INPUT DATA]\n" + "[END OF INPUT DATA]"

    nen_average_pile_factors = (
        "[NEN AVERAGE PILE FACTORS]\n"
        + "[TABLE]\n"
        + "[COLUMN INDICATION]\n"
        + "CptIndex\n"
        + "AlphaSGemSg\n"
        + "AlphaSGemClp\n"
        + "AlphaPGem\n"
        + "CptName\n"
        + "[END OF COLUMN INDICATION]\n"
        + "[DATA]\n"
        + "1  0.0060  0.0000  0.8000 'FUGBEN1'\n"
        + "2  0.0060  0.0200  0.8000 'FUGBEN2'\n"
        + "3  0.0060  0.0000  0.8000 'FUGBEN3'\n"
        + "[END OF DATA]\n"
        + "[END OF TABLE]\n"
        + "[END OF NEN AVERAGE PILE FACTORS]"
    )

    calculation_parameters_bearing_piles_ec_7 = (
        "[CALCULATION PARAMETERS BEARING PILES EC 7]\n"
        + "Ksi3Used = 1.3000\n"
        + "Ksi4Used = 1.3000\n"
        + "GammaBUsed = 1.2000\n"
        + "GammaSUsed = 1.2000\n"
        + "IsKsi3Used = 0\n"
        + "[END OF CALCULATION PARAMETERS BEARING PILES EC 7]"
    )

    cpts = (
        "[CPTS]\n"
        + "[TABLE]\n"
        + "[COLUMN INDICATION]\n"
        + "index\n"
        + "PPN\n"
        + "HNK\n"
        + "HPK\n"
        + "XCoordinate\n"
        + "YCoordinate\n"
        + "CptName\n"
        + "[END OF COLUMN INDICATION]\n"
        + "[DATA]\n"
        + "1    -24.00     -6.50    -17.00      2.50     15.00 'FUGBEN1'\n"
        + "2    -24.00     -6.50    -16.00     16.00      2.00 'FUGBEN2'\n"
        + "3    -24.00     -6.50    -16.00     32.50     15.00 'FUGBEN3'\n"
        + "[END OF DATA]\n"
        + "[END OF TABLE]\n"
        + "[END OF CPTS]"
    )

    max_shaft_and_point = (
        "[MAX SHAFT AND POINT]\n"
        + "[TABLE]\n"
        + "[COLUMN INDICATION]\n"
        + "CptIndex\n"
        + "Grenstoestand\n"
        + "MaxShaft\n"
        + "MaxPoint\n"
        + "[END OF COLUMN INDICATION]\n"
        + "[DATA]\n"
        + "1 GT1B   697.777  2253.992\n"
        + "2 GT1B   719.921  1644.805\n"
        + "3 GT1B   719.114  1385.901\n"
        + "1 GT2    837.332  2704.790\n"
        + "2 GT2    863.905  1973.766\n"
        + "3 GT2    862.937  1663.081\n"
        + "[END OF DATA]\n"
        + "[END OF TABLE]\n"
        + "[END OF MAX SHAFT AND POINT]"
    )

    nen_pile_results = (
        "[NEN PILE RESULTS]\n"
        + "1  pile count\n"
        + "3  cpt count\n"
        + "40  total number of piles in foundation plan\n"
        + f"{cpts}\n"
        + "1.00 = Pile point shape factor beta\n"
        + "1.00 = Factor influence crosssection of pile point s\n"
        + "1800.000 = Max load on foundation Fs_rep\n"
        + "2105.015 = Max bearing capacity foundation Fr;fund;max;d\n"
        + "6 = Critical pile nr for settlement in GT1B\n"
        + "3 = Critical CPT nr for settlement in GT1B\n"
        + "6 = Critical pile nr for settlement in GT2\n"
        + "3 = Critical CPT nr for settlement in GT2\n"
        + "4 = First pile nr for critical rotation in GT1B\n"
        + "7 = Second pile nr for critical rotation in GT1B\n"
        + "4 = First pile nr for critical rotation in GT2\n"
        + "7 = Second pile nr for critical rotation in GT2\n"
        + "1800.00000 = Fs_tot_d_1B\n"
        + "1385.90051 = Fr_max_punt_d_1B\n"
        + "719.11439 = Fr_max_schacht_d_1B\n"
        + "1080.90160 = FR_punt_d_1B\n"
        + "0.045820 = spunt_d_1B\n"
        + "0.00868 = sel_d1B\n"
        + "0.00871 = s2_d1B\n"
        + "0.00000 = sneg1B\n"
        + "1400.00000 = Fs_tot_d_2\n"
        + "1663.08061 = Fr_max_punt_d_2\n"
        + "862.93727 = Fr_max_schacht_d_2\n"
        + "677.32738 = FR_punt_d_2\n"
        + "0.01140 = spunt_d_2\n"
        + "0.00661 = sel_d2\n"
        + "0.00677 = s2_d2\n"
        + "0.00000 = sneg2\n"
        + f"{max_shaft_and_point}\n"
        + "7.576 = Sigma_max_schacht_1B\n"
        + "5.893 = Sigma_max_schacht_2\n"
        + "0.000 = Min value Fs;nk;d\n"
        + "0.000 = Max value Fs;nk;d\n"
        + f"{nen_average_pile_factors}\n"
        + f"{calculation_parameters_bearing_piles_ec_7}\n"
        + "[END OF NEN PILE RESULTS]"
    )

    global_nen_results = (
        "[GLOBAL NEN RESULTS]\n"
        + "0.063203 = wd1B\n"
        + "0.009173 = Betad1B\n"
        + "0.024783 = w2d\n"
        + "0.003441 = Betad2\n"
        + "[END OF GLOBAL NEN RESULTS]"
    )

    verification_results = (
        "[VERIFICATION RESULTS]\n"
        + f"{global_nen_results}\n"
        + "[DEMANDS NEN-EN]\n"
        + "0.066 = wreq1b\n"
        + "0.022 = wreq2\n"
        + "0 = Stiffness\n"
        + "0.010000 = Betadreq1B\n"
        + "1 = GT = 1B\n"
        + "0.003333 = Betadreq2\n"
        + "[END OF DEMANDS NEN-EN]\n"
        + f"{nen_pile_results}\n"
        + "[END OF VERIFICATION RESULTS]"
    )

    dumpfile_output = (
        "[DUMPFILE OUTPUT]\n"
        + "[RESULTS AT CPT TEST LEVEL]\n"
        + "[END OF RESULTS AT CPT TEST LEVEL]\n"
        + f"{verification_results}\n"
        + "[FOOTNOTE WARNINGS]\n"
        + "[END OF FOOTNOTE WARNINGS]\n"
        + "[END OF DUMPFILE OUTPUT]"
    )

    calculation_warnings = (
        "[CALCULATION WARNINGS]\n"
        + "1 = IsWarningF1Given (1=true, 0=false)\n"
        + "0 = F1GreaterThan1Found (1=true, 0=false)\n"
        + "0 = IsWarningNENDepthGiven (1=true, 0=false)\n"
        + "1 = IsWarningSFFundWidthGiven (1=true, 0=false)\n"
        + "0 = IsWarningSFFundLengthGiven (1=true, 0=false)\n"
        + "0 = IsWarningSFCudGiven (1=true, 0=false)\n"
        + "0 = IsWarningSFDeltaPhiGiven (1=true, 0=false)\n"
        + "12 = IsWarningNENSpacingGiven (> 0 warning, 0= no warning)\n"
        + "0 = IsWarningSFSlopeNotRelevantGiven (1=true, 0=false)\n"
        + "0 = IsWarningNENSFPlacementDepthTooDeep (1=true, 0=false)\n"
        + "0 = IsWarningNENSFPlacementDepthTooShallow (1=true, 0=false)\n"
        + "[END OF CALCULATION WARNINGS]"
    )

    dfoundations_structure_text = (
        "[DUMPFILE]\n"
        + f"{input_data}\n"
        + f"{dumpfile_output}\n"
        + f"{calculation_warnings}\n"
        + "[END OF DUMPFILE]"
    )

    # endregion

    @pytest.mark.integrationtest
    def test_given_calculation_warnings_text_when_parse_then_returns_structure(self):
        # 1. Get test text.
        group_text = self.get_group_text(self.calculation_warnings)

        # 2. Parse.
        parsed_warnings = DFoundationsCalculationWarnings.parse_text(group_text)

        # 3. Verify expectations.
        assert parsed_warnings
        assert parsed_warnings.is_warning_f1_given
        assert not parsed_warnings.f1_greater_than_1_found
        assert parsed_warnings.is_warning_sf_fund_width_given
        assert parsed_warnings.is_warning_nen_spacing_given == 12

    @pytest.mark.integrationtest
    def test_given_nen_average_pile_factors_text_when_parse_then_returns_structure(self):
        # 1. Set up test data
        group_text = self.get_group_text(self.nen_average_pile_factors)
        first_expected_value = {
            "CptIndex": 1,
            "AlphaSGemSg": 0.0060,
            "AlphaSGemClp": 0.0000,
            "AlphaPGem": 0.8000,
            "CptName": "'FUGBEN1'",
        }
        # 2. Run test
        parsed_structure = DFoundationsNenPileResultsTable.parse_text(group_text)

        # 3. Verify final expectations.
        assert parsed_structure
        assert len(parsed_structure.data) == 3
        assert parsed_structure.data[0] == first_expected_value

    @pytest.mark.integrationtest
    def test_given_max_shaft_and_point_text_when_parse_then_returns_structure(self):
        # 1. Set up test data
        group_text = self.get_group_text(self.max_shaft_and_point)
        first_expected_value = {
            "CptIndex": 1,
            "Grenstoestand": "GT1B",
            "MaxShaft": 697.777,
            "MaxPoint": 2253.992,
        }
        # 2. Run test
        parsed_structure = DFoundationsNenPileResultsTable.parse_text(group_text)

        # 3. Verify final expectations.
        assert parsed_structure
        assert len(parsed_structure.data) == 6
        assert parsed_structure.data[0] == first_expected_value

    @pytest.mark.integrationtest
    def test_given_cpt_text_when_parse_then_returns_structure(self):
        # 1. Set up test data
        group_text = self.get_group_text(self.cpts)
        first_expected_value = {
            "index": 1,
            "PPN": -24.00,
            "HNK": -6.5,
            "HPK": -17.00,
            "XCoordinate": 2.50,
            "YCoordinate": 15.00,
            "CptName": "'FUGBEN1'",
        }
        # 2. Run test
        parsed_structure = DFoundationsNenPileResultsTable.parse_text(group_text)

        # 3. Verify final expectations.
        assert parsed_structure
        assert len(parsed_structure.data) == 3
        assert parsed_structure.data[0] == first_expected_value

    @pytest.mark.integrationtest
    def test_given_nen_pile_results_text_when_parse_then_returns_structure(self):
        # 1. Set up test data.
        group_text = self.get_group_text(self.nen_pile_results)

        # 2. Parse text.
        parsed_structure = DFoundationsNenPileResults.parse_text(group_text)

        # 3. Verify final expectations.
        assert parsed_structure

    @pytest.mark.integrationtest
    def test_given_global_nen_results_when_parse_then_returns_structure(self):
        # 1. Set up test data
        group_text = self.get_group_text(self.global_nen_results)
        # 2. Parse text.
        parsed_structure = DFoundationsGlobalNenResults.parse_text(group_text)
        # 3. Verify results
        assert parsed_structure.wd1b == 0.063203
        assert parsed_structure.betad1b == 0.009173
        assert parsed_structure.w2d == 0.024783
        assert parsed_structure.betad2 == 0.003441

    @pytest.mark.integrationtest
    def test_given_calculation_parameters_bearing_piles_ec_7_when_parse_then_returns_structure(
        self,
    ):
        # 1. Set up test data
        group_text = self.get_group_text(self.calculation_parameters_bearing_piles_ec_7)

        # 2. Parse text data.
        parsed_structure = DFoundationsCalculationParametersBearingPilesEC7.parse_text(
            group_text
        )

        # 3. Verify results.
        assert parsed_structure.ksi3used == 1.3
        assert parsed_structure.ksi4used == 1.3
        assert parsed_structure.gammabused == 1.2
        assert parsed_structure.gammasused == 1.2
        assert parsed_structure.isksi3used is False

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse, property_name, parsing_type, expected_type",
        [
            pytest.param(
                dfoundations_structure_text,
                "calculation_warnings",
                DFoundationsStructure,
                DFoundationsCalculationWarnings,
                id="Calculation Warnings",
            ),
            pytest.param(
                dfoundations_structure_text,
                "dumpfile_output",
                DFoundationsStructure,
                DFoundationsDumpfileOutputStructure,
                id="Dumpfile Output",
            ),
            pytest.param(
                dumpfile_output,
                "verification_results",
                DFoundationsDumpfileOutputStructure,
                DFoundationsVerificationResults,
                id="Verification results",
            ),
            pytest.param(
                verification_results,
                "nen_pile_results",
                DFoundationsVerificationResults,
                DFoundationsNenPileResults,
                id="Nen Pile results",
            ),
            pytest.param(
                verification_results,
                "global_nen_results",
                DFoundationsVerificationResults,
                DFoundationsGlobalNenResults,
                id="Global Nen Results",
            ),
            pytest.param(
                nen_pile_results,
                "nen_average_pile_factors",
                DFoundationsNenPileResults,
                DFoundationsNenPileResultsTable,
                id="Nen Average Pile results",
            ),
            pytest.param(
                nen_pile_results,
                "cpts",
                DFoundationsNenPileResults,
                DFoundationsNenPileResultsTable,
                id="CPTs",
            ),
            pytest.param(
                nen_pile_results,
                "max_shaft_and_point",
                DFoundationsNenPileResults,
                DFoundationsNenPileResultsTable,
                id="Max Shaft And Point",
            ),
            pytest.param(
                nen_pile_results,
                "calculation_parameters_bearing_piles_ec_7",
                DFoundationsNenPileResults,
                DFoundationsCalculationParametersBearingPilesEC7,
                id="Calculation parameters bearing piles EC7",
            ),
        ],
    )
    def test_given_all_dfoundationsstructure_fixtures_when_parse_dfoundationtype_then_returns_as_property(
        self,
        text_to_parse: str,
        property_name: str,
        parsing_type: Type,
        expected_type: Type,
    ):
        # 1. Run test
        group_text = self.get_group_text(text_to_parse)

        # 2. Parse text.
        parsed_text = parsing_type.parse_text(group_text)

        # 3. Verify results
        assert parsed_text is not None
        parsed_dict = dict(parsed_text)
        assert isinstance(parsed_dict[property_name], expected_type)
