import warnings
from typing import Callable, List

import pytest

import geolib.models.dsheetpiling.settings as settings
from geolib.geometry import Point
from geolib.models.dseries_parser import DSeriesStructure
from geolib.models.dsheetpiling.calculation_options import CalculationOptionsPerStage
from geolib.models.dsheetpiling.constructions import Sheet, SheetPileProperties
from geolib.models.dsheetpiling.internal import (
    Anchor,
    AnchorData,
    Anchors,
    BaseVerificationStructureProperties,
    BreukData,
    CalculationOptions,
    DesignLengthCalculation,
    DesignLengthInfo,
    DesignSheetpileLength,
    DSheetPilingInputStructure,
    DSheetPilingOutputStructure,
    Model,
    MomentsForcesDisplacements,
    OutputConstructionStage,
    PointsOnSheetpile,
    Pressures,
    Resume,
    SheetPileElement,
    SheetPiling,
    SideOutput,
    StageOptions,
    Strut,
    Struts,
    SurchargeLoad,
    SurchargeLoads,
    SurchargePoint,
    UniformLoad,
    UniformLoads,
    VerifyAnchorForce,
    VerifySheetpileData,
)
from geolib.models.dsheetpiling.settings import SheetPilingElementMaterialType


@pytest.fixture
def model() -> DSheetPilingInputStructure:
    model = DSheetPilingInputStructure()
    model.add_stage(
        name="Initial stage",
        passive_side=settings.PassiveSide.DSHEETPILING_DETERMINED,
        method_left=settings.LateralEarthPressureMethodStage.KA_KO_KP,
        method_right=settings.LateralEarthPressureMethodStage.KA_KO_KP,
        pile_top_displacement=0.0,
    )
    return model


class TestInternal:
    @pytest.mark.integrationtest
    def test_update_arguments_if_invalid_input(self):
        # create sheet pile element
        sheet_piling_element = SheetPileElement(
            sheetpilingelementkmod=0.1,
            sheetpilingelementmaterialfactor=0.3,
            sheetpilingelementmaterialtype=SheetPilingElementMaterialType.Concrete,
        )
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            sheet_piling_element.update_arguments_if_invalid_input()
            assert len(w) == 2
            assert issubclass(w[0].category, ImportWarning)
            assert "Inputed value for kmod was not valid and was change to 1" in str(
                w[0].message
            )
            assert issubclass(w[1].category, ImportWarning)
            assert (
                "Inputed value for material factor was not valid and was change to 1.1"
                in str(w[1].message)
            )
        assert sheet_piling_element.sheetpilingelementkmod == 1
        assert sheet_piling_element.sheetpilingelementmaterialfactor == 1.1

    @pytest.mark.integrationtest
    def test_set_construction(self):
        # create sheet pile element and point
        sheet1 = Sheet(name="First inputted pile")
        sheet1.sheet_pile_properties = SheetPileProperties(section_bottom_level=-2)
        top_level = 1

        # initial expectations checked
        assert top_level
        assert sheet1

        # run test
        model = DSheetPilingInputStructure()
        internal = sheet1.to_internal()
        model.set_construction(elements=[internal], top_level=top_level)
        assert model.sheet_piling.lengthsheetpiling == 3
        assert model.sheet_piling.leveltopsheetpiling == top_level

    def test_set_construction_no_elements_raises_value_error(self):
        model = DSheetPilingInputStructure()
        with pytest.raises(ValueError, match="At least one sheet should be provided"):
            model.set_construction(elements=[], top_level=0)

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_cur(
        self, model: DSheetPilingInputStructure
    ):
        # set inputs
        calc_options_per_stage = CalculationOptionsPerStage(
            anchor_factor=1.5, partial_factor_set=settings.PartialFactorSetCUR.CLASSIII
        )
        # test initial expectations
        assert model
        assert calc_options_per_stage
        assert model.calculation_options.verifytype == settings.VerifyType.CUR
        # run test
        model.add_calculation_options_per_stage(
            input_calc_options=calc_options_per_stage, stage_id=0
        )
        # test output
        assert len(model.calculation_options_per_stage.stageoptions) == 1
        assert (
            model.calculation_options_per_stage.stageoptions[0].stagepartialfactorsetcur
            == settings.PartialFactorSetCUR.CLASSIII
        )
        assert model.calculation_options_per_stage.stageoptions[0].stageverify == 1
        assert (
            model.calculation_options_per_stage.stageoptions[0].stageanchorfactor == 1.5
        )

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_ec7_nl(
        self, model: DSheetPilingInputStructure
    ):
        # set inputs
        model.calculation_options.verifytype = settings.VerifyType.EC7NL

        calc_options_per_stage = CalculationOptionsPerStage(
            anchor_factor=1.5, partial_factor_set=settings.PartialFactorSetEC7NADNL.RC2
        )
        # test initial expectations
        assert model
        assert calc_options_per_stage
        assert model.calculation_options.verifytype == settings.VerifyType.EC7NL
        # run test
        model.add_calculation_options_per_stage(
            input_calc_options=calc_options_per_stage, stage_id=0
        )
        # test output
        assert len(model.calculation_options_per_stage.stageoptions) == 1
        assert (
            model.calculation_options_per_stage.stageoptions[
                0
            ].stagepartialfactorsetec7nadnl
            == settings.PartialFactorSetEC7NADNL.RC2
        )
        assert (
            model.calculation_options_per_stage.stageoptions[0].stageverifyec7nadnl == 1
        )
        assert (
            model.calculation_options_per_stage.stageoptions[0].stageanchorfactorec7nadnl
            == 1.5
        )

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_ec7_b(
        self, model: DSheetPilingInputStructure
    ):
        # set inputs
        model.calculation_options.verifytype = settings.VerifyType.EC7BE

        calc_options_per_stage = CalculationOptionsPerStage(anchor_factor=1.5)
        # test initial expectations
        assert model
        assert calc_options_per_stage
        assert model.calculation_options.verifytype == settings.VerifyType.EC7BE
        # run test
        model.add_calculation_options_per_stage(
            input_calc_options=calc_options_per_stage, stage_id=0
        )
        # test output
        assert len(model.calculation_options_per_stage.stageoptions) == 1
        assert model.calculation_options_per_stage.stageoptions[0].stageverifyec7nadb == 1


