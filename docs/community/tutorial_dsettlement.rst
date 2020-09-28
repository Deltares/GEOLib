.. tutorialdsettlement:

Tutorial D-Settlement
=====================

1. The model data should be set. This can be done by initialasing the class  :class:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel`.

.. code-block:: python

    dm = DSettlementModel()

2. Bases on the model the function :func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.set_model`. Here the calculation model options can be set.

.. code-block:: python

    dm.set_model(
        constitutive_model=SoilModel.ISOTACHE,
        consolidation_model=ConsolidationModel.DARCY,
        is_two_dimensional=True,
        strain_type=StrainType.LINEAR,
        is_vertical_drain=True,
        is_fit_for_settlement_plate=False,
        is_probabilistic=False,
        is_horizontal_displacements=False,
        is_secondary_swelling=False,
        is_waspan=True,
    )

3. Then the geometry of the model should be defined by setting up the points which will make up the full geometry.

.. code-block:: python

    # points for the geometry 
    p1 = Point(x=-50, z=0.0)
    p2 = Point(x=-10, z=0.0)
    p3 = Point(x=0, z=2)
    p4 = Point(x=10, z=2)
    p5 = Point(x=30, z=0.0)
    p6 = Point(x=50, z=0.0)
    p7 = Point(x=-50, z=-5)
    p8 = Point(x=50, z=-5)
    p9 = Point(x=-50, z=-10)
    p10 = Point(x=50, z=-10)
    p11 = Point(x=-50, z=-20)
    p12 = Point(x=50, z=-20)
    p15 = Point(x=-50, z=-30)
    p16 = Point(x=-20, z=-30)
    p17 = Point(x=-10, z=-30)
    p18 = Point(x=0, z=-30)
    p19 = Point(x=10, z=-30)
    p20 = Point(x=20, z=-30)
    p21 = Point(x=25, z=-30)
    p22 = Point(x=30, z=-30)
    p23 = Point(x=35, z=-30)
    p24 = Point(x=40, z=-30)
    p25 = Point(x=45, z=-30)
    p26 = Point(x=50, z=-30)

After defining the first points the boundaries of the geometry can be defined. This is done by calling the function 
:func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.add_boundary`. A boundary is represented as a list of points.

.. code-block:: python

    b1 = dm.add_boundary([p11, p12])
    b2 = dm.add_boundary([p9, p10])
    b3 = dm.add_boundary([p7, p8])
    b4 = dm.add_boundary([p1, p2, p5, p6])
    b5 = dm.add_boundary([p1, p2, p3, p4, p5, p6])
    b6 = dm.add_boundary(
        [p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26]
    )

Then define the calculation verticals from the function :func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.set_verticals`.

.. code-block:: python

    dm.set_verticals([p21])

Define the points for the headline and set these points as input in the function :func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.add_head_line`.

.. code-block:: python

    # headline points
    p13 = Point(x=-50, z=-2)
    p14 = Point(x=50, z=-2)

    pl_id = dm.add_head_line([p13, p14], is_phreatic=True)

4. After the basic geometry is inputted the soils can be defined. An example is appended below.

.. code-block:: python

    soil = Soil(name="Sand")
    soil.soil_weight_parameters.saturated_weight.mean = 17
    soil.soil_weight_parameters.unsaturated_weight.mean = 15
    soil.soil_weight_parameters.saturated_weight.standard_deviation = 0.7
    soil.soil_weight_parameters.unsaturated_weight.standard_deviation = 0.8
    soil.storage_parameters.vertical_consolidation_coefficient.mean = 1.00e-12
    soil.storage_parameters.vertical_consolidation_coefficient.standard_deviation = (
        5.00e-13
    )
    soil.soil_state.pop_layer.mean = 5
    soil.isotache_parameters.precon_isotache_type = StateType.POP
    soil.isotache_parameters.reloading_swelling_constant_a = StochasticParameter(
        mean=1.000e-02, standard_deviation=2.500e-03, correlation_coefficient=0.01
    )
    soil.isotache_parameters.primary_compression_constant_b = StochasticParameter(
        mean=1.000e-01, standard_deviation=2.500e-03
    )
    soil.isotache_parameters.secondary_compression_constant_c = StochasticParameter(
        mean=5.000e-03, standard_deviation=1.250e-03, correlation_coefficient=0.01
    )
    s1 = dm.add_soil(soil)

After the soils have been added, layers can be defined with the function :func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.add_layer`. Note that we refer to the soils by name.

.. code-block:: python

    l1 = dm.add_layer(
        material_name="Sand",
        head_line_top=pl_id,
        head_line_bottom=pl_id,
        boundary_top=b1,
        boundary_bottom=b2,
    )
    l2 = dm.add_layer(
        material_name="Sand",
        head_line_top=pl_id,
        head_line_bottom=pl_id,
        boundary_top=b2,
        boundary_bottom=b3,
    )
    l3 = dm.add_layer(
        material_name="Sand",
        head_line_top=pl_id,
        head_line_bottom=pl_id,
        boundary_top=b3,
        boundary_bottom=b4,
    )
    l4 = dm.add_layer(
        material_name="Sand",
        head_line_top=pl_id,
        head_line_bottom=pl_id,
        boundary_top=b4,
        boundary_bottom=b5,
    )
    l5 = dm.add_layer(
        material_name="Sand",
        head_line_top=pl_id,
        head_line_bottom=pl_id,
        boundary_top=b5,
        boundary_bottom=b6,
    )

5. After the complete geometry is defined other inputs can be set. For example the vertical drains.
Initialise class :class:`~geolib.models.dsettlement.dsettlement_model.VerticalDrain`. And add it to the model
using :func:`~geolib.models.dsettlement.dsettlement_model.DSettlementModel.set_vertical_drain`

.. code-block:: python

    from datetime import timedelta
    test_drain = VerticalDrain(
        drain_type=DrainType.COLUMN,
        range_from=0.1,
        range_to=1.5,
        bottom_position=-10,
        center_to_center=4,
        diameter=0.1,
        grid=DrainGridType.RECTANGULAR,
        schedule=ScheduleValuesSimpleInput(
            start_of_drainage=timedelta(days=0.1),
            phreatic_level_in_drain=2,
            begin_time=1,
            end_time=100,
            underpressure=55,
            tube_pressure_during_dewatering=10,
            water_head_during_dewatering=12,
        ),
    )
    # set vertical drains
    dm.set_vertical_drain(test_drain)

6. For a D-Settlement calculation to be performed at least one  load should be defined.
In this case a non uniform load is added to the model.

.. code-block:: python

    from datetime import timedelta
    # set up the point list
    point3 = Point(label="1", x=-50, y=0, z=0)
    point4 = Point(label="2", x=-50, y=0, z=2)
    point5 = Point(label="3", x=-10, y=0, z=2)
    point6 = Point(label="4", x=-10, y=0, z=0)
    pointlist = [point3, point4, point5, point6]
    # Add first uniform load
    dm.add_non_uniform_load(
        name="My First Load",
        points=pointlist,
        time_start=timedelta(days=0),
        time_end=timedelta(days=100),
        gamma_dry=20.02,
        gamma_wet=21.02,
    )

7. To run the model first the model needs to be serialised. To do that define a 
output file name and call the function :meth:`geolib.models.dsettlement.dsettlement_model.DSettlementModel.serialize`.

.. code-block:: python

    from pathlib import Path
    input_test_file = Path("Tutorial.sli")
    dm.serialize(input_test_file)

8. Finally the execute function can be called to run the model in D-Settlement console.

.. code-block:: python

    dm.filename = input_test_file
    dm.execute()

