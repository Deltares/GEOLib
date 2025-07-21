from pathlib import Path

import pytest

import geolib as gl
from geolib.geometry import Point
from geolib.models.dfoundations import piles, profiles
from geolib.models.dfoundations.internal import DFoundationsDumpStructure
from geolib.soils import Soil
from tests.utils import TestUtils, only_teamcity


@pytest.mark.usefixtures("cleandir_dfo")
@pytest.mark.acceptance
@only_teamcity
def test_run_model_from_scratch_expanded():
    output_test_folder = Path(TestUtils.get_output_test_data_dir("dfoundations"))
    output_test_file = output_test_folder / "acceptance_from_scratch_extended.foi"

    df = gl.models.dfoundations.DFoundationsModel()

    # Model options are required to be set before setting additional parameters
    model_options = gl.models.dfoundations.dfoundations_model.BearingPilesModel(
        is_rigid=False,
        factor_xi3=9,
        max_allowed_rel_rotation_lim_state_str=100,
        max_allowed_rel_rotation_lim_state_serv=300,
    )
    calculation_options = gl.models.dfoundations.dfoundations_model.CalculationOptions(
        calculationtype=gl.models.dfoundations.dfoundations_model.CalculationType.VERIFICATION_DESIGN,
        cpt_test_level=-19.0,
    )

    df.set_model(model_options, calculation_options)

    cpt = profiles.CPT(
        cptname="DELFT1",
        groundlevel=0.5,
        measured_data=[
            {"z": 0.0, "qc": 0.1},
            {"z": -0.10, "qc": 0.5},
            {"z": -0.20, "qc": 2.0},
            {"z": -0.30, "qc": 3.0},
            {"z": -0.40, "qc": 5.0},
            {"z": -10, "qc": 1.0},
            {"z": -12.681, "qc": 3.307},
            {"z": -15, "qc": 5.0},
            {"z": -25, "qc": 5.0},
            {"z": -30, "qc": 35.0},
        ],
        timeorder_type=profiles.TimeOrderType.CPT_BEFORE_AND_AFTER_INSTALL,
    )

    excavation = profiles.Excavation(excavation_level=1.0)
    location_cpt = profiles.Point(x=1.0, y=2.0)
    profile = profiles.Profile(
        name="DELFT1",
        location=location_cpt,
        phreatic_level=-0.5,
        pile_tip_level=-0.5,
        cpt=cpt,
        excavation=excavation,
        layers=[
            {
                "material": "Clay, clean, stiff",
                "top_level": 0.0,
                "excess_pore_pressure_top": 0.0,
                "excess_pore_pressure_bottom": 0.0,
                "ocr_value": 1.0,
                "reduction_core_resistance": 0,
            },
            {
                "material": "Clay, clean, soft",
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

    soil = Soil()
    soil.name = "test"
    soil.mohr_coulomb_parameters.friction_angle = 20
    soil.undrained_parameters.undrained_shear_strength = 20

    df.add_soil(soil)

    df.add_profile(profile)

    # Add Bearing Pile
    location = piles.BearingPileLocation(
        point=Point(x=1.0, y=1.0),
        pile_head_level=1,
        surcharge=1,
        limit_state_str=1,
        limit_state_service=1,
    )
    geometry_pile = dict(base_width=1, base_length=1)
    parent_pile = dict(
        pile_name="test",
        pile_type=piles.BasePileType.USER_DEFINED_VIBRATING,
        pile_class_factor_shaft_sand_gravel=1,
        preset_pile_class_factor_shaft_clay_silt_peat=piles.BasePileTypeForClaySiltPeat.STANDARD,
        pile_class_factor_shaft_clay_silt_peat=1,
        pile_class_factor_tip=1,
        load_settlement_curve=piles.LoadSettlementCurve.ONE,
        user_defined_pile_type_as_prefab=False,
        use_manual_reduction_for_qc=False,
        elasticity_modulus=1e7,
        characteristic_adhesion=10,
        overrule_pile_tip_shape_factor=False,
        overrule_pile_tip_cross_section_factors=False,
    )
    pile = piles.BearingRectangularPile(**parent_pile, **geometry_pile)

    df.add_pile_if_unique(pile, location)

    # 2. Verify initial expectations.
    df.serialize(output_test_file)
    assert output_test_file.is_file()

    # 3. Run test.
    df.filename = output_test_file
    df.execute()

    # 4. Verify model has run and output has been parsed
    assert isinstance(df.datastructure, DFoundationsDumpStructure)