class TestInternalParseInputStructure:
    @staticmethod
    def get_group_text(text: str) -> str:
        return "\n".join(text.split("\n")[1:-1])

    text_uniform_load = """[LOAD]
        Uniform load = 10 kN/m2
        UniformLoadLeft=10.00
        UniformLoadRight=10.00
        UniformLoadPermanent=0
        UniformLoadFavourable=0
        UniformLoadStandardDeviationLeft=0.00
        UniformLoadStandardDeviationRight=0.00
        UniformLoadDistLeft=2
        UniformLoadDistRight=2
        [END OF LOAD]"""
    text_uniform_loads = (
        "[UNIFORM LOADS]\n" + "1 = number of items\n"
        f"{text_uniform_load}\n" + "[END OF UNIFORM LOADS]"
    )

    text_surcharge_load = """[LOAD]
        Surcharge Load
        2
        [POINT]
        SurchargeLoadDistance=0.00
        SurchargeLoadValue=3.00
        [END OF POINT]
        [POINT]
        SurchargeLoadDistance=100.00
        SurchargeLoadValue=3.00
        [END OF POINT]
        SurchargeLoadPermanent=0
        SurchargeLoadFavourable=0
        SurchargeLoadStandardDeviation=0.00
        SurchargeLoadDistribution=2
        [END OF LOAD]"""

    text_surcharge_loads = (
        "[SURCHARGE LOADS]\n"
        + "1 = number of items\n"
        + f"{text_surcharge_load}\n"
        + "[END OF SURCHARGE LOADS]"
    )

    @pytest.mark.integrationtest
    def test_given_uniform_load_text_when_parse_text_then_returns_structure(self):
        # 1. Define test data.
        group_load = self.get_group_text(self.text_uniform_load)

        # 2. Run test.
        parsed_structure = UniformLoad.parse_text(group_load)

        # 3. Verify final expectations.
        self.__verify_expected_uniform_load(parsed_structure)

    @pytest.mark.integrationtest
    def test_given_uniform_loads_text_when_parse_text_then_returns_structure(self):
        # 1. Define test data.
        group_load = self.get_group_text(self.text_uniform_loads)

        # 2. Run test.
        parsed_structure = UniformLoads.parse_text(group_load)

        # 3. Verify final expectations.
        assert parsed_structure is not None
        assert len(parsed_structure.loads) == 1
        self.__verify_expected_uniform_load(parsed_structure.loads[0])

    @pytest.mark.integrationtest
    def test_given_surcharge_load_text_when_parse_text_then_returns_structure(self):
        # 1. Define test data
        group_load = self.get_group_text(self.text_surcharge_load)
        # 2. Run test
        parsed_structure = SurchargeLoad.parse_text(group_load)
        # 3. Verify final expectations
        self.__verify_expected_surcharge_load(parsed_structure)

    @pytest.mark.integrationtest
    def test_given_surcharge_loads_text_when_parse_text_then_returns_structure(self):
        # 1. Define test data
        group_load = self.get_group_text(self.text_surcharge_loads)
        # 2. Run test
        parsed_structure = SurchargeLoads.parse_text(group_load)
        # 3. Verify final expectations
        assert parsed_structure
        assert len(parsed_structure.loads) == 1
        self.__verify_expected_surcharge_load(parsed_structure.loads[0])

    @pytest.mark.integrationtest
    def test_given_surcharge_load_with_equal_separator_when_parse_text_then_returns_structure(
        self,
    ):
        # 1. Define test data
        text_to_parse = """Surcharge load = 3
            2
            [POINT]
            SurchargeLoadDistance=0.00
            SurchargeLoadValue=3.00
            [END OF POINT]
            [POINT]
            SurchargeLoadDistance=10000.00
            SurchargeLoadValue=3.00
            [END OF POINT]
            SurchargeLoadPermanent=0
            SurchargeLoadFavourable=2
            SurchargeLoadStandardDeviation=0.00
            SurchargeLoadDistribution=2"""

        # 2. Define test action.
        parsed_structure = SurchargeLoad.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_structure

    @pytest.mark.integrationtest
    def test_given_resume_text_when_parse_text_then_returns_structure(self):
        # 1. Define test data.
        column_values = {
            "moment": 11.64788,
            "shear_force": -5.00187,
            "displacements": 117.98290,
            "perc__mob__moment": 0,
            "perc__mob__resistances": 6.97007,
            "fase": 1,
            "verification_type": 15,
            "partial_factor_type": 4,
            "vertical_balance_result": 0,
            "vertical_result_direction": 0,
            "status": 0,
        }
        column_keys_line = "\n".join(column_values.keys())
        column_values_line = "\t".join([str(value) for value in column_values.values()])
        text_to_parse = f"""
            1 : Number of stages
            [TABLE]
            [COLUMN INDICATION]
            {column_keys_line}
            [END OF COLUMN INDICATION]
            [COLUMN DATA]
                {column_values_line}
            [END OF COLUMN DATA]
            [END OF TABLE]
        """
        # 2. Run test
        resume_structure = Resume.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert resume_structure is not None
        assert len(resume_structure.resume) == 1
        assert resume_structure.resume[0].keys() == column_values.keys()
        for key, value in resume_structure.resume[0].items():
            assert (
                value == column_values[key]
            ), f"Values don't match for column: {key} ({value} but should be {column_values[key]})"

    text_model = """0 : Sheet piling
        0 : Ka, Ko, Kp soil parameters
        0 : Verification = FALSE
        0 : EC7-SE visible = FALSE
        0 : Pile loaded by forces
        0 : Pile loaded by user defined soil displacements
        0 : Probabilistic = FALSE
        0 : Check vertical balance = FALSE
        0 : Trildens calculation = FALSE
        0 : Diepwand calculation = FALSE
        1 : Elastic calculation = TRUE
        0 : Wooden sheet piling = FALSE"""

    text_strut = """1 -10.00  4.2  4.2  4.2 4.2 4.2 2 Strut"""

    text_struts = f"""1 Number of struts  
    Nr        Level        E-mod     Cross sect.    Length     YieldF   Side 
    {text_strut}"""

    text_anchor = """1  -2.00  2.4  2.4 2.4 2.4 2.4 2.4 2 Short anchor"""

    text_anchors = f"""1 Number of anchors
    Nr  Level        E-mod  Cross sect.   Length   YieldF    Angle   Height   Side Name
    {text_anchor}"""

    text_breuk_data = """22.11 : Percentage mobilized resistance left
            8.36 : Percentage mobilized resistance right
            329.04 : Effective left
            329.13 : Effective right
            961.38 : Water pressure left
            961.38 : Water pressure right
            1488.18 : Max passive effect. resistance left
            3939.32 : Max passive effect. resistance right
            0.00 : Max passive moment left
            0.00 : Max passive moment right
            0.00 : Max mobilized passive moment left
            0.00 : Max mobilized passive moment right
            93.87 : Vertical force left
            88.75 : Vertical force right
            0.00 : Level of single support
            1 : Node of single support
            0 : Moment present
            1 : Active side"""

    text_anchor_data = """1 : Number of anchors
        [TABLE]
        [COLUMN INDICATION]
        Node number
        Position
        Force
        E modulus
        Status
        Side
        AnchorType
        AnchorName
        [END OF COLUMN INDICATION]
        [DATA]
            7     -2.00000     17.97193     190000000.000     1     2     0 AnchorName
        [END OF DATA]
        [END OF TABLE]"""

    text_moment_forces_displacements = """[TABLE]
            [COLUMN INDICATION]
            Moment
            Shear force
            Displacements
            [END OF COLUMN INDICATION]
            [DATA]
                0.00000      0.00000   -193.89808
            [END OF DATA]
            [END OF TABLE]
            """

    text_pressures = """1 : Number of nodes
        [TABLE]
        [COLUMN INDICATION]
        Horizontal pressure
        Pore pressure
        Passive pressure
        Neutral pressure
        Status on branches
        Percentage of mobilisation
        Status character
        [END OF COLUMN INDICATION]
        [DATA]
            0.09882      0.00000     10.14826      2.20017            1   0 A
        [END OF DATA]
        [END OF TABLE]"""

    not_parsable_struct = "not parsable yet"

    text_side_left = f"""Leftside
        [CALCULATION METHOD]
        {not_parsable_struct}
        [END OF CALCULATION METHOD]
        [WATER LEVEL]
        {not_parsable_struct}
        [END OF WATER LEVEL]
        [SURFACE]
        {not_parsable_struct}
        [END OF SURFACE]
        [SOIL PROFILE FOR SHEET PILING MODEL]
        {not_parsable_struct}
        [END OF SOIL PROFILE FOR SHEET PILING MODEL]
        [PRESSURES]
        {text_pressures}
        [END OF PRESSURES]
        [FORCE FROM LAYER]
        {not_parsable_struct}
        [END OF FORCE FROM LAYER]
        """
    text_side_right = f"""Rightside
        [CALCULATION METHOD]
        {not_parsable_struct}
        [END OF CALCULATION METHOD]
        [WATER LEVEL]
        {not_parsable_struct}
        [END OF WATER LEVEL]
        [SURFACE]
        {not_parsable_struct}
        [END OF SURFACE]
        [SOIL PROFILE FOR SHEET PILING MODEL]
        {not_parsable_struct}
        [END OF SOIL PROFILE FOR SHEET PILING MODEL]
        [PRESSURES]
        {text_pressures}
        [END OF PRESSURES]
        [FORCE FROM LAYER]
        {not_parsable_struct}
        [END OF FORCE FROM LAYER]
        """

    text_output_construction_stage = f"""1 : Construction stage number
        [BREUK DATA]
        {text_breuk_data}
        [END OF BREUK DATA]
        [ANCHOR DATA]
        {text_anchor_data}
        [END OF ANCHOR DATA]
        [MOMENTS FORCES DISPLACEMENTS]
        {text_moment_forces_displacements}
        [END OF MOMENTS FORCES DISPLACEMENTS]
        [SIDE]
        {text_side_left}
        [END OF SIDE]
        [SIDE]
        {text_side_right}
        [END OF SIDE]
        """

    def validate_anchor(self, anchor: Anchor):
        assert anchor
        assert anchor.name == "Short anchor"
        assert anchor.level == -2.00
        assert anchor.e_modulus == 2.4
        assert anchor.cross_section == 2.4
        assert anchor.wall_height_kranz == 2.4
        assert anchor.length == 2.4
        assert anchor.angle == 2.4
        assert anchor.yield_force == 2.4
        assert anchor.side == 2

    def validate_anchors(self, anchor_list: Anchors):
        assert anchor_list
        assert len(anchor_list.anchors) == 1
        self.validate_anchor(anchor_list.anchors[0])

    def validate_strut(self, strut: Strut):
        assert strut
        assert strut.name == "Strut"
        assert strut.level == -10.00
        assert strut.e_modulus == 4.2
        assert strut.cross_section == 4.2
        assert strut.length == 4.2
        assert strut.angle == 4.2
        assert strut.buckling_force == 4.2
        assert strut.side == 2

    def validate_struts(self, strut_list: Struts):
        assert strut_list
        assert len(strut_list.struts) == 1
        self.validate_strut(strut_list.struts[0])

    def validate_model_structure(self, model: Model):
        assert model
        assert model.model == 0
        assert model.method == 0
        assert model.verification is False
        assert model.ec7se_visible is False
        assert model.pile_load_option is False
        assert model.probabilistic is False
        assert model.check_vertical_balance is False
        assert model.trildens_calculation is False
        assert model.diepwand_calculation is False
        assert model.elastic_calculation is True
        assert model.wooden_sheetpiling is False

    def validate_pressures_structure(self, pressures: Pressures):
        assert pressures
        assert len(pressures.pressures) == 1
        p_table = pressures.pressures[0]
        assert p_table["horizontal_pressure"] == 0.09882
        assert p_table["pore_pressure"] == 0
        assert p_table["passive_pressure"] == 10.14826
        assert p_table["neutral_pressure"] == 2.20017
        assert p_table["status_on_branches"] == 1
        assert p_table["percentage_of_mobilisation"] == 0
        assert p_table["status_character"] == "A"

    def validate_side_structure(self, side_output: SideOutput):
        assert side_output
        assert side_output.calculation_method == self.not_parsable_struct
        assert side_output.water_level == self.not_parsable_struct
        assert side_output.surface == self.not_parsable_struct
        assert side_output.soil_profile_for_sheet_piling_model == self.not_parsable_struct
        self.validate_pressures_structure(side_output.pressures)
        assert side_output.force_from_layer == self.not_parsable_struct

    def validate_breuk_data_structure(self, breuk_data: BreukData):
        assert breuk_data is not None
        assert breuk_data.percentage_mobilized_resistance_left == 22.11
        assert breuk_data.percentage_mobilized_resistance_right == 8.36
        assert breuk_data.effective_left == 329.04
        assert breuk_data.effective_right == 329.13
        assert breuk_data.water_pressure_left == 961.38
        assert breuk_data.water_pressure_right == 961.38
        assert breuk_data.max_passive_effect_resistance_left == 1488.18
        assert breuk_data.max_passive_effect_resistance_right == 3939.32
        assert breuk_data.max_passive_moment_left == 0
        assert breuk_data.max_passive_moment_right == 0
        assert breuk_data.max_mobilized_passive_moment_left == 0
        assert breuk_data.max_mobilized_passive_moment_right == 0
        assert breuk_data.vertical_force_left == 93.87
        assert breuk_data.vertical_force_right == 88.75
        assert breuk_data.level_of_single_support == 0
        assert breuk_data.node_of_single_support == 1
        assert breuk_data.moment_present == 0
        assert breuk_data.active_side == 1

    def validate_anchor_data_structure(self, anchor_data: AnchorData):
        assert anchor_data
        assert len(anchor_data.anchordata) == 1
        ad_table = anchor_data.anchordata[0]
        assert ad_table["node_number"] == 7
        assert ad_table["position"] == -2
        assert ad_table["force"] == 17.97193
        assert ad_table["e_modulus"] == 190000000
        assert ad_table["status"] == 1
        assert ad_table["side"] == 2
        assert ad_table["anchortype"] == 0
        assert ad_table["anchorname"] == "AnchorName"

    def validate_moment_force_displacements_structure(
        self, mfd_data: MomentsForcesDisplacements
    ):
        assert mfd_data
        assert len(mfd_data.momentsforcesdisplacements) == 1
        mfd_table = mfd_data.momentsforcesdisplacements[0]
        assert mfd_table["moment"] == 0
        assert mfd_table["shear_force"] == 0
        assert mfd_table["displacements"] == -193.89808

    def validate_side_list_structure(self, side_list: List[SideOutput]):
        assert side_list
        assert len(side_list) == 2
        for side in side_list:
            self.validate_side_structure(side)

    def validate_output_construction_stage(
        self, output_construction_stage: OutputConstructionStage
    ):
        # 3. Validate final expectations.
        assert isinstance(output_construction_stage, OutputConstructionStage)
        self.validate_breuk_data_structure(output_construction_stage.breuk_data)
        self.validate_anchor_data_structure(output_construction_stage.anchor_data)
        self.validate_moment_force_displacements_structure(
            output_construction_stage.moments_forces_displacements
        )
        self.validate_side_list_structure(output_construction_stage.side)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse, internal_type, validation_method",
        (
            [
                pytest.param(text_model, Model, validate_model_structure, id="Model"),
                pytest.param(text_strut, Strut, validate_strut, id="Strut"),
                pytest.param(text_struts, Struts, validate_struts, id="Struts"),
                pytest.param(text_anchor, Anchor, validate_anchor, id="Anchor"),
                pytest.param(text_anchors, Anchors, validate_anchors, id="Anchors"),
                pytest.param(
                    text_breuk_data,
                    BreukData,
                    validate_breuk_data_structure,
                    id="Breuk Data",
                ),
                pytest.param(
                    text_anchor_data,
                    AnchorData,
                    validate_anchor_data_structure,
                    id="Anchor Data",
                ),
                pytest.param(
                    text_moment_forces_displacements,
                    MomentsForcesDisplacements,
                    validate_moment_force_displacements_structure,
                    id="Moment Force Displacements",
                ),
                pytest.param(
                    text_output_construction_stage,
                    OutputConstructionStage,
                    validate_output_construction_stage,
                    id="Output Construction Stage",
                ),
                pytest.param(
                    text_pressures,
                    Pressures,
                    validate_pressures_structure,
                    id="Pressures",
                ),
                pytest.param(
                    text_side_left,
                    SideOutput,
                    validate_side_structure,
                    id="Side Output (Leftside)",
                ),
            ]
        ),
    )
    def test_given_construction_stage_inner_structure_when_parse_text_then_returns_structure(
        self,
        text_to_parse: str,
        internal_type: DSeriesStructure,
        validation_method: Callable[[DSeriesStructure], None],
    ):
        # 1. Run test
        parsed_structure = internal_type.parse_text(text_to_parse)
        # 2. Validate
        validation_method(self, parsed_structure)

    def __verify_expected_surcharge_load(self, parsed_load: SurchargeLoad):
        assert parsed_load.name == "Surcharge Load"
        assert len(parsed_load.points) == 2
        assert parsed_load.points[0].surchargeloaddistance == 0
        assert parsed_load.points[0].surchargeloadvalue == 3
        assert parsed_load.points[1].surchargeloaddistance == 100
        assert parsed_load.points[1].surchargeloadvalue == 3
        assert parsed_load.surchargeloadpermanent == 0
        assert parsed_load.surchargeloadfavourable == 0
        assert parsed_load.surchargeloadstandarddeviation == 0
        assert parsed_load.surchargeloaddistribution == 2

    def __verify_expected_uniform_load(self, parsed_load: UniformLoad):
        assert parsed_load
        assert parsed_load.name == "Uniform load = 10 kN/m2"
        assert parsed_load.uniformloadleft == 10
        assert parsed_load.uniformloadright == 10
        assert parsed_load.uniformloadpermanent == 0
        assert parsed_load.uniformloadfavourable == 0
        assert parsed_load.uniformloadstandarddeviationleft == 0
        assert parsed_load.uniformloadstandarddeviationright == 0
        assert parsed_load.uniformloaddistleft == 2
        assert parsed_load.uniformloaddistright == 2

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse, property_name, assert_func",
        [
            pytest.param(
                text_uniform_loads, "uniform_loads", __verify_expected_uniform_load
            ),
            pytest.param(
                text_surcharge_loads, "surcharge_loads", __verify_expected_surcharge_load
            ),
        ],
    )
    def test_given_sheetpilingtext_when_parse_text_then_returns_structure_with_loads(
        self, text_to_parse: str, property_name: str, assert_func
    ):
        parsed_structure = DSheetPilingInputStructure.parse_text(text_to_parse)
        assert_func(self, dict(parsed_structure)[property_name].loads[0])


