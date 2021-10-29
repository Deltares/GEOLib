import json
import random
from pathlib import Path

import pytest
from pydantic.color import Color
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
    FullPlasticCalculationProperties,
    Pile,
    PileProperties,
    Sheet,
    SheetPileModelPlasticCalculationProperties,
    SheetPileProperties,
    WoodenSheetPileProperties,
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
    VerificationLoadSettings,
    VerificationLoadSettingsHorizontalLineLoad,
)
from geolib.models.dsheetpiling.profiles import SoilLayer, SoilProfile
from geolib.models.dsheetpiling.settings import (
    CalculationType,
    CurveSettings,
    DesignType,
    DistributionType,
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    ModelType,
    ModulusReactionType,
    ModulusSubgradeReaction,
    PartialFactorCalculationType,
    PartialFactorSetCUR,
    PartialFactorSetEC7NADNL,
    PassiveSide,
    SheetPilingElementMaterialType,
    Side,
    SinglePileLoadOptions,
    SoilTypeModulusSubgradeReaction,
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
from geolib.soils import (
    EarthPressureCoefficientsType,
    GrainType,
    HorizontalBehaviourType,
    LambdaType,
    Soil,
    SoilType,
)
from tests.utils import TestUtils, only_teamcity


class TestDsheetPilingAcceptance:
    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "calc_options",
        [
            (
                VerifyCalculationOptions(
                    input_calculation_type=CalculationType.VERIFY_SHEETPILING,
                    verify_type=VerifyType.EC7NL,
                    ec7_nl_method=PartialFactorCalculationType.METHODB,
                )
            ),
            (StandardCalculationOptions()),
            (
                OverallStabilityCalculationOptions(
                    cur_stability_stage=0,
                    overall_stability_type=DesignType.CUR,
                    stability_cur_partial_factor_set=PartialFactorSetCUR.CLASSII,
                )
            ),
            (KranzAnchorStrengthCalculationOptions(cur_anchor_force_stage=0)),
            (
                DesignSheetpilingLengthCalculationOptions(
                    design_stage=0,
                    design_pile_length_from=20,
                    design_pile_length_to=12,
                    design_pile_length_decrement=0.1,
                    design_type=DesignType.EC7NL,
                    design_partial_factor_set_ec7_nad_nl=PartialFactorSetEC7NADNL.RC1,
                    design_ec7_nl_method=PartialFactorCalculationType.METHODA,
                )
            ),
        ],
    )
    def test_run_sheet_model_acceptance_different_calculation_types(
        self, request, calc_options
    ):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
        )
        model.set_model(modeltype)

        # Add construction.
        sheet_pile_properties_1 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_1 = Sheet(
            name="AZ 13", sheet_pile_properties=sheet_pile_properties_1
        )
        sheet_pile_properties_2 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_2 = Sheet(
            name="AZ 14", sheet_pile_properties=sheet_pile_properties_2
        )
        level_top = 0
        model.set_construction(
            top_level=level_top, elements=[sheet_element_1, sheet_element_2]
        )

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay", color=Color("green"))
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.mohr_coulomb_parameters.friction_angle_interface = 11
        soil_clay.shell_factor = 1
        soil_clay.soil_state.ocr_layer = 1
        soil_clay.soil_classification_parameters.grain_type = GrainType.FINE
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.soil_classification_parameters.relative_density = 72
        soil_clay.storage_parameters.horizontal_permeability = 8e-11
        soil_clay.soil_type_settlement_by_vibrations = SoilType.CLAY
        # set peat material
        soil_peat = Soil(name="Peat", color=Color("red"))
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.mohr_coulomb_parameters.friction_angle_interface = 0
        soil_peat.shell_factor = 1
        soil_peat.soil_state.ocr_layer = 1
        soil_peat.soil_classification_parameters.grain_type = GrainType.FINE
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_peat.subgrade_reaction_parameters.k_1_top = 800
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 800
        soil_peat.soil_classification_parameters.relative_density = 72
        soil_peat.storage_parameters.horizontal_permeability = 8e-10
        soil_peat.soil_type_settlement_by_vibrations = SoilType.PEAT
        # set sand material
        soil_sand = Soil(name="Sand", color=Color("yellow"))
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.mohr_coulomb_parameters.friction_angle_interface = 27
        soil_sand.shell_factor = 1
        soil_sand.soil_state.ocr_layer = 1
        soil_sand.soil_classification_parameters.grain_type = GrainType.FINE
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.KOTTER
        soil_sand.subgrade_reaction_parameters.k_1_top = 10000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 10000
        soil_sand.soil_classification_parameters.relative_density = 72
        soil_sand.storage_parameters.horizontal_permeability = 8e-9
        soil_sand.soil_type_settlement_by_vibrations = SoilType.SAND
        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)

        # Add stage.
        stage_id = model.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # Add soil profile, surfaces, and water level to stage.
        profile = SoilProfile(
            name="New Profile",
            layers=[
                SoilLayer(top_of_layer=0, soil=soil_clay.name),
                SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                SoilLayer(top_of_layer=-13, soil=soil_sand.name),
            ],
        )
        model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

        ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
        ground_level_minus_7_meter_surface = Surface(
            name="GL-7", points=[Point(x=0, z=-7)],
        )

        model.add_surface(
            surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
        )
        model.add_surface(
            surface=ground_level_minus_7_meter_surface, side=Side.LEFT, stage_id=stage_id
        )

        initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
        model.add_head_line(
            water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
        )
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # Add general calculation options for model
        model.set_calculation_options(calculation_options=calc_options)
        if isinstance(calc_options, VerifyCalculationOptions):
            calc_options_per_stage = CalculationOptionsPerStage(
                anchor_factor=1.5, partial_factor_set=PartialFactorSetEC7NADNL.RC2
            )
            # stage_id refers to the pythonic input and the conversion in stage number for D-SheetPiling is handled internally
            model.add_calculation_options_per_stage(
                calculation_options_per_stage=calc_options_per_stage, stage_id=stage_id,
            )

        # add anchor
        anchor = Anchor(
            name="Grout anchor",
            level=-2,
            side=Side.RIGHT,
            e_modulus=100000,
            cross_section=10,
            wall_height_kranz=1,
            length=2,
            angle=3,
            yield_force=100000000,
        )
        model.add_anchor_or_strut(support=anchor, stage_id=stage_id)

        # add strut
        floor = Strut(
            name="Concrete floor",
            level=-10,
            side=Side.LEFT,
            e_modulus=100000,
            angle=1,
            buckling_force=100,
            pre_compression=10,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_anchor_or_strut(support=floor, stage_id=stage_id)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=0)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(spring_support, stage_id)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(rigid_support, stage_id)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        model.add_load(load=uniform_load, stage_id=stage_id)

        # add surcharge load
        surcharge_load = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
        )
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=0)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        model.execute()

        # 4. Verify succesfull parsing of output datastructure
        assert model.datastructure
        assert model.datastructure.is_valid
        with open("data" + output_test_file.name.split(".")[0] + ".json", "w") as outfile:
            json.dump(model.datastructure.dict(), outfile, ensure_ascii=False, indent=4)

    @pytest.mark.acceptance
    @only_teamcity
    def test_run_sheet_model_acceptance_multiple_stages(self, request):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
        )
        model.set_model(modeltype)

        # Add construction.
        sheet_pile_properties_1 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_1 = Sheet(
            name="AZ 13", sheet_pile_properties=sheet_pile_properties_1
        )
        sheet_pile_properties_2 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_2 = Sheet(
            name="AZ 14", sheet_pile_properties=sheet_pile_properties_2
        )
        level_top = 0
        model.set_construction(
            top_level=level_top, elements=[sheet_element_1, sheet_element_2]
        )

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay")
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.mohr_coulomb_parameters.friction_angle_interface = 11
        soil_clay.shell_factor = 1
        soil_clay.soil_state.ocr_layer = 1
        soil_clay.soil_classification_parameters.grain_type = GrainType.FINE
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.soil_classification_parameters.relative_density = 72
        soil_clay.storage_parameters.horizontal_permeability = 8e-11
        soil_clay.soil_type_settlement_by_vibrations = SoilType.CLAY
        # set peat material
        soil_peat = Soil(name="Peat")
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.mohr_coulomb_parameters.friction_angle_interface = 0
        soil_peat.shell_factor = 1
        soil_peat.soil_state.ocr_layer = 1
        soil_peat.soil_classification_parameters.grain_type = GrainType.FINE
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_peat.subgrade_reaction_parameters.k_1_top = 800
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 800
        soil_peat.soil_classification_parameters.relative_density = 72
        soil_peat.storage_parameters.horizontal_permeability = 8e-10
        soil_peat.soil_type_settlement_by_vibrations = SoilType.PEAT
        # set sand material
        soil_sand = Soil(name="Sand")
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.mohr_coulomb_parameters.friction_angle_interface = 27
        soil_sand.shell_factor = 1
        soil_sand.soil_state.ocr_layer = 1
        soil_sand.soil_classification_parameters.grain_type = GrainType.FINE
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.KOTTER
        soil_sand.subgrade_reaction_parameters.k_1_top = 10000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 10000
        soil_sand.soil_classification_parameters.relative_density = 72
        soil_sand.storage_parameters.horizontal_permeability = 8e-9
        soil_sand.soil_type_settlement_by_vibrations = SoilType.SAND
        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)
        # set inputs for modulus of subgrade reaction
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # add multiple stages
        total_number_of_stages = 4
        for stage in range(total_number_of_stages):
            # Add stage.
            stage_id = model.add_stage(
                name="Stage" + str(stage),
                passive_side=PassiveSide(random.randint(0, 2)),
                method_left=LateralEarthPressureMethodStage(random.randint(1, 2)),
                method_right=LateralEarthPressureMethodStage(random.randint(1, 2)),
                pile_top_displacement=0.01,
            )

            # Add soil profile, surfaces, and water level to stage.
            # variation for stage
            variation = stage
            profile = SoilProfile(
                name="New Profile",
                layers=[
                    SoilLayer(top_of_layer=0, soil=soil_clay.name),
                    SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                    SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                    SoilLayer(top_of_layer=-13, soil=soil_sand.name),
                ],
            )
            model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

            ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
            ground_level_minus_7_meter_surface = Surface(
                name="GL-7" + "-stage-" + str(stage),
                points=[Point(x=0, z=-7 + variation)],
            )

            model.add_surface(
                surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
            )
            model.add_surface(
                surface=ground_level_minus_7_meter_surface,
                side=Side.LEFT,
                stage_id=stage_id,
            )

            initial_water_level = WaterLevel(
                name="WL=GL-2-stage" + str(stage), level=-2 + variation
            )
            model.add_head_line(
                water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
            )

        # Add general calculation options for model
        calc_options = StandardCalculationOptions()
        model.set_calculation_options(calculation_options=calc_options)

        # Add anchors, supports and loads in different stages
        # add anchor
        anchor = Anchor(
            name="Grout anchor",
            level=-2,
            side=Side.RIGHT,
            e_modulus=100000,
            cross_section=10,
            wall_height_kranz=1,
            length=2,
            angle=3,
            yield_force=100,
        )
        model.add_anchor_or_strut(support=anchor, stage_id=stage_id)

        # add strut
        floor = Strut(
            name="Concrete floor",
            level=-10,
            side=Side.LEFT,
            e_modulus=100000,
            angle=1,
            buckling_force=100,
            pre_compression=10,
        )
        model.add_anchor_or_strut(support=floor, stage_id=0)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=1)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        model.add_support(spring_support, 2)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        model.add_support(rigid_support, 3)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        model.add_load(load=uniform_load, stage_id=1)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=3)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        model.execute()

        # 4. Verify succesfull parsing of output datastructure
        assert model.datastructure
        assert model.datastructure.is_valid
        with open("data" + output_test_file.name.split(".")[0] + ".json", "w") as outfile:
            json.dump(model.datastructure.dict(), outfile, ensure_ascii=False, indent=4)

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "modeltype",
        [
            (
                SinglePileModelType(
                    pile_load_option=SinglePileLoadOptions.LOADED_BY_FORCES
                )
            ),
            (
                SinglePileModelType(
                    pile_load_option=SinglePileLoadOptions.LOADED_BY_USER_DEFINED_DISPLACEMENTS
                )
            ),
            (
                SinglePileModelType(
                    pile_load_option=SinglePileLoadOptions.LOADED_BY_CALCULATED_DISPLACEMENTS
                )
            ),
        ],
    )
    def test_acceptance_test_single_pile(self, request, modeltype):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        model.set_model(modeltype)

        # Add construction.
        pile_properties_1 = PileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            note_on_reduction_factor="This is pile 1",
        )
        element_1 = Pile(name="AZ 13", pile_properties=pile_properties_1)
        pile_properties_2 = PileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            note_on_reduction_factor="This is pile 2",
        )
        element_2 = Pile(name="AZ 14", pile_properties=pile_properties_2)
        level_top = 0
        model.set_construction(top_level=level_top, elements=[element_1, element_2])

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay")
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MANUAL
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.earth_pressure_coefficients.earth_pressure_coefficients_type = (
            EarthPressureCoefficientsType.MANUAL
        )
        soil_clay.earth_pressure_coefficients.active = 0.01
        soil_clay.earth_pressure_coefficients.neutral = 0.02
        soil_clay.earth_pressure_coefficients.passive = 0.03
        soil_clay.horizontal_behaviour.horizontal_behavior_type = (
            HorizontalBehaviourType.Elastic
        )

        # set peat material
        soil_peat = Soil(name="Peat")
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MANUAL
        soil_peat.subgrade_reaction_parameters.k_1_top = 2000
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_peat.earth_pressure_coefficients.earth_pressure_coefficients_type = (
            EarthPressureCoefficientsType.BRINCHHANSEN
        )
        soil_peat.horizontal_behaviour.horizontal_behavior_type = (
            HorizontalBehaviourType.Elastic
        )
        soil_peat.horizontal_behaviour.soil_elasticity = 1000
        soil_peat.horizontal_behaviour.soil_default_elasticity = False

        # set sand material
        soil_sand = Soil(name="Sand")
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.MANUAL
        soil_sand.subgrade_reaction_parameters.k_1_top = 2000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_sand.earth_pressure_coefficients.earth_pressure_coefficients_type = (
            EarthPressureCoefficientsType.MANUAL
        )
        soil_sand.earth_pressure_coefficients.active = 0.01
        soil_sand.earth_pressure_coefficients.neutral = 0.02
        soil_sand.earth_pressure_coefficients.passive = 0.03
        soil_sand.horizontal_behaviour.horizontal_behavior_type = (
            HorizontalBehaviourType.Foundation
        )

        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # set unit weight of water

        # Add stage.
        # Inputs passive_side, method_left, method_right are not needed for a single pile calculation but they are defined in the code.
        stage_id = model.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
        )

        # Add soil profile, surfaces, and water level to stage.
        profile = SoilProfile(
            name="New Profile",
            layers=[
                SoilLayer(top_of_layer=0, soil=soil_clay.name),
                SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                SoilLayer(top_of_layer=-13, soil=soil_sand.name),
            ],
        )
        model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

        ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])

        model.add_surface(surface=ground_level_surface, side=Side.BOTH, stage_id=stage_id)

        initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
        model.add_head_line(
            water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
        )

        # Add general calculation options for model
        calc_options = StandardCalculationOptions()
        model.set_calculation_options(calculation_options=calc_options)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=0)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        model.add_support(spring_support, stage_id)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        model.add_support(rigid_support, stage_id)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=0)

        # set displacements
        if (
            modeltype.pile_load_option
            == SinglePileLoadOptions.LOADED_BY_CALCULATED_DISPLACEMENTS
        ):
            # add surcharge load
            surcharge_load = SurchargeLoad(
                name="New SurchargeLoad",
                points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
            )
            model.add_surcharge_load(surcharge_load, side=Side.BOTH, stage_id=stage_id)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        # TODO remove this if statement when GEOLIB-160 is implemented
        if not (
            modeltype.pile_load_option
            == SinglePileLoadOptions.LOADED_BY_USER_DEFINED_DISPLACEMENTS
        ):
            model.execute()

            # 4. Verify successfull parsing of output datastructure
            assert model.datastructure
            assert model.datastructure.is_valid
            with open(
                "data" + output_test_file.name.split(".")[0] + ".json", "w"
            ) as outfile:
                json.dump(
                    model.datastructure.dict(), outfile, ensure_ascii=False, indent=4
                )

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "calc_options",
        [
            (
                VerifyCalculationOptions(
                    input_calculation_type=CalculationType.VERIFY_SHEETPILING,
                    verify_type=VerifyType.EC7NL,
                    ec7_nl_method=PartialFactorCalculationType.METHODB,
                )
            ),
            (StandardCalculationOptions()),
            (
                OverallStabilityCalculationOptions(
                    cur_stability_stage=0,
                    overall_stability_type=DesignType.CUR,
                    stability_cur_partial_factor_set=PartialFactorSetCUR.CLASSII,
                )
            ),
            (KranzAnchorStrengthCalculationOptions(cur_anchor_force_stage=0)),
            (
                DesignSheetpilingLengthCalculationOptions(
                    design_stage=0,
                    design_pile_length_from=20,
                    design_pile_length_to=12,
                    design_pile_length_decrement=0.1,
                    design_type=DesignType.EC7NL,
                    design_partial_factor_set_ec7_nad_nl=PartialFactorSetEC7NADNL.RC1,
                    design_ec7_nl_method=PartialFactorCalculationType.METHODA,
                )
            ),
        ],
    )
    def test_run_sheet_model_acceptance_different_calculation_types_wooden_sheet_pile(
        self, request, calc_options
    ):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
        )
        model.set_model(modeltype)

        # Add construction.
        sheet_pile_properties_1 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        wooden_pile_properties = WoodenSheetPileProperties(
            elasticity_modulus_e_m_0_mean=1e05,
            charac_flexural_strength_f_m_0_char=2.3,
            system_factor_k_sys=1.15,
            deform_factor_k_def=1.1,
            creep_factor_psi_2_eff=1.3,
            material_factor_gamma_m=0.9,
            modif_factor_on_f_m_0_char_short_term_k_mod_f_short=0.65,
            modif_factor_on_f_m_0_char_long_term_k_mod_f_long=0.5,
            modification_factor_on_e_m_0_d_k_mod_e=0.8,
        )
        sheet_element_1 = Sheet(
            name="AZ 13",
            sheet_pile_properties=sheet_pile_properties_1,
            wooden_sheet_pile_properties=wooden_pile_properties,
        )
        sheet_pile_properties_2 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_2 = Sheet(
            name="AZ 14",
            sheet_pile_properties=sheet_pile_properties_2,
            wooden_sheet_pile_properties=wooden_pile_properties,
        )
        level_top = 0
        model.set_construction(
            top_level=level_top, elements=[sheet_element_1, sheet_element_2]
        )

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay")
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.mohr_coulomb_parameters.friction_angle_interface = 11
        soil_clay.shell_factor = 1
        soil_clay.soil_state.ocr_layer = 1
        soil_clay.soil_classification_parameters.grain_type = GrainType.FINE
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.soil_classification_parameters.relative_density = 72
        soil_clay.storage_parameters.horizontal_permeability = 8e-11
        soil_clay.soil_type_settlement_by_vibrations = SoilType.CLAY
        # set peat material
        soil_peat = Soil(name="Peat")
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.mohr_coulomb_parameters.friction_angle_interface = 0
        soil_peat.shell_factor = 1
        soil_peat.soil_state.ocr_layer = 1
        soil_peat.soil_classification_parameters.grain_type = GrainType.FINE
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_peat.subgrade_reaction_parameters.k_1_top = 800
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 800
        soil_peat.soil_classification_parameters.relative_density = 72
        soil_peat.storage_parameters.horizontal_permeability = 8e-10
        soil_peat.soil_type_settlement_by_vibrations = SoilType.PEAT
        # set sand material
        soil_sand = Soil(name="Sand")
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.mohr_coulomb_parameters.friction_angle_interface = 27
        soil_sand.shell_factor = 1
        soil_sand.soil_state.ocr_layer = 1
        soil_sand.soil_classification_parameters.grain_type = GrainType.FINE
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.KOTTER
        soil_sand.subgrade_reaction_parameters.k_1_top = 10000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 10000
        soil_sand.soil_classification_parameters.relative_density = 72
        soil_sand.storage_parameters.horizontal_permeability = 8e-9
        soil_sand.soil_type_settlement_by_vibrations = SoilType.SAND
        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)

        # Add stage.
        stage_id = model.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # Add soil profile, surfaces, and water level to stage.
        profile = SoilProfile(
            name="New Profile",
            layers=[
                SoilLayer(top_of_layer=0, soil=soil_clay.name),
                SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                SoilLayer(top_of_layer=-13, soil=soil_sand.name),
            ],
        )
        model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

        ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
        ground_level_minus_7_meter_surface = Surface(
            name="GL-7", points=[Point(x=0, z=-7)],
        )

        model.add_surface(
            surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
        )
        model.add_surface(
            surface=ground_level_minus_7_meter_surface, side=Side.LEFT, stage_id=stage_id
        )

        initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
        model.add_head_line(
            water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
        )
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # Add general calculation options for model
        model.set_calculation_options(calculation_options=calc_options)
        if isinstance(calc_options, VerifyCalculationOptions):
            calc_options_per_stage = CalculationOptionsPerStage(
                anchor_factor=1.5, partial_factor_set=PartialFactorSetEC7NADNL.RC2
            )
            # stage_id refers to the pythonic input and the conversion in stage number for D-SheetPiling is handled internally
            model.add_calculation_options_per_stage(
                calculation_options_per_stage=calc_options_per_stage, stage_id=stage_id,
            )

        # add anchor
        anchor = Anchor(
            name="Grout anchor",
            level=-2,
            side=Side.RIGHT,
            e_modulus=100000,
            cross_section=10,
            wall_height_kranz=1,
            length=2,
            angle=3,
            yield_force=100,
        )
        model.add_anchor_or_strut(support=anchor, stage_id=stage_id)

        # add strut
        floor = Strut(
            name="Concrete floor",
            level=-10,
            side=Side.LEFT,
            e_modulus=100000,
            angle=1,
            buckling_force=100,
            pre_compression=10,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_anchor_or_strut(support=floor, stage_id=stage_id)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=0)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(spring_support, stage_id)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(rigid_support, stage_id)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        model.add_load(load=uniform_load, stage_id=stage_id)

        # add surcharge load
        surcharge_load = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
        )
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=0)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        model.execute()

        # 4. Verify succesfull parsing of output datastructure
        assert model.datastructure
        assert model.datastructure.is_valid
        with open("data" + output_test_file.name.split(".")[0] + ".json", "w") as outfile:
            json.dump(model.datastructure.dict(), outfile, ensure_ascii=False, indent=4)

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "calc_options",
        [
            (
                VerifyCalculationOptions(
                    input_calculation_type=CalculationType.VERIFY_SHEETPILING,
                    verify_type=VerifyType.EC7NL,
                    ec7_nl_method=PartialFactorCalculationType.METHODB,
                )
            ),
            (StandardCalculationOptions()),
            (
                OverallStabilityCalculationOptions(
                    cur_stability_stage=0,
                    overall_stability_type=DesignType.CUR,
                    stability_cur_partial_factor_set=PartialFactorSetCUR.CLASSII,
                )
            ),
            (KranzAnchorStrengthCalculationOptions(cur_anchor_force_stage=0)),
            (
                DesignSheetpilingLengthCalculationOptions(
                    design_stage=0,
                    design_pile_length_from=20,
                    design_pile_length_to=12,
                    design_pile_length_decrement=0.1,
                    design_type=DesignType.EC7NL,
                    design_partial_factor_set_ec7_nad_nl=PartialFactorSetEC7NADNL.RC1,
                    design_ec7_nl_method=PartialFactorCalculationType.METHODA,
                )
            ),
        ],
    )
    def test_run_sheet_model_acceptance_different_calculation_types_diaphragm_wall(
        self, request, calc_options
    ):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
        )
        model.set_model(modeltype)

        # Add construction.
        diaphragm_wall_properties_1 = DiaphragmWallProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            reduction_factor_on_ei=0.1,
            note_on_reduction_factor="Note on wall 1",
            mr_char_el=312,
            mr_char_pl=392,
            modification_factor_k_mod=0.9,
            material_factor_gamma_m=0.8,
            reduction_factor_on_maximum_moment=0.1,
        )
        plastic_properties_1 = FullPlasticCalculationProperties(
            eI_branch_2_positive=20000,
            eI_branch_2_negative=20000,
            moment_point_1_positive=0,
            moment_point_1_negative=0,
            plastic_moment_positive=0,
            plastic_moment_negative=0,
            eI_branch_3_positive=20000,
            moment_point_2_positive=0,
            eI_branch_3_negative=20000,
            moment_point_2_negative=0,
        )
        sheet_element_1 = DiaphragmWall(
            name="AZ 13",
            diaphragm_wall_properties=diaphragm_wall_properties_1,
            plastic_properties=plastic_properties_1,
        )
        diaphragm_wall_properties_2 = DiaphragmWallProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            reduction_factor_on_ei=0.1,
            note_on_reduction_factor="Note on wall 1",
            mr_char_el=312,
            mr_char_pl=392,
            modification_factor_k_mod=0.9,
            material_factor_gamma_m=0.8,
            reduction_factor_on_maximum_moment=0.1,
        )
        plastic_properties_2 = FullPlasticCalculationProperties(
            eI_branch_2_positive=30000,
            eI_branch_2_negative=30000,
            moment_point_1_positive=1,
            moment_point_1_negative=1,
            plastic_moment_positive=1,
            plastic_moment_negative=1,
            eI_branch_3_positive=30000,
            moment_point_2_positive=1,
            eI_branch_3_negative=30000,
            moment_point_2_negative=1,
        )
        sheet_element_2 = DiaphragmWall(
            name="AZ 14",
            diaphragm_wall_properties=diaphragm_wall_properties_2,
            plastic_properties=plastic_properties_2,
        )
        level_top = 0
        model.set_construction(
            top_level=level_top, elements=[sheet_element_1, sheet_element_2]
        )

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay")
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.mohr_coulomb_parameters.friction_angle_interface = 11
        soil_clay.shell_factor = 1
        soil_clay.soil_state.ocr_layer = 1
        soil_clay.soil_classification_parameters.grain_type = GrainType.FINE
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.soil_classification_parameters.relative_density = 72
        soil_clay.storage_parameters.horizontal_permeability = 8e-11
        soil_clay.soil_type_settlement_by_vibrations = SoilType.CLAY
        # set peat material
        soil_peat = Soil(name="Peat")
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.mohr_coulomb_parameters.friction_angle_interface = 0
        soil_peat.shell_factor = 1
        soil_peat.soil_state.ocr_layer = 1
        soil_peat.soil_classification_parameters.grain_type = GrainType.FINE
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_peat.subgrade_reaction_parameters.k_1_top = 800
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 800
        soil_peat.soil_classification_parameters.relative_density = 72
        soil_peat.storage_parameters.horizontal_permeability = 8e-10
        soil_peat.soil_type_settlement_by_vibrations = SoilType.PEAT
        # set sand material
        soil_sand = Soil(name="Sand")
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.mohr_coulomb_parameters.friction_angle_interface = 27
        soil_sand.shell_factor = 1
        soil_sand.soil_state.ocr_layer = 1
        soil_sand.soil_classification_parameters.grain_type = GrainType.FINE
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.KOTTER
        soil_sand.subgrade_reaction_parameters.k_1_top = 10000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 10000
        soil_sand.soil_classification_parameters.relative_density = 72
        soil_sand.storage_parameters.horizontal_permeability = 8e-9
        soil_sand.soil_type_settlement_by_vibrations = SoilType.SAND
        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)

        # Add stage.
        stage_id = model.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # Add soil profile, surfaces, and water level to stage.
        profile = SoilProfile(
            name="New Profile",
            layers=[
                SoilLayer(top_of_layer=0, soil=soil_clay.name),
                SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                SoilLayer(top_of_layer=-13, soil=soil_sand.name),
            ],
        )
        model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

        ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
        ground_level_minus_7_meter_surface = Surface(
            name="GL-7", points=[Point(x=0, z=-7)],
        )

        model.add_surface(
            surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
        )
        model.add_surface(
            surface=ground_level_minus_7_meter_surface, side=Side.LEFT, stage_id=stage_id
        )

        initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
        model.add_head_line(
            water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
        )
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # Add general calculation options for model
        model.set_calculation_options(calculation_options=calc_options)
        if isinstance(calc_options, VerifyCalculationOptions):
            calc_options_per_stage = CalculationOptionsPerStage(
                anchor_factor=1.5, partial_factor_set=PartialFactorSetEC7NADNL.RC2
            )
            # stage_id refers to the pythonic input and the conversion in stage number for D-SheetPiling is handled internally
            model.add_calculation_options_per_stage(
                calculation_options_per_stage=calc_options_per_stage, stage_id=stage_id,
            )

        # add anchor
        anchor = Anchor(
            name="Grout anchor",
            level=-2,
            side=Side.RIGHT,
            e_modulus=100000,
            cross_section=10,
            wall_height_kranz=1,
            length=2,
            angle=3,
            yield_force=100,
        )
        model.add_anchor_or_strut(support=anchor, stage_id=stage_id)

        # add strut
        floor = Strut(
            name="Concrete floor",
            level=-10,
            side=Side.LEFT,
            e_modulus=100000,
            angle=1,
            buckling_force=100,
            pre_compression=10,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_anchor_or_strut(support=floor, stage_id=stage_id)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=0)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(spring_support, stage_id)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(rigid_support, stage_id)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        model.add_load(load=uniform_load, stage_id=stage_id)

        # add surcharge load
        surcharge_load = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
        )
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=0)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        model.execute()

        # 4. Verify succesfull parsing of output datastructure
        assert model.datastructure
        assert model.datastructure.is_valid
        with open("data" + output_test_file.name.split(".")[0] + ".json", "w") as outfile:
            json.dump(model.datastructure.dict(), outfile, ensure_ascii=False, indent=4)

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "calc_options",
        [
            (
                VerifyCalculationOptions(
                    input_calculation_type=CalculationType.VERIFY_SHEETPILING,
                    verify_type=VerifyType.EC7NL,
                    ec7_nl_method=PartialFactorCalculationType.METHODB,
                )
            ),
            (StandardCalculationOptions()),
            (
                OverallStabilityCalculationOptions(
                    cur_stability_stage=0,
                    overall_stability_type=DesignType.CUR,
                    stability_cur_partial_factor_set=PartialFactorSetCUR.CLASSII,
                )
            ),
            (KranzAnchorStrengthCalculationOptions(cur_anchor_force_stage=0)),
            (
                DesignSheetpilingLengthCalculationOptions(
                    design_stage=0,
                    design_pile_length_from=20,
                    design_pile_length_to=12,
                    design_pile_length_decrement=0.1,
                    design_type=DesignType.EC7NL,
                    design_partial_factor_set_ec7_nad_nl=PartialFactorSetEC7NADNL.RC1,
                    design_ec7_nl_method=PartialFactorCalculationType.METHODA,
                )
            ),
        ],
    )
    def test_run_sheet_model_plastic_pile_acceptance_different_calculation_types(
        self, request, calc_options
    ):
        # 0. Set up test data.
        model = DSheetPilingModel()
        test_name_with_id = request.node.name
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsheetpiling"))
        output_test_file = output_test_folder / f"{test_name_with_id}.shi"

        # 1. Build model.
        modeltype = SheetModelType(
            method=LateralEarthPressureMethod.MIXED,
            check_vertical_balance=False,
            trildens_calculation=True,
            verification=True,
            elastic_calculation=False,
        )
        model.set_model(modeltype)

        # Add construction.
        sheet_pile_properties_1 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-10,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_pile_plastic_properties_1 = SheetPileModelPlasticCalculationProperties(
            symmetrical=True, plastic_moment_positive=10, plastic_moment_negative=20,
        )
        sheet_element_1 = Sheet(
            name="AZ 13",
            sheet_pile_properties=sheet_pile_properties_1,
            plastic_properties=sheet_pile_plastic_properties_1,
        )
        sheet_pile_properties_2 = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            section_bottom_level=-16,
            elastic_stiffness_ei=4.137e4,
            acting_width=1,
            mr_char_el=312,
            modification_factor_k_mod=1,
            material_factor_gamma_m=1,
            reduction_factor_on_maximum_moment=1,
            reduction_factor_on_ei=1,
            section_area=137,
            elastic_section_modulus_w_el=1300,
            coating_area=1.23,
            height=303.0,
        )
        sheet_element_2 = Sheet(
            name="AZ 14",
            sheet_pile_properties=sheet_pile_properties_2,
            plastic_properties=sheet_pile_plastic_properties_1,
        )
        level_top = 0
        model.set_construction(
            top_level=level_top, elements=[sheet_element_1, sheet_element_2]
        )

        # Add soil
        # Set clay material
        soil_clay = Soil(name="Clay")
        soil_clay.soil_weight_parameters.unsaturated_weight = 10
        soil_clay.soil_weight_parameters.saturated_weight = 11
        soil_clay.mohr_coulomb_parameters.cohesion = 10
        soil_clay.mohr_coulomb_parameters.friction_angle = 17
        soil_clay.mohr_coulomb_parameters.friction_angle_interface = 11
        soil_clay.shell_factor = 1
        soil_clay.soil_state.ocr_layer = 1
        soil_clay.soil_classification_parameters.grain_type = GrainType.FINE
        soil_clay.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_clay.subgrade_reaction_parameters.k_1_top = 2000
        soil_clay.subgrade_reaction_parameters.k_1_bottom = 2000
        soil_clay.soil_classification_parameters.relative_density = 72
        soil_clay.storage_parameters.horizontal_permeability = 8e-11
        soil_clay.soil_type_settlement_by_vibrations = SoilType.CLAY
        # set peat material
        soil_peat = Soil(name="Peat")
        soil_peat.soil_weight_parameters.unsaturated_weight = 10
        soil_peat.soil_weight_parameters.saturated_weight = 11
        soil_peat.mohr_coulomb_parameters.cohesion = 2
        soil_peat.mohr_coulomb_parameters.friction_angle = 20
        soil_peat.mohr_coulomb_parameters.friction_angle_interface = 0
        soil_peat.shell_factor = 1
        soil_peat.soil_state.ocr_layer = 1
        soil_peat.soil_classification_parameters.grain_type = GrainType.FINE
        soil_peat.subgrade_reaction_parameters.lambda_type = LambdaType.MULLERBRESLAU
        soil_peat.subgrade_reaction_parameters.k_1_top = 800
        soil_peat.subgrade_reaction_parameters.k_1_bottom = 800
        soil_peat.soil_classification_parameters.relative_density = 72
        soil_peat.storage_parameters.horizontal_permeability = 8e-10
        soil_peat.soil_type_settlement_by_vibrations = SoilType.PEAT
        # set sand material
        soil_sand = Soil(name="Sand")
        soil_sand.soil_weight_parameters.unsaturated_weight = 17
        soil_sand.soil_weight_parameters.saturated_weight = 19
        soil_sand.mohr_coulomb_parameters.cohesion = 0
        soil_sand.mohr_coulomb_parameters.friction_angle = 35
        soil_sand.mohr_coulomb_parameters.friction_angle_interface = 27
        soil_sand.shell_factor = 1
        soil_sand.soil_state.ocr_layer = 1
        soil_sand.soil_classification_parameters.grain_type = GrainType.FINE
        soil_sand.subgrade_reaction_parameters.lambda_type = LambdaType.KOTTER
        soil_sand.subgrade_reaction_parameters.k_1_top = 10000
        soil_sand.subgrade_reaction_parameters.k_1_bottom = 10000
        soil_sand.soil_classification_parameters.relative_density = 72
        soil_sand.storage_parameters.horizontal_permeability = 8e-9
        soil_sand.soil_type_settlement_by_vibrations = SoilType.SAND
        # add soils in model
        for soil in (soil_clay, soil_peat, soil_sand):
            model.add_soil(soil)

        # Add stage.
        stage_id = model.add_stage(
            name="New Stage",
            passive_side=PassiveSide.DSHEETPILING_DETERMINED,
            method_left=LateralEarthPressureMethodStage.C_PHI_DELTA,
            method_right=LateralEarthPressureMethodStage.C_PHI_DELTA,
            pile_top_displacement=0.01,
        )

        # Add soil profile, surfaces, and water level to stage.
        profile = SoilProfile(
            name="New Profile",
            layers=[
                SoilLayer(top_of_layer=0, soil=soil_clay.name),
                SoilLayer(top_of_layer=-4, soil=soil_peat.name),
                SoilLayer(top_of_layer=-6, soil=soil_clay.name),
                SoilLayer(top_of_layer=-13, soil=soil_sand.name),
            ],
        )
        model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

        ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
        ground_level_minus_7_meter_surface = Surface(
            name="GL-7", points=[Point(x=0, z=-7)],
        )

        model.add_surface(
            surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
        )
        model.add_surface(
            surface=ground_level_minus_7_meter_surface, side=Side.LEFT, stage_id=stage_id
        )

        initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
        model.add_head_line(
            water_level=initial_water_level, side=Side.BOTH, stage_id=stage_id
        )
        curve_settings = CurveSettings(
            modulus_reaction_type=ModulusReactionType.TANGENT, curve_number=1
        )
        model.set_curve_settings(curve_settings=curve_settings)

        # Add general calculation options for model
        model.set_calculation_options(calculation_options=calc_options)
        if isinstance(calc_options, VerifyCalculationOptions):
            calc_options_per_stage = CalculationOptionsPerStage(
                anchor_factor=1.5, partial_factor_set=PartialFactorSetEC7NADNL.RC2
            )
            # stage_id refers to the pythonic input and the conversion in stage number for D-SheetPiling is handled internally
            model.add_calculation_options_per_stage(
                calculation_options_per_stage=calc_options_per_stage, stage_id=stage_id,
            )

        # add anchor
        anchor = Anchor(
            name="Grout anchor",
            level=-2,
            side=Side.RIGHT,
            e_modulus=100000,
            cross_section=10,
            wall_height_kranz=1,
            length=2,
            angle=3,
            yield_force=100,
        )
        model.add_anchor_or_strut(support=anchor, stage_id=stage_id)

        # add strut
        floor = Strut(
            name="Concrete floor",
            level=-10,
            side=Side.LEFT,
            e_modulus=100000,
            angle=1,
            buckling_force=100,
            pre_compression=10,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_anchor_or_strut(support=floor, stage_id=stage_id)

        # add horizontal line load
        load = HorizontalLineLoad(name="New HorizontalLineLoad", level=-1, load=10)
        model.add_load(load=load, stage_id=0)

        # add spring support
        spring_support = SpringSupport(
            name="Jerry", level=-15, rotational_stiffness=50, translational_stiffness=50
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(spring_support, stage_id)

        # add rigid support
        rigid_support = RigidSupport(
            name="Redgy", level=-13, support_type=SupportType.ROTATION,
        )
        # For KranzAnchorStrengthCalculationOptions only one support should be present
        if not (isinstance(calc_options, KranzAnchorStrengthCalculationOptions)):
            model.add_support(rigid_support, stage_id)

        # add moment load
        moment_load = Moment(name="New Moment", level=-4, load=10,)
        model.add_load(load=moment_load, stage_id=0)

        # add uniform load
        uniform_load = UniformLoad(name="New UniformLoad", left_load=10, right_load=12.5)
        model.add_load(load=uniform_load, stage_id=stage_id)

        # add surcharge load
        surcharge_load = SurchargeLoad(
            name="New SurchargeLoad",
            points=[Point(x=0, z=5), Point(x=5, z=10), Point(x=10, z=0)],
        )
        model.add_surcharge_load(surcharge_load, side=Side.LEFT, stage_id=stage_id)

        # add normal force
        normal_force = NormalForce(
            name="New normal force",
            force_at_sheet_pile_top=5,
            force_at_surface_level_left_side=5,
            force_at_surface_level_right_side=5,
            force_at_sheet_pile_toe=5,
        )
        model.add_load(load=normal_force, stage_id=0)

        # 2. Verify initial expectations.
        model.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        model.filename = output_test_file
        model.execute(timeout_in_seconds=1000)

        # 4. Verify succesfull parsing of output datastructure
        assert model.datastructure
        assert model.datastructure.is_valid
        with open("data" + output_test_file.name.split(".")[0] + ".json", "w") as outfile:
            json.dump(model.datastructure.dict(), outfile, ensure_ascii=False, indent=4)
