import logging
import os
from pathlib import Path
from typing import List, Type

import pytest
from teamcity import is_running_under_teamcity

from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dsheetpiling.calculation_options import (
    CalculationOptions,
    CalculationOptionsPerStage,
    DesignSheetpilingLengthCalculationOptions,
    KranzAnchorStrengthCalculationOptions,
    OverallStabilityCalculationOptions,
    ReliabilityAnalysisCalculationOptions,
    StandardCalculationOptions,
    VerifyCalculationOptions,
)
from geolib.models.dsheetpiling.constructions import (
    DiaphragmWall,
    DiaphragmWallProperties,
    Pile,
    PileProperties,
    Sheet,
    SheetPileProperties,
)
from geolib.models.dsheetpiling.dsheetpiling_model import (
    DiaphragmModelType,
    DSheetPilingModel,
    SheetModelType,
    SinglePileModelType,
    WoodenSheetPileModelType,
)
from geolib.models.dsheetpiling.internal import (
    DSheetPilingDumpStructure,
    DSheetPilingInputStructure,
    DSheetPilingOutputStructure,
    DSheetPilingStructure,
    SurchargePoint,
)
from geolib.models.dsheetpiling.loads import (
    HorizontalLineLoad,
    LoadTypeFavourableUnfavourable,
    LoadTypePermanentVariable,
    Moment,
    NormalForce,
    SurchargeLoad,
    UniformLoad,
    VerificationLoadSettingsMomentNormalForce,
    VerificationLoadSettingsLoads,
)
from geolib.models.dsheetpiling.profiles import SoilLayer, SoilProfile
from geolib.models.dsheetpiling.settings import (
    CalculationType,
    CurveSettings,
    DistributionType,
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    ModelType,
    ModulusReactionType,
    ModulusSubgradeReaction,
    PartialFactorCalculationType,
    PartialFactorSetEC7NADNL,
    PassiveSide,
    SheetPilingElementMaterialType,
    Side,
    VerifyType,
)
from geolib.models.dsheetpiling.supports import (
    Anchor,
    RigidSupport,
    SpringSupport,
    Strut,
    SupportType,
)
from geolib.models.dsheetpiling.surface import Surface
from geolib.models.dsheetpiling.water_level import WaterLevel
from geolib.soils import MohrCoulombParameters, Soil, SoilType
from tests.utils import TestUtils, only_teamcity