class TestInternalParseOutputStructure:
    # region Output text
    not_parsable_struct = "not parsable yet"

    text_calculation_type = """Test output dump structure"""

    text_resume_structure = """
        1 : Number of stages
        [TABLE]
        [COLUMN INDICATION]
        Moment
        Shear force
        Displacement
        Percentage mobilized moment
        Percentage mobilized resistance
        Stage
        Verification type
        Partial factor type
        Vertical balance result
        Vertical result direction
        Status
        [END OF COLUMN INDICATION]
        [COLUMN DATA]
        11.64788     -5.00187    117.98290      0.00000      6.97007     1    15     4 0 0     0
        [END OF COLUMN DATA]
        [END OF TABLE]"""

    text_breuk_data = """22.11 : Percentage mobilized resistance left
            8.36 : Percentage mobilized resistance right
            329.04 : Effective left
            329.13 : Effective right
            961.38 : Water pressure left
            961.38 : Water pressure right
            1488.18 : Max passive effect. resistance left
            3939.32 : Max passive effect. resistance right
            0.00 : Max passive moment left
            0.00 : Max passive moment right
            0.00 : Max mobilized passive moment left
            0.00 : Max mobilized passive moment right
            93.87 : Vertical force left
            88.75 : Vertical force right
            0.00 : Level of single support
            1 : Node of single support
            0 : Moment present
            1 : Active side"""

    text_anchor_data = """1 : Number of anchors
        [TABLE]
        [COLUMN INDICATION]
        Node number
        Position
        Force
        E modulus
        Status
        Side
        AnchorType
        AnchorName
        [END OF COLUMN INDICATION]
        [DATA]
            7     -2.00000     17.97193     190000000.000     1     2     0 AnchorName
        [END OF DATA]
        [END OF TABLE]"""

    text_moment_forces_displacements = """[TABLE]
            [COLUMN INDICATION]
            Moment
            Shear force
            Displacements
            [END OF COLUMN INDICATION]
            [DATA]
                0.00000      0.00000   -193.89808
            [END OF DATA]
            [END OF TABLE]
            """

    text_pressures = """1 : Number of nodes
        [TABLE]
        [COLUMN INDICATION]
        Horizontal pressure
        Pore pressure
        Passive pressure
        Neutral pressure
        Status on branches
        Percentage of mobilisation
        Status character
        [END OF COLUMN INDICATION]
        [DATA]
            0.09882      0.00000     10.14826      2.20017            1   0 A
        [END OF DATA]
        [END OF TABLE]"""

    text_side_left = f"""Leftside
        [CALCULATION METHOD]
        {not_parsable_struct}
        [END OF CALCULATION METHOD]
        [WATER LEVEL]
        {not_parsable_struct}
        [END OF WATER LEVEL]
        [SURFACE]
        {not_parsable_struct}
        [END OF SURFACE]
        [SOIL PROFILE FOR SHEET PILING MODEL]
        {not_parsable_struct}
        [END OF SOIL PROFILE FOR SHEET PILING MODEL]
        [PRESSURES]
        {text_pressures}
        [END OF PRESSURES]
        [FORCE FROM LAYER]
        {not_parsable_struct}
        [END OF FORCE FROM LAYER]
        """

    text_side_right = f"""Rightside
        [CALCULATION METHOD]
        {not_parsable_struct}
        [END OF CALCULATION METHOD]
        [WATER LEVEL]
        {not_parsable_struct}
        [END OF WATER LEVEL]
        [SURFACE]
        {not_parsable_struct}
        [END OF SURFACE]
        [SOIL PROFILE FOR SHEET PILING MODEL]
        {not_parsable_struct}
        [END OF SOIL PROFILE FOR SHEET PILING MODEL]
        [PRESSURES]
        {text_pressures}
        [END OF PRESSURES]
        [FORCE FROM LAYER]
        {not_parsable_struct}
        [END OF FORCE FROM LAYER]
        """

    text_output_construction_stage = f"""1 : Construction stage number
        [BREUK DATA]
        {text_breuk_data}
        [END OF BREUK DATA]
        [ANCHOR DATA]
        {text_anchor_data}
        [END OF ANCHOR DATA]
        [MOMENTS FORCES DISPLACEMENTS]
        {text_moment_forces_displacements}
        [END OF MOMENTS FORCES DISPLACEMENTS]
        [SIDE]
        {text_side_left}
        [END OF SIDE]
        [SIDE]
        {text_side_right}
        [END OF SIDE]
        """

    text_design_length_calculation = """ 1: Number of data
        [TABLE]
        [COLUMN INDICATION]
        Design Length
        Design Displacement
        Design MaxMoment
        Design Min Moment
        Design Anchor Foece
        Design Mobilisation percentage
        [END OF COLUMN INDICATION]

        [COLUMN DATA]
        15.000 -180.020 286.526 -118.981 -38.182 29.945
        [END OF COLUMN DATA]
        [END OF TABLE]"""

    text_design_length_info = """[TABLE]
        [COLUMN INDICATION]
        Design construction stage
        Design minimum length
        Design maximum length
        Design delta length
        Design verification type
        Use method A
        [END OF COLUMN INDICATION]
        [DATA]
        3   13.000   15.000    1.000  1     1 
        [END OF DATA]
        [END OF TABLE]"""

    text_design_sheetpile_length = f"""
        [DESIGN LENGTH INFO]
        {text_design_length_info}
        [END OF DESIGN LENGTH INFO]
        [DESIGN LENGTH CALCULATION]
        {text_design_length_calculation}
        [END OF DESIGN LENGTH CALCULATION]
        """

    text_points_on_sheetpile = """6: Number of nodes
        [TABLE]
        [COLUMN INDICATION]
        Depth
        [END OF COLUMN INDICATION]
        [DATA]
            0.42
            4.2
            42
            24
            2.4
            0.24
        [END OF DATA]
        [END OF TABLE]
        """

    text_section_points_on_sheetpile = f"""[POINTS ON SHEETPILE]
        {text_points_on_sheetpile}
        [END OF POINTS ON SHEETPILE]
        """

    text_section_construction_stage = f"""[CONSTRUCTION STAGE]
        {text_output_construction_stage}
        [END OF CONSTRUCTION STAGE]"""

    text_base_verification_structure_properties = f"""[POINTS ON SHEETPILE]
        {text_points_on_sheetpile}
        [END OF POINTS ON SHEETPILE]
        [POINTS ON SHEETPILE]
        {text_points_on_sheetpile}
        [END OF POINTS ON SHEETPILE]
        {text_section_construction_stage}
        {text_section_construction_stage}"""

    text_verify_anchor_force = f"""[ANCHOR NUMBER]
        1
        [END OF ANCHOR NUMBER]
        {text_section_points_on_sheetpile}
        {text_section_construction_stage}
        [UNKOWN GROUP]
        [END OF UNKONWN GROUP]"""

    text_verify_sheetpile_data = f"""3     FaseNr
        1     PartialFactorSet
        [VERIFY DEFORMATION]
        {text_base_verification_structure_properties}
        [END OF VERIFY DEFORMATION]
        [VERIFY MOMENT LOW ANGLE OF SUBGR REAC]
        {not_parsable_struct}
        [END OF VERIFY MOMENT LOW ANGLE OF SUBGR REAC]
        [VERIFY MOMENT HIGH ANGLE OF SUBGR REAC]
        {not_parsable_struct}
        [END OF VERIFY MOMENT HIGH ANGLE OF SUBGR REAC]
        [VERIFY MOMENT HIGH ANGLE OF SUBGR REAC]
        {not_parsable_struct}
        [END OF VERIFY MOMENT HIGH ANGLE OF SUBGR REAC]
        [VERIFY LOW MOD WITH ALT PASSIVE WATERLEVEL]
        {not_parsable_struct}
        [END OF VERIFY LOW MOD WITH ALT PASSIVE WATERLEVEL]
        [VERIFY HIGH MOD WITH ALT PASSIVE WATERLEVEL]
        {not_parsable_struct}
        [END OF VERIFY HIGH MOD WITH ALT PASSIVE WATERLEVEL]
        [VERIFY ANCHOR FORCE]
        {text_verify_anchor_force}
        [END OF VERIFY ANCHOR FORCE]
        [RESUME]
        {text_resume_structure}
        [END OF RESUME]
        [FACTORS FOR VERIFICATION]
        {not_parsable_struct}
        [END OF FACTORS FOR VERIFICATION]
        """

    text_output_data = f"""[CALCULATION TYPE]
        {text_calculation_type}
        [END OF CALCULATION TYPE]
        [RESUME]
        {text_resume_structure}
        [END OF RESUME]
        [POINTS ON SHEETPILE]
        {text_points_on_sheetpile}
        [END OF POINTS ON SHEETPILE]
        [CONSTRUCTION STAGE]
        {text_output_construction_stage}
        [END OF CONSTRUCTION STAGE]
        [DESIGN SHEETPILE LENGTH]
        {text_design_sheetpile_length}
        [END OF DESIGN SHEETPILE LENGTH]
        [VERIFY SHEETPILE DATA]
        {text_verify_sheetpile_data}
        [END OF VERIFY SHEETPILE DATA]
        [VERIFY SHEETPILE DATA]
        {text_verify_sheetpile_data}
        [END OF VERIFY SHEETPILE DATA]
        """

    # endregion

    # region validations
    def validate_verify_anchor_force(self, verify_anchor_force: VerifyAnchorForce):
        assert isinstance(verify_anchor_force, VerifyAnchorForce)
        assert verify_anchor_force.anchor_number == 1
        assert verify_anchor_force.points_on_sheetpile
        self.validate_points_on_sheetpile(verify_anchor_force.points_on_sheetpile[0])
        assert verify_anchor_force.construction_stage
        self.validate_output_construction_stage(verify_anchor_force.construction_stage[0])

    def validate_points_on_sheetpile(self, points_on_sheetpile: PointsOnSheetpile):
        assert isinstance(points_on_sheetpile, PointsOnSheetpile)
        assert len(points_on_sheetpile.pointsonsheetpile) == 6
        expected_values = [0.42, 4.2, 42, 24, 2.4, 0.24]
        for pos, point in enumerate(points_on_sheetpile.pointsonsheetpile):
            assert point["depth"] == expected_values[pos]

    def validate_resume_structure(self, resume_structure: Resume):
        assert resume_structure
        assert len(resume_structure.resume) == 1
        rs_table = resume_structure.resume[0]
        assert rs_table["moment"] == 11.64788
        assert rs_table["shear_force"] == -5.00187
        assert rs_table["displacement"] == 117.98290
        assert rs_table["percentage_mobilized_moment"] == 0
        assert rs_table["percentage_mobilized_resistance"] == 6.97007
        assert rs_table["stage"] == 1
        assert rs_table["verification_type"] == 15
        assert rs_table["partial_factor_type"] == 4
        assert rs_table["vertical_balance_result"] == 0
        assert rs_table["vertical_result_direction"] == 0
        assert rs_table["status"] == 0

    def validate_dsheetpiling_output_structure(
        self, output_structure: DSheetPilingOutputStructure
    ):
        assert output_structure
        assert output_structure.calculation_type == self.text_calculation_type
        self.validate_points_on_sheetpile(output_structure.points_on_sheetpile[-1])
        self.validate_resume_structure(output_structure.resume)
        self.validate_output_construction_stage(output_structure.construction_stage[-1])
        self.validate_design_sheetpile_length(output_structure.design_sheetpile_length)
        assert len(output_structure.verify_sheetpile_data) == 2

    def validate_design_length_calculation(
        self, design_length_calc: DesignLengthCalculation
    ):
        assert design_length_calc
        assert len(design_length_calc.designlengthcalculation) == 1
        dlc_table = design_length_calc.designlengthcalculation[0]
        assert dlc_table["design_length"] == 15
        assert dlc_table["design_displacement"] == -180.020
        assert dlc_table["design_maxmoment"] == 286.526
        assert dlc_table["design_min_moment"] == -118.981
        assert dlc_table["design_anchor_foece"] == -38.182
        assert dlc_table["design_mobilisation_percentage"] == 29.945

    def validate_design_length_info(self, design_length_info: DesignLengthInfo):
        assert design_length_info
        assert len(design_length_info.designlengthinfo) == 1
        dli_table = design_length_info.designlengthinfo[0]
        assert dli_table["design_construction_stage"] == 3
        assert dli_table["design_minimum_length"] == 13
        assert dli_table["design_maximum_length"] == 15
        assert dli_table["design_delta_length"] == 1
        assert dli_table["design_verification_type"] == 1
        assert dli_table["use_method_a"] == 1

    def validate_design_sheetpile_length(
        self, design_sheetpile_length: DesignSheetpileLength
    ):
        assert design_sheetpile_length
        self.validate_design_length_info(design_sheetpile_length.design_length_info)
        self.validate_design_length_calculation(
            design_sheetpile_length.design_length_calculation
        )

    def validate_pressures_structure(self, pressures: Pressures):
        assert pressures
        assert len(pressures.pressures) == 1
        p_table = pressures.pressures[0]
        assert p_table["horizontal_pressure"] == 0.09882
        assert p_table["pore_pressure"] == 0
        assert p_table["passive_pressure"] == 10.14826
        assert p_table["neutral_pressure"] == 2.20017
        assert p_table["status_on_branches"] == 1
        assert p_table["percentage_of_mobilisation"] == 0
        assert p_table["status_character"] == "A"

    def validate_side_structure(self, side_output: SideOutput):
        assert side_output
        assert side_output.calculation_method == self.not_parsable_struct
        assert side_output.water_level == self.not_parsable_struct
        assert side_output.surface == self.not_parsable_struct
        assert side_output.soil_profile_for_sheet_piling_model == self.not_parsable_struct
        self.validate_pressures_structure(side_output.pressures)
        assert side_output.force_from_layer == self.not_parsable_struct

    def validate_breuk_data_structure(self, breuk_data: BreukData):
        assert breuk_data is not None
        assert breuk_data.percentage_mobilized_resistance_left == 22.11
        assert breuk_data.percentage_mobilized_resistance_right == 8.36
        assert breuk_data.effective_left == 329.04
        assert breuk_data.effective_right == 329.13
        assert breuk_data.water_pressure_left == 961.38
        assert breuk_data.water_pressure_right == 961.38
        assert breuk_data.max_passive_effect_resistance_left == 1488.18
        assert breuk_data.max_passive_effect_resistance_right == 3939.32
        assert breuk_data.max_passive_moment_left == 0
        assert breuk_data.max_passive_moment_right == 0
        assert breuk_data.max_mobilized_passive_moment_left == 0
        assert breuk_data.max_mobilized_passive_moment_right == 0
        assert breuk_data.vertical_force_left == 93.87
        assert breuk_data.vertical_force_right == 88.75
        assert breuk_data.level_of_single_support == 0
        assert breuk_data.node_of_single_support == 1
        assert breuk_data.moment_present == 0
        assert breuk_data.active_side == 1

    def validate_anchor_data_structure(self, anchor_data: AnchorData):
        assert anchor_data
        assert len(anchor_data.anchordata) == 1
        ad_table = anchor_data.anchordata[0]
        assert ad_table["node_number"] == 7
        assert ad_table["position"] == -2
        assert ad_table["force"] == 17.97193
        assert ad_table["e_modulus"] == 190000000
        assert ad_table["status"] == 1
        assert ad_table["side"] == 2
        assert ad_table["anchortype"] == 0
        assert ad_table["anchorname"] == "AnchorName"

    def validate_moment_force_displacements_structure(
        self, mfd_data: MomentsForcesDisplacements
    ):
        assert mfd_data
        assert len(mfd_data.momentsforcesdisplacements) == 1
        mfd_table = mfd_data.momentsforcesdisplacements[0]
        assert mfd_table["moment"] == 0
        assert mfd_table["shear_force"] == 0
        assert mfd_table["displacements"] == -193.89808

    def validate_side_list_structure(self, side_list: List[SideOutput]):
        assert side_list
        assert len(side_list) == 2
        for side in side_list:
            self.validate_side_structure(side)

    def validate_output_construction_stage(
        self, output_construction_stage: OutputConstructionStage
    ):
        # 3. Validate final expectations.
        assert isinstance(output_construction_stage, OutputConstructionStage)
        self.validate_breuk_data_structure(output_construction_stage.breuk_data)
        self.validate_anchor_data_structure(output_construction_stage.anchor_data)
        self.validate_moment_force_displacements_structure(
            output_construction_stage.moments_forces_displacements
        )
        self.validate_side_list_structure(output_construction_stage.side)

    def validate_verify_sheetpile_data(self, verify_sheetpile_data: VerifySheetpileData):
        assert verify_sheetpile_data
        self.validate_resume_structure(verify_sheetpile_data.resume)
        self.validate_verify_anchor_force(verify_sheetpile_data.verify_anchor_force)
        self.validate_base_verification_structure_properties(
            verify_sheetpile_data.verify_deformation
        )

    def validate_points_on_sheetpile_list(self, pos_list: List[PointsOnSheetpile]):
        assert len(pos_list) == 2
        for pos in pos_list:
            self.validate_points_on_sheetpile(pos)

    def validate_output_construction_stage_list(
        self, ocs_list: List[OutputConstructionStage]
    ):
        assert len(ocs_list) == 2
        for ocs in ocs_list:
            self.validate_output_construction_stage(ocs)

    def validate_base_verification_structure_properties(
        self, bv_struct_props: BaseVerificationStructureProperties
    ):
        assert bv_struct_props
        self.validate_points_on_sheetpile_list(bv_struct_props.points_on_sheetpile)
        self.validate_output_construction_stage_list(bv_struct_props.construction_stage)

    # endregion

    text_to_structure_testdata = [
        pytest.param(
            text_base_verification_structure_properties,
            BaseVerificationStructureProperties,
            validate_base_verification_structure_properties,
            id="Base Verification Structure Properties.",
        ),
        pytest.param(
            text_verify_sheetpile_data,
            VerifySheetpileData,
            validate_verify_sheetpile_data,
            id="Verify Sheetpile Data",
        ),
        pytest.param(
            text_points_on_sheetpile,
            PointsOnSheetpile,
            validate_points_on_sheetpile,
            id="Points on Sheetpile",
        ),
        pytest.param(
            text_resume_structure, Resume, validate_resume_structure, id="Resume"
        ),
        pytest.param(
            text_output_data,
            DSheetPilingOutputStructure,
            validate_dsheetpiling_output_structure,
            id="Output Dump Structure",
        ),
        pytest.param(
            text_design_length_info,
            DesignLengthInfo,
            validate_design_length_info,
            id="Design Length Info",
        ),
        pytest.param(
            text_design_length_calculation,
            DesignLengthCalculation,
            validate_design_length_calculation,
            id="Design Length Calculation",
        ),
        pytest.param(
            text_design_sheetpile_length,
            DesignSheetpileLength,
            validate_design_sheetpile_length,
            id="Design Sheetpile Length",
        ),
        pytest.param(
            text_breuk_data,
            BreukData,
            validate_breuk_data_structure,
            id="Breuk Data",
        ),
        pytest.param(
            text_anchor_data,
            AnchorData,
            validate_anchor_data_structure,
            id="Anchor Data",
        ),
        pytest.param(
            text_moment_forces_displacements,
            MomentsForcesDisplacements,
            validate_moment_force_displacements_structure,
            id="Moment Force Displacements",
        ),
        pytest.param(
            text_output_construction_stage,
            OutputConstructionStage,
            validate_output_construction_stage,
            id="Output Construction Stage",
        ),
        pytest.param(
            text_pressures,
            Pressures,
            validate_pressures_structure,
            id="Pressures",
        ),
        pytest.param(
            text_side_left,
            SideOutput,
            validate_side_structure,
            id="Side Output (Leftside)",
        ),
        pytest.param(
            text_verify_anchor_force,
            VerifyAnchorForce,
            validate_verify_anchor_force,
            id="Verify Anchor Force",
        ),
    ]

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "text_to_parse, internal_type, validation_method",
        text_to_structure_testdata,
    )
    def test_given_construction_stage_inner_structure_when_parse_text_then_returns_structure(
        self,
        text_to_parse: str,
        internal_type: DSeriesStructure,
        validation_method: Callable[[DSeriesStructure], None],
    ):
        # 1. Run test
        parsed_structure = internal_type.parse_text(text_to_parse)
        # 2. Validate
        validation_method(self, parsed_structure)
