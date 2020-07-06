import pytest
from geolib.models.dsheetpiling.internal import (
    SheetPileElement,
    SheetPiling,
    DSheetPilingInputStructure,
    CalculationOptions,
    StageOptions,
    UniformLoad,
    UniformLoads,
    SurchargePoint,
    SurchargeLoad,
    SurchargeLoads,
)
from geolib.geometry import Point
from geolib.models.dsheetpiling.settings import SheetPilingElementMaterialType
import warnings
from geolib.models.dsheetpiling.constructions import (
    Sheet,
    SheetPileProperties,
)
import geolib.models.dsheetpiling.settings as settings
from geolib.models.dsheetpiling.calculation_options import CalculationOptionsPerStage


class TestInternal:
    @pytest.mark.integrationtest
    def test_update_length_of_sheet_pile_raises_error(self):
        # create sheet elements
        sheet_pile_1 = SheetPileElement(
            name="My sheet pile 1", sheetpilingelementlevel=-2
        )
        sheet_pile_2 = SheetPileElement(
            name="My sheet pile 2", sheetpilingelementlevel=-1
        )
        # append them to list
        sheet_piling = SheetPiling()
        sheet_piling.sheetpiling = [sheet_pile_1, sheet_pile_2]
        sheet_piling.leveltopsheetpiling = 0
        # set expected message
        expected_mssg = "Value not strictly decreasing for element My sheet pile 2"
        # Run test
        with pytest.raises(ValueError, match=expected_mssg):
            sheet_piling.update_length_of_sheet_pile()

    @pytest.mark.integrationtest
    def test_update_length_of_sheet_pile(self):
        # create sheet elements
        sheet_pile_1 = SheetPileElement(
            name="My sheet pile 1", sheetpilingelementlevel=-1
        )
        sheet_pile_2 = SheetPileElement(
            name="My sheet pile 2", sheetpilingelementlevel=-2
        )
        # append them to list
        sheet_piling = SheetPiling()
        sheet_piling.sheetpiling = [sheet_pile_1, sheet_pile_2]
        sheet_piling.leveltopsheetpiling = 2
        # Run test
        sheet_piling.update_length_of_sheet_pile()
        assert sheet_piling.lengthsheetpiling == 4

    @pytest.mark.integrationtest
    def test_update_level_top_sheet_pile_raised_error1(self):
        # Create sheet pile
        sheet_piling = SheetPiling()
        # value is set to simulate value not set by user
        test_top_level = None
        # set expected message
        expected_mssg = "Top pile level should be defined."
        # Run test
        with pytest.raises(Exception, match=expected_mssg):
            sheet_piling.update_level_top_sheet_pile(top_level=test_top_level)

    @pytest.mark.integrationtest
    def test_update_level_top_sheet_pile_raised_error2(self):
        """ Value is arleady set """
        # Create sheet pile
        sheet_piling = SheetPiling()
        # value is set to simulate value not set by user
        test_top_level = Point(x=0, y=1)
        sheet_piling.update_level_top_sheet_pile(top_level=test_top_level)
        # initial expectation tested
        assert sheet_piling.leveltopsheetpiling == 1
        # set expected message
        expected_mssg = "Top pile level was arleady determined."
        # Run test
        with pytest.raises(Exception, match=expected_mssg):
            sheet_piling.update_level_top_sheet_pile(top_level=test_top_level)

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
    def test_add_element_in_sheet_piling(self):
        # create sheet pile element and point
        sheet1 = Sheet(name="First inputted pile")
        sheet1.sheet_pile_properties = SheetPileProperties(section_bottom_level=-2)
        location_top = Point(x=0, y=0)
        # initial expectations checked
        assert location_top
        assert sheet1
        # run test
        model = DSheetPilingInputStructure()
        model.add_element_in_sheet_piling(sheet=sheet1, location_top=location_top)
        assert model.sheet_piling.lengthsheetpiling == 2
        assert model.sheet_piling.leveltopsheetpiling == 0

    @pytest.mark.integrationtest
    def test_add_element_in_sheet_piling_raised_error(self):
        location_top = Point(x=0, y=0)
        # initial expectations checked
        assert location_top
        # run test
        model = DSheetPilingInputStructure()
        expected_mssg = "Invalid argument, expected sheet, got <class 'NoneType'>"
        with pytest.raises(ValueError, match=expected_mssg):
            model.add_element_in_sheet_piling(sheet=None, location_top=location_top)

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_cur(self):
        # set inputs
        model = DSheetPilingInputStructure()

        calc_options_per_stage = CalculationOptionsPerStage(
            anchor_factor=1.5, partial_factor_set=settings.DesignPartialFactorSet.CLASSIII
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
            == settings.DesignPartialFactorSet.CLASSIII
        )
        assert model.calculation_options_per_stage.stageoptions[0].stageverify == 0
        assert (
            model.calculation_options_per_stage.stageoptions[0].stageanchorfactor == 1.5
        )

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_ec7_nl(self):
        # set inputs
        model = DSheetPilingInputStructure()
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
            model.calculation_options_per_stage.stageoptions[0].stageverifyec7nadnl == 0
        )
        assert (
            model.calculation_options_per_stage.stageoptions[0].stageanchorfactorec7nadnl
            == 1.5
        )

    @pytest.mark.integrationtest
    def test_add_calculation_options_per_stage_ec7_b(self):
        # set inputs
        model = DSheetPilingInputStructure()
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
        assert model.calculation_options_per_stage.stageoptions[0].stageverifyec7nadb == 0


class TestInternalParseText:
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
