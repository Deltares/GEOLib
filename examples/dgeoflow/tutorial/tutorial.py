from pathlib import Path

from geolib.geometry import Point
from geolib.models.dgeoflow import DGeoFlowModel
from geolib.models.dgeoflow.internal import (
    CalculationTypeEnum,
    ErosionDirectionEnum,
    PersistablePoint,
    PipeTrajectory,
)
from geolib.soils import Soil

dm = DGeoFlowModel()
dm.set_calculation_type(calculation_type=CalculationTypeEnum.CRITICAL_HEAD)

# Add soil
soil = Soil()
soil.name = "Peat"
soil.code = "HV"
soil.storage_parameters.horizontal_permeability = 0.01
soil.storage_parameters.vertical_permeability = 0.01
soil_peat_id = dm.add_soil(soil)

# Add layers
layer_1 = [
    Point(x=-50, z=-10),
    Point(x=50, z=-10),
    Point(x=50, z=-20),
    Point(x=-50, z=-20),
]
layer_2 = [
    Point(x=-50, z=-5),
    Point(x=50, z=-5),
    Point(x=50, z=-10),
    Point(x=-50, z=-10),
]
layer_3 = [
    Point(x=-50, z=0),
    Point(x=-10, z=0),
    Point(x=30, z=0),
    Point(x=50, z=0),
    Point(x=50, z=-5),
    Point(x=-50, z=-5),
]
embankment = [
    Point(x=-10, z=0),
    Point(x=0, z=2),
    Point(x=10, z=2),
    Point(x=30, z=0),
]

layers_and_soils = [
    (layer_1, "Sand"),
    (layer_2, "H_Ro_z&k"),
    (layer_3, "HV"),
    (embankment, "H_Aa_ht_old"),
]

for points, soil in layers_and_soils:
    dm.add_layer(points, soil)

river_boundary_id = dm.add_boundary_condition(
    [Point(x=-50, z=0), Point(x=-10, z=0)], 17, "River"
)
dm.add_boundary_condition([Point(x=30, z=0), Point(x=50, z=0)], 0, "Polder")


# Set a pipe trajectory
dm.set_pipe_trajectory(
    pipe_trajectory=PipeTrajectory(
        Label="Pipe",
        D70=0.1,
        ErosionDirection=ErosionDirectionEnum.RIGHT_TO_LEFT,
        ElementSize=1,
        Points=[PersistablePoint(X=30, Z=0), PersistablePoint(X=-10, Z=0)],
    )
)

# Set the river boundary to be the critical boundary condition
dm.set_critical_head_boundary_condition(boundary_condition_id=river_boundary_id)

# Set the critical head search parameters
dm.set_critical_head_search_parameters(minimum_head_level=17, maximum_head_level=18)

dm.serialize(Path("tutorial.flox"))

dm.execute()
