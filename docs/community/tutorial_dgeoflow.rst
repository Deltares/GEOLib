.. tutorialdgeoflow:

Tutorial D-Geo Flow
====================
1. The model data should be set. This can be done by initializing the class  :class:`~geolib.models.dgeoflow.dgeoflow_model.DGeoFlowModel`.

.. code-block:: python

    from geolib.models.dgeoflow import DGeoFlowModel

    dm = DGeoFlowModel()

2. Choose a calculation, from the :class:`~geolib.models.dgeoflow.CalculationTypeEnum` and set
it to the model.

.. code-block:: python

    from geolib.models.dgeoflow.internal import CalculationTypeEnum
    
    dm.set_calculation_type(calculation_type=CalculationTypeEnum.CRITICAL_HEAD)

3. We can then create a :class:`~geolib.soils.Soil` and add it to the model. Refer to :ref:`soil_tut` for more information.

.. code-block:: python

    from geolib.soils import Soil

    # add soil
    soil = Soil()
    soil.name = "Peat"
    soil.code = "HV"
    soil.storage_parameters.horizontal_permeability = 0.01
    soil.storage_parameters.vertical_permeability = 0.01   
    soil_peat_id = dm.add_soil(soil)

4. Afterwards we create several layers and choose a soil for them.

.. code-block:: python

    from geolib.geometry import Point

    # add layers
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
    
    [dm.add_layer(points, soil) for points, soil in layers_and_soils]

5. With the geometry defined, let's add the boundary conditions.

.. code-block:: python

    river_boundary_id = dm.add_boundary_condition(
        [Point(x=-50, z=0), Point(x=-10, z=0)], 17, "River"
    )
    dm.add_boundary_condition([Point(x=30, z=0), Point(x=50, z=0)], 0, "Polder")

6. You can now set the calculation settings.

.. code-block:: python
    
    from geolib.models.dgeoflow.internal import PipeTrajectory, ErosionDirectionEnum, PersistablePoint

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
    dm.set_critical_head_search_parameters(
        minimum_head_level=17, maximum_head_level=18
    )


To run the model first the model needs to be serialized. To do that define a 
output file name and call the function :meth:`~geolib.models.dgeoflow.dgeoflow_model.DGeoFlowModel.serialize`.

.. code-block:: python

    from pathlib import Path
    
    dm.serialize(Path("tutorial.flox")

Finally the execute function can be called to run the model in D-Geo Flow.

.. code-block:: python

    dm.execute()
