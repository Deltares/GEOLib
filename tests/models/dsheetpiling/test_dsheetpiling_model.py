import logging
import os
from pathlib import Path
from typing import List, Type

import pytest
from teamcity import is_running_under_teamcity

from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dsheetpiling.calculation_options import (
    StandardCalculationOptions,
    CalculationOptions,
    DesignSheetpilingLengthCalculationOptions,
    VerifyCalculationOptions,
    KranzAnchorStrengthCalculationOptions,
    OverallStabilityCalculationOptions,
    ReliabilityAnalysisCalculationOptions,
    CalculationOptionsPerStage,
)
from geolib.models.dsheetpiling.dsheetpiling_model import (
    DSheetPilingModel,
    SheetModelType,
    WoodenSheetPileModelType,
    SinglePileModelType,
    DiaphragmModelType,
)
from geolib.models.dsheetpiling.internal import (
    DSheetPilingInputStructure,
    DSheetPilingOutputStructure,
    DSheetPilingStructure,
    DSheetPilingDumpStructure,
)
from geolib.models.dsheetpiling.constructions import (
    DiaphragmWall,
    Pile,
    Sheet,
    SheetPileProperties,
    PileProperties,
    DiaphragmWallProperties,
)
from geolib.models.dsheetpiling.water_level import WaterLevel
from geolib.models.dsheetpiling.supports import Anchor, Strut
from geolib.models.dsheetpiling.settings import (
    LateralEarthPressureMethod,
    ModelType,
    CalculationType,
    VerifyType,
    PartialFactorCalculationType,
    PartialFactorSetEC7NADNL,
    Side,
)
from tests.utils import TestUtils, only_teamcity
from geolib.soils import Soil


class TestDsheetPilingModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSheetPilingModel_instance(self):
        dsheetpiling_model = DSheetPilingModel()
        assert dsheetpiling_model is not None
        assert isinstance(dsheetpiling_model, BaseModel), (
            "" + "DSheetPilingModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename,structure",
        [
            pytest.param(Path("bm1-1.shi"), DSheetPilingStructure, id="Input file"),
            pytest.param(Path("bm1-1.shd"), DSheetPilingDumpStructure, id="Output file"),
        ],
    )
    def test_given_filepath_when_parse_then_does_not_raise(
        self, filename: Path, structure: Type
    ):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / filename
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.is_file()

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert isinstance(ds.datastructure, structure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1.shi"), id="Input file")],
    )
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / filename
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / filename
        ds = DSheetPilingModel()

        # 2. Verify initial expectations
        assert test_file.is_file()
        if output_test_file.is_file():
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure.input_data, "No data has been generated."
        assert isinstance(ds.datastructure.input_data, DSheetPilingInputStructure)
        input_datastructure = dict(ds.datastructure.input_data)

        # 4.2. Read the generated data.
        assert output_test_file.is_file()
        output_datastructure = dict(
            DSheetPilingModel().parse(output_test_file).input_data
        )
        assert not (
            input_datastructure is output_datastructure
        ), "Both references are the same."

        # 4.3. Compare values
        output_keys = output_datastructure.keys()
        errors = []
        for ds_key, ds_value in input_datastructure.items():
            if not (ds_key in output_keys):
                errors.append(f"Key {ds_key} not serialized!")
                continue
            if not (ds_value == output_datastructure[ds_key]):
                logging.warning(f"UNEQUAL: {ds_value} != {output_datastructure[ds_key]}")
                errors.append(f"Values for key {ds_key} differ from parsed to serialized")
        if errors:
            pytest.fail(f"Failed with the following {errors}")

    @pytest.mark.systemtest
    @only_teamcity
    def test_execute_console_successfully(self):
        # 1. Set up test data.
        df = DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling"))
        test_file = test_folder / "bm1-1.shi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / "test.shi"

        df.parse(test_file)
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert output_test_file.is_file()

        # 3. Run test.
        df.filename = output_test_file
        status = df.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0

    @pytest.mark.unittest
    def test_execute_console_without_filename_raises_exception(self):
        # 1. Set up test data.
        df = DSheetPilingModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "modeltype,first_sheet,second_sheet",
        [
            pytest.param(
                SheetModelType(),
                SheetModelType(
                    name="First inputted pile",
                    sheet_pile_properties=SheetPileProperties(section_bottom_level=-2),
                ),
                SheetModelType(
                    name="Second inputted pile",
                    sheet_pile_properties=SheetPileProperties(section_bottom_level=-7),
                ),
                id="Sheetpile",
            ),
            pytest.param(
                DiaphragmModelType(),
                DiaphragmModelType(
                    name="First inputted pile",
                    sheet_pile_properties=DiaphragmWallProperties(
                        section_bottom_level=-2
                    ),
                ),
                DiaphragmModelType(
                    name="Second inputted pile",
                    sheet_pile_properties=DiaphragmWallProperties(
                        section_bottom_level=-7
                    ),
                ),
                id="Diaphragm wall",
            ),
        ],
    )
    @pytest.mark.xfail(reason="Can't work yet.")
    def test_run_sheet_model_from_scratch(self, modeltype, first_sheet, second_sheet):
        """
        Model is a 3 staged model with an excavation to the left.
        """
        # 0. Set up test data.
        model = DSheetPilingModel()
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / "acceptance_from_scratch.shi"

        # 1. Build model.
        model.set_model(modeltype)

        # Add construction.
        location_top = Point(x=0, z=1)
        model.add_sheet(sheet=first_sheet, location_top=location_top)
        model.add_sheet(sheet=second_sheet)

        # Add soil
        soil = Soil(name="Test Soil", soil_type_nl=3, friction_angle=0.01)
        new_soil = model.add_soil(soil)

        # Add general calculation options for model
        calc_options = VerifyCalculationOptions(
            input_calculation_type=CalculationType.VERIFY_SHEETPILING,
            verify_type=VerifyType.EC7NL,
            ec7_nl_method=PartialFactorCalculationType.METHODB,
        )
        model.set_calculation_options(calculation_options=calc_options)
        calc_options_per_stage = CalculationOptionsPerStage(
            anchor_factor=1.5, partial_factor_set=settings.PartialFactorSetEC7NADNL.RC2
        )

        # Add 1st stage.
        profile = Profile()
        left_initial_surface: List[Point] = [Point(x=0, z=0)]
        right_initial_surface: List[Point] = [Point(x=0, z=0)]
        intial_water_level = WaterLevel(name="Intitial water level", level=-2)

        model.add_stage(name="Intial situation")
        model.add_profile(left=profile, right=profile)
        model.add_surface(left=left_initial_surface, right=right_initial_surface)
        model.add_head_line(left=intial_water_level, right=intial_water_level)
        model.add_calculation_options_per_stage(
            calculation_options_per_stage=calc_options_per_stage
        )

        # Add 2nd stage.
        half_excavated_surface: List[Point] = [Point(x=0, z=-5)]
        halfway_water_level = WaterLevel(name="Halfway water level", level=-7)
        anchor = Anchor(name="Grout anchor", level=-2, side=Side.RIGHT)

        model.add_stage(name="Halfway through excavation")
        model.add_profile(left=profile, right=profile)
        model.add_surface(left=half_excavated_surface, right=right_initial_surface)
        model.add_head_line(left=halfway_water_level, right=intial_water_level)
        model.add_support(support=anchor)
        model.add_calculation_options_per_stage(
            calculation_options_per_stage=calc_options_per_stage
        )

        # Add 3th stage.
        right_final_surface: List[Point] = [Point(x=0, y=-10)]
        final_water_level = WaterLevel(
            name="After dry pumping", level=-12
        )  # Model a dry cofferdam by setting water level lower than the surface.
        floor = Strut(name="Concrete floor", level=-10, side=Side.LEFT)

        model.add_stage(name="Final situation")
        model.add_surface(left=left_initial_surface, right=right_final_surface)
        model.add_head_line(left=final_water_level, right=intial_water_level)
        model.add_support(support=floor)
        model.add_calculation_options_per_stage(
            calculation_options_per_stage=calc_options_per_stage
        )

        # TODO add uniform loads
        # TODO add non-uniform loads

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        status = model.execute()

        # 4. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0

    @pytest.mark.integrationtest
    def test_add_sheet(self):
        # 0. Set up test data.
        model = DSheetPilingModel()
        # output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        # output_test_file = output_test_folder / "acceptance_from_scratch.shi"

        # Define inputs
        # first define the top level of the sheet pile
        location_top = Point(x=0, y=1)
        sheet1 = Sheet(name="First inputted pile")
        sheet1.sheet_pile_properties = SheetPileProperties(section_bottom_level=-2)
        sheet2 = Sheet(name="Second inputted pile")
        sheet2.sheet_pile_properties = SheetPileProperties(section_bottom_level=-7)
        # Initial expectation tested
        assert sheet1
        assert sheet2
        assert location_top
        # Run test
        model.add_sheet(sheet=sheet1, location_top=location_top)
        model.add_sheet(sheet=sheet2)
        # test final
        assert model.datastructure.input_data.sheet_piling.lengthsheetpiling == 8
        assert model.datastructure.input_data.sheet_piling.leveltopsheetpiling == 1
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[0].name
            == "First inputted pile"
        )
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[1].name
            == "Second inputted pile"
        )

    @pytest.mark.integrationtest
    def test_add_pile(self):
        # 0. Set up test data.
        model = DSheetPilingModel()
        # output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        # output_test_file = output_test_folder / "acceptance_from_scratch.shi"

        # Define inputs
        # first define the top level of the sheet pile
        location_top = Point(x=0, y=1)
        pile1 = Pile(name="First inputted pile")
        pile1.pile_properties = PileProperties(section_bottom_level=-2)
        pile2 = Pile(name="Second inputted pile")
        pile2.pile_properties = PileProperties(section_bottom_level=-7)
        # Initial expectation tested
        assert pile1
        assert pile2
        assert location_top
        # Run test
        model.add_pile(pile=pile1, location_top=location_top)
        model.add_pile(pile=pile2)
        # test final
        assert model.datastructure.input_data.sheet_piling.lengthsheetpiling == 8
        assert model.datastructure.input_data.sheet_piling.leveltopsheetpiling == 1
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[0].name
            == "First inputted pile"
        )
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[1].name
            == "Second inputted pile"
        )

    @pytest.mark.integrationtest
    def test_add_diaphragm_wall(self):
        # 0. Set up test data.
        model = DSheetPilingModel()
        # output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        # output_test_file = output_test_folder / "acceptance_from_scratch.shi"

        # Define inputs
        # first define the top level of the sheet pile
        location_top = Point(x=0, y=1)
        wall1 = DiaphragmWall(name="First inputted pile")
        wall1.diaphragm_wall_properties = DiaphragmWallProperties(section_bottom_level=-2)
        wall2 = DiaphragmWall(name="Second inputted pile")
        wall2.diaphragm_wall_properties = DiaphragmWallProperties(section_bottom_level=-7)
        # Initial expectation tested
        assert wall1
        assert wall2
        assert location_top
        # Run test
        model.add_pile(pile=wall1, location_top=location_top)
        model.add_pile(pile=wall2)
        # test final
        assert model.datastructure.input_data.sheet_piling.lengthsheetpiling == 8
        assert model.datastructure.input_data.sheet_piling.leveltopsheetpiling == 1
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[0].name
            == "First inputted pile"
        )
        assert (
            model.datastructure.input_data.sheet_piling.sheetpiling[1].name
            == "Second inputted pile"
        )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "modeltype,expected_model_value",
        [
            pytest.param(SheetModelType, 0, id="Sheet model"),
            pytest.param(WoodenSheetPileModelType, 0, id="Wooden sheet model"),
            pytest.param(SinglePileModelType, 1, id="Single pile model"),
            pytest.param(DiaphragmModelType, 2, id="Diaphragm model"),
        ],
    )
    def test_set_model(self, modeltype, expected_model_value: int):
        model = DSheetPilingModel()
        model.set_model(modeltype())
        assert model.datastructure.input_data.model.model.value == expected_model_value

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "model_method",
        [
            pytest.param(LateralEarthPressureMethod.MIXED),
            pytest.param(LateralEarthPressureMethod.KA_KO_KP),
            pytest.param(LateralEarthPressureMethod.C_PHI_DELTA),
        ],
    )
    @pytest.mark.parametrize(
        "stage_method_left",
        [
            pytest.param(LateralEarthPressureMethod.KA_KO_KP),
            pytest.param(LateralEarthPressureMethod.C_PHI_DELTA),
        ],
    )
    @pytest.mark.parametrize(
        "stage_method_right",
        [
            pytest.param(LateralEarthPressureMethod.KA_KO_KP),
            pytest.param(LateralEarthPressureMethod.C_PHI_DELTA),
        ],
    )
    def test_set_model_updates_all_stages(
        self,
        model_method: LateralEarthPressureMethod,
        stage_method_left: LateralEarthPressureMethod,
        stage_method_right: LateralEarthPressureMethod,
    ):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        name_2nd_stage = "Second stage"
        model.add_stage(name=name_1st_stage)
        model.add_stage(name=name_2nd_stage)

        model_type = SheetModelType(method=model_method)
        model.set_model(model_type)

        # Check if all stage methods are updated
        for stage in model.datastructure.input_data.construction_stages.stages:
            if (
                model == LateralEarthPressureMethod.MIXED
            ):  # Should not affect set methods.
                assert stage.method_left == stage_method_left
                assert stage.method_right == stage_method_right
            else:
                assert stage.method_left == model.datastructure.input_data.model.method
                assert stage.method_right == model.datastructure.input_data.model.method

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "method_left",
        [
            pytest.param(LateralEarthPressureMethod.KA_KO_KP, id="Left, not right"),
            pytest.param(LateralEarthPressureMethod.C_PHI_DELTA, id="Not left, right"),
            pytest.param(LateralEarthPressureMethod.MIXED, id="Both"),
        ],
    )
    @pytest.mark.parametrize(
        "method_right",
        [
            pytest.param(LateralEarthPressureMethod.KA_KO_KP, id="Left, not right"),
            pytest.param(LateralEarthPressureMethod.C_PHI_DELTA, id="Not left, right"),
            pytest.param(LateralEarthPressureMethod.MIXED, id="Both"),
        ],
    )
    def test_add_stage_with_single_pile_model_stages_are_not_equal_raises_value_error(
        self,
        method_left: LateralEarthPressureMethod,
        method_right: LateralEarthPressureMethod,
    ):
        model = DSheetPilingModel()
        model.set_model(SinglePileModelType())

        # Assert test correctness.
        assert model.datastructure.input_data.model.model.value == ModelType.SINGLE_PILE

        if (
            method_left != method_right
            or method_left == LateralEarthPressureMethod.MIXED
            or method_right == LateralEarthPressureMethod.MIXED
        ):
            with pytest.raises(ValueError):
                model.add_stage(
                    name="Intial stage",
                    method_left=method_left,
                    method_right=method_right,
                )
        else:
            model.add_stage(
                name="Intial stage", method_left=method_left, method_right=method_right
            )

    @pytest.mark.integrationtest
    def test_add_soil(self):
        # 1. Set up test data
        ds = DSheetPilingModel()
        soil = Soil(name="Test Soil", soil_type_nl=3, friction_angle=0.01)
        soil2 = Soil(name="Test Soil 2", soil_type_nl=3, friction_angle=0.01)
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir("dsheetpiling/serialize/")
        )
        output_test_file = output_test_folder / "soils.shi"

        # 2. Verify initial expectations
        assert ds.datastructure.input_data.soil_collection.soil == []

        # 3. Run test.
        new_soil = ds.add_soil(soil)
        new_soil2 = ds.add_soil(soil2)

        # 4. Verify final expectations.
        assert new_soil == "Test Soil"
        assert ds.datastructure.input_data.soil_collection.soil[0].name == "Test Soil"
        assert ds.datastructure.input_data.soil_collection.soil[-1].name == "Test Soil 2"

        # 5. Serialize result to check manually
        ds.serialize(output_test_file)