@pytest.fixture
def model() -> DSheetPilingModel:
    model = DSheetPilingModel()
    model.add_stage(
        name="Initial stage",
        passive_side=PassiveSide.DSHEETPILING_DETERMINED,
        method_left=LateralEarthPressureMethodStage.KA_KO_KP,
        method_right=LateralEarthPressureMethodStage.KA_KO_KP,
    )
    return model


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
        "filename",
        [pytest.param(Path("bm1-1.shi"), id="Input file")],
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
    @pytest.mark.parametrize(
        "filename",
        [pytest.param(Path("bm1-1.shi"), id="Input file")],
    )
    def test_writing_anchors_large_values(self, filename: Path):
        """Test for bug in which very large values overlapped eachother
        in the .shi output, resulting in an invalid file.
        """

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
        stage_id = ds.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.KA_KO_KP,
            method_right=LateralEarthPressureMethodStage.KA_KO_KP,
            pile_top_displacement=0.01,
        )
        anchor = Anchor(name="Test", level="-1", yield_force=1e10)
        ds.add_anchor_or_strut(anchor, stage_id)
        ds.serialize(output_test_file)

        # 4.2. Read the generated data and make sure we can read
        # the large values.
        assert output_test_file.is_file()
        output_datastructure = DSheetPilingModel().parse(output_test_file).input_data
        print(output_datastructure.anchors)
        anchorline = output_datastructure.anchors.split("\n")[2].strip()  # dataline
        values = list(filter(lambda x: (len(x) != 0), anchorline.split(" ")))
        assert len(values) == 10

    @pytest.mark.acceptance
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
        df.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert df.datastructure

    @pytest.mark.unittest
    def test_execute_console_without_filename_raises_exception(self):
        # 1. Set up test data.
        df = DSheetPilingModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.parametrize(
        "reverse_elements",
        [
            pytest.param(True, id="Reverse elements"),
            pytest.param(False, id="Don't reverse elements"),
        ],
    )
    @pytest.mark.integrationtest
    def test_add_sheet(self, reverse_elements: bool):
        # 0. Set up test data.
        model = DSheetPilingModel()

        # Define inputs
        # first define the top level of the sheet pile
        top_level = 1
        sheet1 = Sheet(name="First inputted pile")
        sheet1.sheet_pile_properties = SheetPileProperties(section_bottom_level=-2)
        sheet2 = Sheet(name="Second inputted pile")
        sheet2.sheet_pile_properties = SheetPileProperties(section_bottom_level=-7)
        sheets = [sheet1, sheet2]
        if reverse_elements:
            sheets.reverse()

        # Initial expectation tested
        assert sheet1
        assert sheet2
        assert top_level

        # Run test
        model.set_construction(top_level=top_level, elements=sheets)

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

    @pytest.mark.parametrize(
        "reverse_elements",
        [
            pytest.param(True, id="Reverse elements"),
            pytest.param(False, id="Don't reverse elements"),
        ],
    )
    @pytest.mark.integrationtest
    def test_add_pile(self, reverse_elements: bool):
        # 0. Set up test data.
        model = DSheetPilingModel()

        # Define inputs
        # first define the top level of the sheet pile
        top_level = 1
        pile1 = Pile(name="First inputted pile")
        pile1.pile_properties = PileProperties(section_bottom_level=-2)
        pile2 = Pile(name="Second inputted pile")
        pile2.pile_properties = PileProperties(section_bottom_level=-7)

        piles = [pile1, pile2]
        if reverse_elements:
            piles.reverse()

        # Initial expectation tested
        assert pile1
        assert pile2
        assert top_level

        # Run test
        model.set_construction(top_level=top_level, elements=piles)

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

    @pytest.mark.parametrize(
        "reverse_elements",
        [
            pytest.param(True, id="Reverse elements"),
            pytest.param(False, id="Don't reverse elements"),
        ],
    )
    @pytest.mark.integrationtest
    def test_add_diaphragm_wall(self, reverse_elements: bool):
        # 0. Set up test data.
        model = DSheetPilingModel()

        # Define inputs
        # first define the top level of the sheet pile
        top_level = 1
        wall1 = DiaphragmWall(name="First inputted pile")
        wall1.diaphragm_wall_properties = DiaphragmWallProperties(section_bottom_level=-2)
        wall2 = DiaphragmWall(name="Second inputted pile")
        wall2.diaphragm_wall_properties = DiaphragmWallProperties(section_bottom_level=-7)
        walls = [wall1, wall2]
        if reverse_elements:
            walls.reverse()

        # Initial expectation tested
        assert wall1
        assert wall2
        assert top_level

        # Run test
        model.set_construction(top_level=top_level, elements=walls)

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
            pytest.param(LateralEarthPressureMethodStage.KA_KO_KP),
            pytest.param(LateralEarthPressureMethodStage.C_PHI_DELTA),
        ],
    )
    @pytest.mark.parametrize(
        "stage_method_right",
        [
            pytest.param(LateralEarthPressureMethodStage.KA_KO_KP),
            pytest.param(LateralEarthPressureMethodStage.C_PHI_DELTA),
        ],
    )
    def test_set_model_updates_all_stages(
        self,
        model_method: LateralEarthPressureMethod,
        stage_method_left: LateralEarthPressureMethodStage,
        stage_method_right: LateralEarthPressureMethodStage,
    ):
        model = DSheetPilingModel()
        name_1st_stage = "Initial stage"
        name_2nd_stage = "Second stage"
        model.add_stage(
            name=name_1st_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=stage_method_left,
            method_right=stage_method_right,
        )
        model.add_stage(
            name=name_2nd_stage,
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=stage_method_left,
            method_right=stage_method_right,
        )
        model_type = SheetModelType(method=model_method)
        model.set_model(model_type)

        # Check if all stage methods are updated
        for stage in model.datastructure.input_data.construction_stages.stages:
            if (
                model_method == LateralEarthPressureMethod.MIXED
            ):  # Should not affect set methods.
                assert stage.method_left.name == stage_method_left.name
                assert stage.method_right.name == stage_method_right.name
            else:
                assert (
                    stage.method_left.name
                    == model.datastructure.input_data.model.method.name
                )
                assert (
                    stage.method_right.name
                    == model.datastructure.input_data.model.method.name
                )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "method_left",
        [
            pytest.param(LateralEarthPressureMethodStage.KA_KO_KP, id="Left, not right"),
            pytest.param(
                LateralEarthPressureMethodStage.C_PHI_DELTA, id="Not left, right"
            ),
        ],
    )
    @pytest.mark.parametrize(
        "method_right",
        [
            pytest.param(LateralEarthPressureMethodStage.KA_KO_KP, id="Left, not right"),
            pytest.param(
                LateralEarthPressureMethodStage.C_PHI_DELTA, id="Not left, right"
            ),
        ],
    )
    def test_add_stage_with_single_pile_model_stages_are_not_equal_raises_value_error(
        self,
        method_left: LateralEarthPressureMethodStage,
        method_right: LateralEarthPressureMethodStage,
    ):
        model = DSheetPilingModel()
        model.set_model(SinglePileModelType())

        # Assert test correctness.
        assert model.datastructure.input_data.model.model.value == ModelType.SINGLE_PILE

        if method_left != method_right:
            with pytest.raises(ValueError):
                model.add_stage(
                    name="Intial stage",
                    passive_side=PassiveSide.DSHEETPILING_DETERMINED,
                    method_left=method_left,
                    method_right=method_right,
                )
        else:
            model.add_stage(
                name="Intial stage",
                passive_side=PassiveSide.DSHEETPILING_DETERMINED,
                method_left=method_left,
                method_right=method_right,
            )

    @pytest.mark.integrationtest
    def test_add_soil(self):
        # 1. Set up test data
        ds = DSheetPilingModel()
        soil = Soil(name="Test Soil")
        soil.soil_weight_parameters.unsaturated_weight = 10
        soil.soil_weight_parameters.saturated_weight = 11
        soil.mohr_coulomb_parameters.cohesion = 10
        soil.mohr_coulomb_parameters.friction_angle = 17
        soil2 = Soil(name="Test Soil 2")
        soil2.soil_weight_parameters.unsaturated_weight = 11
        soil2.soil_weight_parameters.saturated_weight = 12
        soil2.mohr_coulomb_parameters.cohesion = 13
        soil2.mohr_coulomb_parameters.friction_angle = 14

        # 2. Verify initial expectations
        assert ds.datastructure.input_data.soil_collection.soil == []

        # 3. Run test.
        new_soil = ds.add_soil(soil)
        new_soil2 = ds.add_soil(soil2)

        # 4. Verify final expectations.
        assert new_soil == "Test Soil"
        assert new_soil2 == "Test Soil 2"
        assert ds.datastructure.input_data.soil_collection.soil[0].name == "Test Soil"
        assert ds.datastructure.input_data.soil_collection.soil[-1].name == "Test Soil 2"

    @pytest.mark.integrationtest
    def test_add_soil_with_soil_type(self):
        # 1. Set up test data
        ds = DSheetPilingModel()

        gravel = Soil(name="Gravel")
        gravel.soil_type_settlement_by_vibrations = SoilType.GRAVEL

        sandy_loam = Soil(name="Sandy loam")
        sandy_loam.soil_type_settlement_by_vibrations = SoilType.SANDY_LOAM

        # 3. Run test
        ds.add_soil(gravel)
        with pytest.raises(ValueError):
            ds.add_soil(sandy_loam)

        # 4. Verify final expectations.
        assert len(ds.datastructure.input_data.soil_collection.soil) == 1
        assert (
            ds.datastructure.input_data.soil_collection.soil[0].soilsoiltype
            == SoilType.GRAVEL
        )

    @pytest.mark.parametrize(
        "testload",
        [
            pytest.param(
                HorizontalLineLoad(
                    name="New load",
                    level=-1,
                    load=10,
                    verification_load_settings=VerificationLoadSettingsLoads(
                        duration_type=LoadTypePermanentVariable.VARIABLE,
                        load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
                    ),
                )
            ),
            pytest.param(
                Moment(
                    name="New load",
                    level=-1,
                    load=10,
                    verification_load_settings=VerificationLoadSettingsMomentNormalForce(
                        duration_type=LoadTypePermanentVariable.VARIABLE,
                        load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
                    ),
                )
            ),
        ],
    )
    @pytest.mark.integrationtest
    def test_add_loads_normal_calculation(self, model: DSheetPilingModel, testload):
        # call the test function
        model.add_load(load=testload, stage_id=0)

        # test expectations
        if isinstance(testload, Moment):
            comparison_load = model.datastructure.input_data.moments
            assert (
                model.datastructure.input_data.construction_stages.stages[0].moment_loads[
                    0
                ]
                == "New load"
            )
        elif isinstance(testload, HorizontalLineLoad):
            comparison_load = model.datastructure.input_data.horizontal_line_loads
            assert (
                model.datastructure.input_data.construction_stages.stages[
                    0
                ].horizontal_line_loads[0]
                == "New load"
            )
        assert 1 == len(comparison_load.loads)
        assert "New load" == comparison_load.loads[0].name
        assert -1 == comparison_load.loads[0].level
        assert 10 == comparison_load.loads[0].load

        assert (
            comparison_load.loads[0].duration_type == LoadTypePermanentVariable.VARIABLE
        )
        assert (
            comparison_load.loads[0].load_type
            == LoadTypeFavourableUnfavourable.UNFAVOURABLE
        )

    @pytest.mark.parametrize(
        "testload",
        [
            pytest.param(
                NormalForce(
                    name="New load",
                    force_at_sheet_pile_top=-1,
                    force_at_surface_level_left_side=-10,
                    force_at_surface_level_right_side=1,
                    force_at_sheet_pile_toe=10,
                    verification_load_settings=VerificationLoadSettingsMomentNormalForce(
                        duration_type=LoadTypePermanentVariable.VARIABLE,
                        load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
                    ),
                )
            ),
        ],
    )
    @pytest.mark.integrationtest
    def test_add_normal_force_normal_calculation(
        self, model: DSheetPilingModel, testload
    ):
        # call the test function
        model.add_load(load=testload, stage_id=0)

        # test expectations
        assert (
            model.datastructure.input_data.construction_stages.stages[0].normal_forces[0]
            == "New load"
        )

        assert 1 == len(model.datastructure.input_data.normal_forces.loads)
        assert "New load" == model.datastructure.input_data.normal_forces.loads[0].name
        assert (
            -1
            == model.datastructure.input_data.normal_forces.loads[
                0
            ].force_at_sheet_pile_top
        )
        assert (
            -10
            == model.datastructure.input_data.normal_forces.loads[
                0
            ].force_at_surface_level_left_side
        )
        assert (
            1
            == model.datastructure.input_data.normal_forces.loads[
                0
            ].force_at_surface_level_right_side
        )
        assert (
            10
            == model.datastructure.input_data.normal_forces.loads[
                0
            ].force_at_sheet_pile_toe
        )
        assert (
            model.datastructure.input_data.normal_forces.loads[0].duration_type
            == LoadTypePermanentVariable.VARIABLE
        )
        assert (
            model.datastructure.input_data.normal_forces.loads[0].load_type
            == LoadTypeFavourableUnfavourable.UNFAVOURABLE
        )

    @pytest.mark.integrationtest
    def test_add_horizontal_line_loads_error_raised(self, model: DSheetPilingModel):
        # set up test data
        load = HorizontalLineLoad(name="New load", level=-1, load=10)
        expected_message = "Stage 1 is not added to the internal datastructure"

        # test expectations
        with pytest.raises(ValueError, match=expected_message):
            model.add_load(load=load, stage_id=1)

    def test_add_support_with_invalid_support_raises_ValueError(
        self, model: DSheetPilingModel
    ):
        stage_id = model.current_stage

        with pytest.raises(
            ValueError,
            match=r"support should be SpringSupport or RigidSupport, received ",
        ):
            model.add_support(support="not a support object", stage_id=stage_id)

    def test_add_anchor_or_strut_with_invalid_support_raises_ValueError(
        self, model: DSheetPilingModel
    ):
        stage_id = model.current_stage

        with pytest.raises(
            ValueError, match=r"support should be Anchor or Strut, received "
        ):
            model.add_anchor_or_strut(support="not a support object", stage_id=stage_id)

    def test_intialized_model_can_be_serialized(self):
        """Internal datastructure should be serializable from a intialized model"""
        # 1. setup test
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        filename = "serialized_from_intialized_model.shi"
        output_test_file = output_test_folder / filename

        # 2. Verify initial expectations
        model = DSheetPilingModel()
        assert isinstance(model, DSheetPilingModel)

        # 3. Run test.
        model.serialize(output_test_file)

        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_surcharge_load(self, model: DSheetPilingModel):
        # set up test load
        testload = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
            verification_load_settings=VerificationLoadSettingsLoads(
                duration_type=LoadTypePermanentVariable.VARIABLE,
                load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
            ),
            standard_deviation=0.1,
            distribution_type=DistributionType.LOG_NORMAL,
        )

        # perform test function
        model.add_surcharge_load(load=testload, side=Side.LEFT, stage_id=0)

        # test results
        # model.input_data
        assert 1 == len(model.datastructure.input_data.surcharge_loads.loads)

        assert (
            "New SurchargeLoad"
            == model.datastructure.input_data.surcharge_loads.loads[0].name
        )

        assert model.datastructure.input_data.surcharge_loads.loads[0].points[
            0
        ] == SurchargePoint(surchargeloaddistance=0.0, surchargeloadvalue=5.0)
        assert model.datastructure.input_data.surcharge_loads.loads[0].points[
            1
        ] == SurchargePoint(surchargeloaddistance=5.0, surchargeloadvalue=10.0)
        assert model.datastructure.input_data.surcharge_loads.loads[0].points[
            2
        ] == SurchargePoint(surchargeloaddistance=10.0, surchargeloadvalue=0.0)

        assert (
            1
            == model.datastructure.input_data.surcharge_loads.loads[
                0
            ].surchargeloadpermanent
        )
        assert (
            2
            == model.datastructure.input_data.surcharge_loads.loads[
                0
            ].surchargeloadfavourable
        )
        assert (
            3
            == model.datastructure.input_data.surcharge_loads.loads[
                0
            ].surchargeloaddistribution
        )
        assert (
            0.1
            == model.datastructure.input_data.surcharge_loads.loads[
                0
            ].surchargeloadstandarddeviation
        )

    @pytest.mark.integrationtest
    def test_add_surcharge_load_error_of_points(self, model: DSheetPilingModel):
        # Error with negative values
        error_message = (
            "All x-coordinates must be greater than or equal to 0, found -10.0"
        )
        with pytest.raises(ValueError, match=error_message):
            SurchargeLoad(
                name="New SurchargeLoad",
                points=[Point(x=0, z=-5), Point(x=-5, z=-10), Point(x=-10, z=0)],
                verification_load_settings=VerificationLoadSettingsLoads(
                    duration_type=LoadTypePermanentVariable.VARIABLE,
                    load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
                ),
                standard_deviation=0.1,
                distribution_type=DistributionType.LOG_NORMAL,
            )

        # Error the points are not strictly increasing
        error_message = "x-coordinates must be strictly increasing"
        with pytest.raises(ValueError, match=error_message):
            SurchargeLoad(
                name="New SurchargeLoad",
                points=[Point(x=10, z=5), Point(x=0, z=5), Point(x=10, z=0)],
                verification_load_settings=VerificationLoadSettingsLoads(
                    duration_type=LoadTypePermanentVariable.VARIABLE,
                    load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
                ),
                standard_deviation=0.1,
                distribution_type=DistributionType.LOG_NORMAL,
            )

    @pytest.mark.integrationtest
    def test_duplicate_loads(self, model: DSheetPilingModel):
        testload = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=10)],
            verification_load_settings=VerificationLoadSettingsLoads(
                duration_type=LoadTypePermanentVariable.VARIABLE,
                load_type=LoadTypeFavourableUnfavourable.UNFAVOURABLE,
            ),
            standard_deviation=0.1,
            distribution_type=DistributionType.LOG_NORMAL,
        )
        model.add_surcharge_load(load=testload, side=Side.LEFT, stage_id=0)
        error_message = "New SurchargeLoad load name is duplicated. Please change the name of the load."
        with pytest.raises(ValueError, match=error_message):
            model.add_surcharge_load(load=testload, side=Side.LEFT, stage_id=0)
