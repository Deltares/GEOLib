import logging
import os
from pathlib import Path
from typing import Type

import pytest
from teamcity import is_running_under_teamcity

from geolib.errors import CalculationError
from geolib.geometry.one import Point
from geolib.models import BaseModel, DFoundationsModel
from geolib.models.dfoundations.dfoundations_model import (
    BearingPilesModel,
    CalculationOptions,
    TensionPilesModel,
)
from geolib.models.dfoundations.internal import (
    CalculationOptions as InternalCalculationOptions,
)
from geolib.models.dfoundations.internal import (
    DFoundationsDumpStructure,
    DFoundationsStructure,
    LoadSettlementCurve,
    MainCalculationType,
    ModelTypeEnum,
    SubCalculationType,
)
from geolib.models.dfoundations.piles import (
    BasePileType,
    BasePileTypeForClayLoamPeat,
    BearingHShapedPile,
    BearingPileLocation,
    BearingRectangularPile,
    BearingRectangularPileWithEnlargedBase,
    BearingRoundHollowPileWithClosedBase,
    BearingRoundOpenEndedHollowPile,
    BearingRoundPile,
    BearingRoundPileWithEnlargedBase,
    BearingRoundPileWithInSituFormedBase,
    BearingRoundPileWithLostTip,
    BearingRoundTaperedPile,
    BearingSection,
    TensionHShapedPile,
    TensionPileLocation,
    TensionRectangularPile,
    TensionRectangularPileWithEnlargedBase,
    TensionRoundHollowPileWithClosedBase,
    TensionRoundOpenEndedHollowPile,
    TensionRoundPile,
    TensionRoundPileWithEnlargedBase,
    TensionRoundPileWithInSituFormedBase,
    TensionRoundPileWithLostTip,
    TensionRoundTaperedPile,
    TensionSection,
)
from geolib.models.dfoundations.profiles import CPT, Excavation, Profile
from geolib.models.internal import Bool
from geolib.soils import MohrCoulombParameters, Soil, SoilType
from tests.utils import TestUtils, only_teamcity


class TestDFoundationsModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DFoundationsModel_instance(self):
        dfoundation_model = DFoundationsModel()
        assert dfoundation_model is not None
        assert isinstance(dfoundation_model, BaseModel), (
            "" + "DFoundationsModel does not instanciate BaseModel"
        )

    @pytest.mark.unittest
    def test_ensure_newlines_run_identification(self):
        dfoundation_model = DFoundationsModel()
        assert dfoundation_model is not None
        # Default is 6
        assert (
            dfoundation_model.datastructure.input_data.run_identification.count("\n") == 6
        )
        # Less than that should be set to 6 again
        dfoundation_model.datastructure.input_data.run_identification = ""
        assert (
            dfoundation_model.datastructure.input_data.run_identification.count("\n") == 6
        )
        # More than that should be left as is
        dfoundation_model.datastructure.input_data.run_identification = 8 * "\n"
        assert (
            dfoundation_model.datastructure.input_data.run_identification.count("\n") == 8
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename,structure",
        [
            pytest.param(Path("bm1-1a.foi"), DFoundationsStructure, id="Input file"),
            pytest.param(Path("bm1-1a.fod"), DFoundationsDumpStructure, id="Output file"),
        ],
    )
    def test_given_filepath_when_parse_then_does_not_raise(
        self, filename: Path, structure: Type
    ):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / filename
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.is_file()

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert isinstance(ds.datastructure, structure)

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1a.foi"), id="Input file")],
    )
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / filename
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / filename
        ds = DFoundationsModel()

        # 2. Verify initial expectations
        assert test_file.is_file()
        if output_test_file.is_file():
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DFoundationsStructure)
        input_datastructure = dict(ds.datastructure.input_data)

        # 4.2. Read the generated data.
        assert output_test_file.is_file()
        output_datastructure = dict(
            DFoundationsModel().parse(output_test_file).input_data
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
            print(errors)
            pytest.fail(f"Failed with the following {errors}")

    @pytest.mark.acceptance
    @only_teamcity
    def test_execute_console_successfully(self):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test.foi"

        df.parse(test_file)
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert output_test_file.is_file()

        # 3. Run test.
        df.filename = output_test_file
        model = df.execute()

        # 3. Verify model output has been parsed
        assert model

    @pytest.mark.unittest
    def test_execute_console_without_filename_raises_exception(self):
        # 1. Set up test data.
        df = DFoundationsModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.integrationtest
    def test_add_generic_soil(self):
        # 1. Set up test data
        ds = DFoundationsModel()

        mohr_coulomb_parameters = MohrCoulombParameters(friction_angle=0.01)
        soil = Soil(
            name="Test Soil",
            soil_type_nl=SoilType.CLAY,
            mohr_coulomb_parameters=mohr_coulomb_parameters,
        )
        soil.undrained_parameters.undrained_shear_strength = 1000
        output_test_folder = Path(
            TestUtils.get_output_test_data_dir("dfoundations/serialize/")
        )
        output_test_file = output_test_folder / "soils.foi"

        # 2. Verify initial expectations
        assert ds.datastructure.input_data.soil_collection.soil

        # 3. Run test.
        new_soil = ds.add_soil(soil)

        # 4. Verify final expectations.
        assert ds.datastructure.input_data.soil_collection.soil[-1].name == "Test Soil"

        # 5. Serialize result to check manually
        ds.serialize(output_test_file)

    @pytest.mark.integrationtest
    def test_add_soil_with_soil_type(self):
        # 1. Set up test data
        df = DFoundationsModel()

        mohr_coulomb_parameters = MohrCoulombParameters(friction_angle=0.01)

        gravel = Soil(name="Gravel")
        gravel.soil_type_nl = SoilType.GRAVEL
        gravel.soil_type_be = SoilType.GRAVEL
        gravel.mohr_coulomb_parameters = mohr_coulomb_parameters
        gravel.undrained_parameters.undrained_shear_strength = 1000

        sandy_loam = Soil(name="Sandy loam")
        sandy_loam.soil_type_nl = SoilType.SANDY_LOAM
        sandy_loam.soil_type_be = SoilType.SANDY_LOAM
        sandy_loam.mohr_coulomb_parameters = mohr_coulomb_parameters
        sandy_loam.undrained_parameters.undrained_shear_strength = 1000

        sandy_loam_and_gravel = Soil(name="Sandy loam")
        sandy_loam_and_gravel.soil_type_nl = SoilType.SANDY_LOAM
        sandy_loam_and_gravel.soil_type_be = SoilType.GRAVEL
        sandy_loam_and_gravel.mohr_coulomb_parameters = mohr_coulomb_parameters
        sandy_loam_and_gravel.undrained_parameters.undrained_shear_strength = 1000

        # 3. Run test
        df.add_soil(gravel)
        with pytest.raises(ValueError):
            df.add_soil(sandy_loam)
        df.add_soil(sandy_loam_and_gravel)

        # 4. Verify final expectations.
        assert (
            df.datastructure.input_data.soil_collection.soil[-2].soilsoiltype
            == SoilType.GRAVEL
        )
        assert (
            df.datastructure.input_data.soil_collection.soil[-2].soilbelgiansoiltype
            == SoilType.GRAVEL
        )

        assert (
            df.datastructure.input_data.soil_collection.soil[-1].soilsoiltype
            == SoilType.SANDY_LOAM
        )
        assert (
            df.datastructure.input_data.soil_collection.soil[-1].soilbelgiansoiltype
            == SoilType.GRAVEL
        )

    @pytest.fixture
    def setup_profile(self):
        cpt = CPT(
            cptname="DELFT1",
            groundlevel=0.5,
            measured_data=[
                {"z": 0.0, "qc": 0.1},
                {"z": -0.10, "qc": 0.5},
                {"z": -0.20, "qc": 2.0},
                {"z": -0.30, "qc": 3.0},
                {"z": -0.40, "qc": 5.0},
                {"z": -10, "qc": 1.0},
                {"z": -15, "qc": 5.0},
                {"z": -25, "qc": 5.0},
                {"z": -30, "qc": 35.0},
            ],
        )
        excavation = Excavation(excavation_level=-0.1)
        location = Point(x=1.0, y=2.0)
        profile = Profile(
            name="DELFT1",
            location=location,
            phreatic_level=-0.5,
            pile_tip_level=-0.5,
            cpt=cpt,
            top_of_positive_skin_friction=-0.2,
            excavation=excavation,
            layers=[
                {
                    "material": "Clay, clean, stiff",
                    "top_level": 0,
                    "excess_pore_pressure_top": 0.0,
                    "excess_pore_pressure_bottom": 0.0,
                    "ocr_value": 1.0,
                    "reduction_core_resistance": 0,
                },
                {
                    "material": "Clay, clean, weak",
                    "top_level": -0.2,
                    "excess_pore_pressure_top": 0.0,
                    "excess_pore_pressure_bottom": 0.0,
                    "ocr_value": 1.0,
                    "reduction_core_resistance": 0,
                },
                {
                    "material": "Clay, clean, stiff",
                    "top_level": -0.3,
                    "excess_pore_pressure_top": 0.0,
                    "excess_pore_pressure_bottom": 0.0,
                    "ocr_value": 1.0,
                    "reduction_core_resistance": 0,
                },
            ],
        )
        return profile

    @pytest.mark.integrationtest
    def test_add_profile(self, setup_profile):
        df = DFoundationsModel()

        assert len(df.profiles.profiles) == 0
        assert len(df.cpts.cpt_collection) == 0

        df.add_profile(setup_profile)

        assert len(df.profiles.profiles) == 1
        assert len(df.cpts.cpt_collection) == 1

    @pytest.mark.integrationtest
    def test_add_profile_with_non_existing_soil(self, setup_profile):
        df = DFoundationsModel()

        setup_profile.layers.append(
            {
                "material": "Foo Bar Clay",
                "top_level": -0.3,
                "reduction_core_resistance": 0,
            },
        )
        with pytest.raises(KeyError):
            df.add_profile(setup_profile)

    @pytest.mark.acceptance
    @only_teamcity
    def test_run_model_from_scratch(self, setup_profile):
        # 1. Set up test data.
        df = DFoundationsModel()
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "acceptance_from_scratch.foi"

        # Setup from scratch data here
        # soils are already added by default
        df.add_profile(setup_profile)

        # Add Bearing Pile
        location = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = dict(
            pile_name="test",
            pile_type=BasePileType.USER_DEFINED_VIBRATING,
            pile_class_factor_shaft_sand_gravel=1,
            preset_pile_class_factor_shaft_clay_loam_peat=BasePileTypeForClayLoamPeat.STANDARD,
            pile_class_factor_shaft_clay_loam_peat=1,
            pile_class_factor_tip=1,
            load_settlement_curve=LoadSettlementCurve.ONE,
            user_defined_pile_type_as_prefab=False,
            use_manual_reduction_for_qc=False,
            elasticity_modulus=1e7,
            characteristic_adhesion=10,
            overrule_pile_tip_shape_factor=False,
            overrule_pile_tip_cross_section_factors=False,
        )
        pile = BearingRectangularPile(**parent_pile, **geometry_pile)
        df.add_pile_if_unique(pile, location)

        # 2. Verify initial expectations.
        df.serialize(output_test_file)
        assert output_test_file.is_file()

        # 3. Run test.
        df.filename = output_test_file
        model = df.execute()

        # 3. Verify model output has been parsed
        assert model

    @pytest.mark.integrationtest
    def test_add_bearing_pile_location(self, create_bearing_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_bearing_pile_location.foi"

        df.parse(test_file)

        location = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_bearing_pile
        pile = BearingRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location)

        positions = df.datastructure.input_data.positions___bearing_piles.positions

        # Assert if pile is added
        assert len(positions) == 1
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"

        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_two_equal_bearing_pile_locations(self, create_bearing_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_bearing_pile_location.foi"

        df.parse(test_file)

        location = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_bearing_pile
        pile = BearingRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location)
        df.add_pile_if_unique(pile, location)

        positions = df.datastructure.input_data.positions___bearing_piles.positions
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert len(positions) == 1
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"
        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_two_unique_bearing_pile_locations(self, create_bearing_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_two_bearing_pile_locations.foi"

        df.parse(test_file)

        location_1 = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add a new pile
        location_2 = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_bearing_pile
        pile = BearingRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location_1)
        df.add_pile_if_unique(pile, location_2)

        positions = df.datastructure.input_data.positions___bearing_piles.positions
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert len(positions) == 2
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"
        assert positions[1].index == 2
        assert positions[1].pile_name == "'Pos(2)'"
        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_tension_pile_location(self, create_tension_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_tension_pile_location.foi"

        df.parse(test_file)

        location = TensionPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            use_alternating_loads=False,
            max_force=1,
            min_force=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_tension_pile
        pile = TensionRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location)

        positions = df.datastructure.input_data.positions___tension_piles_cur.positions

        # Assert if pile is added
        assert len(positions) == 1
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"

        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_two_equal_tension_pile_locations(self, create_tension_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_two_tension_pile_locations.foi"

        df.parse(test_file)

        location = TensionPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            use_alternating_loads=False,
            max_force=1,
            min_force=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_tension_pile
        pile = TensionRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location)
        df.add_pile_if_unique(pile, location)

        positions = df.datastructure.input_data.positions___tension_piles_cur.positions
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert len(positions) == 1
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"
        assert output_test_file.is_file()

    @pytest.mark.integrationtest
    def test_add_two_unique_tension_pile_locations(self, create_tension_pile):
        # 1. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / "test_add_two_tension_pile_locations.foi"

        df.parse(test_file)

        location_1 = TensionPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            use_alternating_loads=False,
            max_force=1,
            min_force=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add a new pile
        location_2 = TensionPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            use_alternating_loads=False,
            max_force=1,
            min_force=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # Add the pile
        geometry_pile = dict(base_width=1, base_length=1)
        parent_pile = create_tension_pile
        pile = TensionRectangularPile(**parent_pile, **geometry_pile)

        df.add_pile_if_unique(pile, location_1)
        df.add_pile_if_unique(pile, location_2)

        positions = df.datastructure.input_data.positions___tension_piles_cur.positions
        df.serialize(output_test_file)

        # 2. Verify initial expectations.
        assert len(positions) == 2
        assert positions[0].index == 1
        assert positions[0].pile_name == "'Pos(1)'"
        assert positions[1].index == 2
        assert positions[1].pile_name == "'Pos(2)'"
        assert output_test_file.is_file()

    @pytest.mark.acceptance
    @only_teamcity
    def test_bearing_pile(self, create_bearing_pile, create_bearing_pile_shape):

        # 1. Get test information
        test_file_name = create_bearing_pile_shape[0]
        geometry_pile = create_bearing_pile_shape[1]
        pile_shape = create_bearing_pile_shape[2]

        # 2. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"

        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / test_file_name

        df.parse(test_file)

        parent_pile = create_bearing_pile
        pile = pile_shape(**parent_pile, **geometry_pile)

        location = BearingPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            surcharge=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # 3. Run test
        df.add_pile_if_unique(pile, location)
        df.serialize(output_test_file)

        # 4. Verify initial expectations.
        assert output_test_file.is_file()

        # 5. Run test.
        df.filename = output_test_file

        # 6. Verify model output has been parsed.
        with pytest.raises(CalculationError) as e:
            df.execute()

        assert "Number of CPTs (0 ) is outside its limits" in e.value.message

    @pytest.mark.acceptance
    @only_teamcity
    def test_tension_pile(self, create_tension_pile, create_tension_pile_shape):

        # 1. Get test information
        test_file_name = create_tension_pile_shape[0]
        geometry_pile = create_tension_pile_shape[1]
        pile_shape = create_tension_pile_shape[2]

        # 2. Set up test data.
        df = DFoundationsModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dfoundations"))
        test_file = test_folder / "bm1-1a.foi"

        output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
        output_test_file = output_test_folder / test_file_name

        df.parse(test_file)

        parent_pile = create_tension_pile
        pile = pile_shape(**parent_pile, **geometry_pile)

        location = TensionPileLocation(
            point=Point(x=1.0, y=1.0),
            pile_head_level=1,
            use_alternating_loads=False,
            max_force=1,
            min_force=1,
            limit_state_str=1,
            limit_state_service=1,
        )

        # 3. Run test
        df.add_pile_if_unique(pile, location)
        df.serialize(output_test_file)

        # 4. Verify initial expectations.
        assert output_test_file.is_file()

        # 5. Run test.
        df.filename = output_test_file

        # 3. Verify model output has been parsed.
        with pytest.raises(CalculationError) as e:
            df.execute()

        assert "Number of CPTs (0 ) is outside its limits" in e.value.message

    @pytest.mark.integrationtest
    def test_set_model_options(self):
        # Setup
        df = DFoundationsModel()

        # Integration
        mo = BearingPilesModel(is_rigid=False, factor_xi3=9)
        cp = CalculationOptions(
            calculationtype=SubCalculationType.VERIFICATION_DESIGN, cpt_test_level=-50.0
        )
        df.set_model(mo, cp)

        # Verify
        assert df.input.model.model == ModelTypeEnum.BEARING_PILES
        assert (
            df.input.calculationtype.sub_calculationtype
            == SubCalculationType.VERIFICATION_DESIGN
        )
        assert df.input.calculation_options.is_rigid == False
        assert df.input.calculation_options.factor_xi3 == 9
        assert (
            df.input.calculationtype.main_calculationtype
            == MainCalculationType.VERIFICATION_DESIGN
        )
        assert df.input.preliminary_design.cpt_test_level == -50.0

    @pytest.mark.integrationtest
    def test_default_soils_generated_on_model_change(self):

        # Setup
        df = DFoundationsModel()
        mo = BearingPilesModel(is_rigid=False, factor_xi3=9)
        mo_change = TensionPilesModel(is_rigid=False, factor_xi3=9)

        cp = CalculationOptions(
            calculationtype=SubCalculationType.VERIFICATION_DESIGN, cpt_test_level=-50.0
        )
        df.set_model(mo, cp)

        # Check assumptions
        assert len(df.soils.soil) != 0
        assert df.soils.soil[0].name == "BClay, clean, moderate"
        assert df.soils.soil[0].soilgamdry == 18

        # Change model
        df.set_model(mo_change, cp)

        # Verify soils have changed
        assert len(df.soils.soil) != 0
        assert df.soils.soil[0].name == "BClay, clean, moderate"
        assert df.soils.soil[0].soilgamdry == 17

    @pytest.mark.unittest
    def test_calculation_options_when_value_set_toggle_true(self):
        # Setup
        co = InternalCalculationOptions()

        # Check expectations
        co.factor_xi3 == 2
        co.is_xi3_overruled == Bool.FALSE

        # Test
        co = InternalCalculationOptions(factor_xi3=0.1)

        # Verify expectations
        assert co.factor_xi3 == 0.1
        assert co.is_xi3_overruled == Bool.TRUE


@pytest.fixture
def create_bearing_pile():
    return dict(
        pile_name="test",
        pile_type=BasePileType.USER_DEFINED_VIBRATING,
        pile_class_factor_shaft_sand_gravel=1,
        preset_pile_class_factor_shaft_clay_loam_peat=BasePileTypeForClayLoamPeat.STANDARD,
        pile_class_factor_shaft_clay_loam_peat=1,
        pile_class_factor_tip=1,
        load_settlement_curve=LoadSettlementCurve.ONE,
        user_defined_pile_type_as_prefab=False,
        use_manual_reduction_for_qc=False,
        elasticity_modulus=1e7,
        characteristic_adhesion=10,
        overrule_pile_tip_shape_factor=False,
        overrule_pile_tip_cross_section_factors=False,
    )


@pytest.fixture
def create_tension_pile():
    return dict(
        pile_name="test",
        pile_type=BasePileType.USER_DEFINED_VIBRATING,
        pile_class_factor_shaft_sand_gravel=1,
        preset_pile_class_factor_shaft_clay_loam_peat=BasePileTypeForClayLoamPeat.STANDARD,
        pile_class_factor_shaft_clay_loam_peat=1,
        elasticity_modulus=1e7,
        unit_weight_pile=20,
    )


@pytest.fixture(
    params=[
        ["test_add_bearing_round_pile.foi", dict(diameter=1), BearingRoundPile],
        [
            "test_add_bearing_rectangular_pile.foi",
            dict(base_width=1, base_length=1),
            BearingRectangularPile,
        ],
        [
            "test_add_bearing_round_pile_with_enlarged_base.foi",
            dict(base_diameter=1, pile_diameter=0.9, base_height=1),
            BearingRoundPileWithEnlargedBase,
        ],
        [
            "test_add_bearing_rectangular_pile_with_enlarged_base.foi",
            dict(
                base_width_v=1,
                base_length_v=1,
                base_height=1,
                shaft_width=1,
                shaft_length=1,
            ),
            BearingRectangularPileWithEnlargedBase,
        ],
        [
            "test_add_bearing_round_tapered_pile.foi",
            dict(diameter_at_pile_tip=1, increase_in_diameter=1),
            BearingRoundTaperedPile,
        ],
        [
            "test_add_bearing_round_hollow_pile_with_closed_base.foi",
            dict(external_diameter=1, wall_thickness=0.01),
            BearingRoundHollowPileWithClosedBase,
        ],
        [
            "test_add_bearing_round_pile_with_lost_tip.foi",
            dict(base_diameter=1, pile_diameter=0.9),
            BearingRoundPileWithLostTip,
        ],
        [
            "test_add_bearing_round_pile_with_in_situ_formed_base.foi",
            dict(base_diameter=1, pile_diameter=0.9, base_height=1),
            BearingRoundPileWithInSituFormedBase,
        ],
        [
            "test_add_bearing_section.foi",
            dict(base_width=1, base_length=1),
            BearingSection,
        ],
        [
            "test_add_bearing_round_open_ended_hollow_pile.foi",
            dict(external_diameter=1, wall_thickness=0.01),
            BearingRoundOpenEndedHollowPile,
        ],
        [
            "test_add_bearing_h_shaped_pile.foi",
            dict(
                height_h_shape=1,
                width_h_shape=1,
                thickness_web=0.01,
                thickness_flange=0.01,
            ),
            BearingHShapedPile,
        ],
    ]
)
def create_bearing_pile_shape(request):
    return request.param


@pytest.fixture(
    params=[
        ["test_add_tension_round_pile.foi", dict(diameter=1), TensionRoundPile],
        [
            "test_add_tension_rectangular_pile.foi",
            dict(base_width=1, base_length=1),
            TensionRectangularPile,
        ],
        [
            "test_add_tension_round_pile_with_enlarged_base.foi",
            dict(base_diameter=1, pile_diameter=0.9, base_height=1),
            TensionRoundPileWithEnlargedBase,
        ],
        [
            "test_add_tension_rectangular_pile_with_enlarged_base.foi",
            dict(
                base_width_v=1,
                base_length_v=1,
                base_height=1,
                shaft_width=1,
                shaft_length=1,
            ),
            TensionRectangularPileWithEnlargedBase,
        ],
        [
            "test_add_tension_round_tapered_pile.foi",
            dict(diameter_at_pile_tip=1, increase_in_diameter=1),
            TensionRoundTaperedPile,
        ],
        [
            "test_add_tension_round_hollow_pile_with_closed_base.foi",
            dict(external_diameter=1, wall_thickness=0.01),
            TensionRoundHollowPileWithClosedBase,
        ],
        [
            "test_add_tension_round_pile_with_lost_tip.foi",
            dict(base_diameter=1, pile_diameter=0.9),
            TensionRoundPileWithLostTip,
        ],
        [
            "test_add_tension_round_pile_with_in_situ_formed_base.foi",
            dict(base_diameter=1, pile_diameter=0.9, base_height=1),
            TensionRoundPileWithInSituFormedBase,
        ],
        [
            "test_add_tension_section.foi",
            dict(circumference=1, cross_section=1),
            TensionSection,
        ],
        [
            "test_add_tension_round_open_ended_hollow_pile.foi",
            dict(external_diameter=1, wall_thickness=0.01),
            TensionRoundOpenEndedHollowPile,
        ],
        [
            "test_add_tension_h_shaped_pile.foi",
            dict(
                height_h_shape=1,
                width_h_shape=1,
                thickness_web=0.01,
                thickness_flange=0.01,
            ),
            TensionHShapedPile,
        ],
    ]
)
def create_tension_pile_shape(request):
    return request.param
