import geolib as gl
import os
from pathlib import Path
from geolib.models.dfoundations import profiles, piles

from geolib.geometry import Point
from geolib.soils import Soil

test_folder = r'D:\software_development\geolib\tests\test_data\dfoundations\benchmarks'
test_file_name = r"bm1-1b.foi"
test_dump_file = r"bm1-1b.fod"

output_file = r"D:\software_development\geolib\tests\test_output\dfoundations\acceptation\test.foi"
exe_loc = r"D:\installed_software\D-Serie Consoles\consoles"


df = gl.models.dfoundations.DFoundationsModel()

df.meta.console_folder = Path(exe_loc)

df.parse(Path(os.path.join(test_folder,test_file_name)))
df.parse(Path(os.path.join(test_folder,test_dump_file)))
cpt = profiles.CPT(
            cptname="DELFT1",
            groundlevel=0.5,
            measured_data=[
                {"z": 0.0, "qc": 0.1},
                {"z": -0.10, "qc": 0.5},
                {"z": -0.20, "qc": 2.0},
                {"z": -0.30, "qc": 3.0},
                {"z": -0.40, "qc": 5.0},
            ],
            timeorder_type=profiles.TimeOrderType.CPT_BEFORE_AND_AFTER_INSTALL
        )

excavation = profiles.Excavation(excavation_level=0.1)
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
            "top_level": -0.1,
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

soil = Soil()
soil.name="test"
soil.friction_angle = 20
soil.soil_parameters.undrained_parameters.undrained_shear_strength = 20

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
    execution_factor_sand_gravel=1,
    pile_type_for_execution_factor_clay_loam_peat=piles.BasePileTypeForClayLoamPeat.STANDARD,
    execution_factor_clay_loam_peat=1,
    pile_class_factor=1,
    load_settlement_curve=piles.LoadSettlementCurve.ONE,
    user_defined_pile_type_as_prefab=False,
    use_manual_reduction_for_qc=False,
    elasticity_modulus=1e7,
    characteristic_adhesion=10,
    overrule_pile_tip_shape_factor=False,
    overrule_pile_tip_cross_section_factors=False,
)
pile = piles.BearingRectangularPile(**parent_pile, **geometry_pile)

model_options = gl.models.dfoundations.dfoundations_model.BearingPilesModel(is_rigid=False, factor_xi3=9)
calculation_options = gl.models.dfoundations.dfoundations_model.CalculationOptions(
    calculationtype=gl.models.dfoundations.dfoundations_model.CalculationType.PILETIP_LEVELS_AND_NET_BEARING_CAPACITY,
    cpt_test_level=-50.0
)
df.set_model(model_options, calculation_options)

df.add_pile_if_unique(pile, location)

df.serialize(Path(output_file))
df.execute()
print('test')
