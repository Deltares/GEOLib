.. tutorialdstability:

Tutorial D-Stability
====================
1. The model data should be set. This can be done by initialising the class  :class:`~geolib.models.dstability.dstability_model.DStabilityModel`.

.. code-block:: python

    dm = DStabilityModel()

2. Choose an analysis method, such as :class:`~geolib.models.dstability.DStabilityBishopAnalysisMethod` and set
it to the model.

.. code-block:: python

    bishop_analysis_method = DStabilityBishopAnalysisMethod(
        circle=DStabilityCircle(center=Point(x=20, z=3), radius=15)
    )
    dm.set_model(bishop_analysis_method)

For completeness, here follow examples for all possible models.


.. code-block:: python

    # add bishop brute force
    dm.set_model(
        DStabilityBishopBruteForceAnalysisMethod(
            search_grid=DStabilitySearchGrid(
                bottom_left=Point(x=15, z=2),
                number_of_points_in_x=10,
                number_of_points_in_z=10,
                space=0.5,
            ),
            bottom_tangent_line_z=-6.0,
            number_of_tangent_lines=5,
            space_tangent_lines=0.5,
        )
    )


    # add spencer
    dm.set_model(
        DStabilitySpencerAnalysisMethod(
            slipplane=[
                Point(x=7, z=2.0),
                Point(x=15, z=-3),
                Point(x=30, z=-4.5),
                Point(x=40, z=0.0),
            ]
        )
    )


    # add spencer genetic
    dm.set_model(
        DStabilitySpencerGeneticAnalysisMethod(
            slip_plane_a=[
                Point(x=10, z=2.0),
                Point(x=15, z=0),
                Point(x=30, z=-4),
                Point(x=35, z=0.0),
            ],
            slip_plane_b=[
                Point(x=5, z=2.0),
                Point(x=15, z=-3),
                Point(x=30, z=-6),
                Point(x=40, z=0.0),
            ],
        )
    )


    # uplift
    dm.set_model(
        DStabilityUpliftVanAnalysisMethod(
            first_circle=DStabilityCircle(center=Point(x=5, z=5), radius=9.5),
            second_circle_center=Point(x=40, z=2),
        )
    )


    # uplift particle swarm
    dm.set_model(
        DStabilityUpliftVanParticleSwarmAnalysisMethod(
            search_area_a=DStabilitySearchArea(
                height=5.0, top_left=Point(x=0.0, z=10.0), width=5.0
            ),
            search_area_b=DStabilitySearchArea(
                height=5.0, top_left=Point(x=35.0, z=5.0), width=5.0
            ),
            tangent_area_height=2.0,
            tangent_area_top_z=-4.5,
        )
    )


3. We can then create a :class:`~geolib.soils.Soil` and add it to the model. Refer to :ref:`soil_tut` for more information.

.. code-block:: python

    # add soil
    soil = Soil()
    soil.name = "Soil test"
    soil.code = "HV"
    soil.soil_weight_parameters.saturated_weight.mean = 10.2
    soil.soil_weight_parameters.unsaturated_weight.mean = 10.2
    soil.mohr_coulomb_parameters.cohesion.mean = 0.5
    soil.mohr_coulomb_parameters.friction_angle.mean = 15.0      
    soil_peat_id = dm.add_soil(soil)

4. Afterwards we create several layers and choose a soil for them.

.. code-block:: python

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
    layer_ids = []
    for layer, soil in layers_and_soils:
        layer_id = dm.add_layer(layer, soil)
        layer_ids.append(layer_id)

5. With the geometry defined, let's add the headlines. One of these can be set as the phreatic line.

.. code-block:: python

    # add phreatic line
    phreatic_line_id = dm.add_head_line(
        points=[
            Point(x=-50, z=1.0),
            Point(x=0, z=1),
            Point(x=30, z=-1),
            Point(x=50, z=-1),
        ],
        label="Phreatic Line",
        is_phreatic_line=True,
    )

    # add headline for deep sand
    sand_head_line_id = dm.add_head_line(
        points=[Point(x=-50, z=5.0), Point(x=50, z=5.0)],
        label="Hydraulic head in sandlayer",
    )

    dm.add_reference_line(
        points=[Point(x=-50, z=-3), Point(x=50, z=-3)],
        bottom_headline_id=phreatic_line_id,
        top_head_line_id=phreatic_line_id,
    )
    dm.add_reference_line(
        points=[Point(x=-50, z=-10), Point(x=50, z=-10)],
        bottom_headline_id=sand_head_line_id,
        top_head_line_id=sand_head_line_id,
    )

6. What's left to add is the creation of several types of loads.

.. code-block:: python

    #  add uniform load
    dm.add_load(
        UniformLoad(
            label="trafficload",
            start=6.5,
            end=9.0,
            magnitude=13,
            angle_of_distribution=45,
        )
    )

    # add line load
    dm.add_load(
        LineLoad(
            location=Point(x=2.0, z=2.0),
            angle=0.0,
            magnitude=10.0,
            angle_of_distribution=45.0,
        )
    )

    # create reinforcements NAIL
    dm.add_reinforcement(
        Nail(
            location=Point(x=20.0, z=1.0),
            direction=15.0,
            horizontal_spacing=1.0,
            length=3.0,
            grout_diameter=0.1,
            max_pull_force=10.0,
            plastic_moment=5.0,
            bending_stiffness=100.0,
        )
    )

    # create reinforcements GEOTEXTILE
    dm.add_reinforcement(
        Geotextile(
            start=Point(x=20.0, z=0.0),
            end=Point(x=30.0, z=0.0),
            effective_tensile_strength=10.0,
            reduction_area=0.5,
        )
    )

    # create reinforcements FORBIDDEN LINE
    dm.add_reinforcement(
        ForbiddenLine(start=Point(x=30.0, z=0.0), end=Point(x=30.0, z=-4.0))
    )

7. And we can set state points or statelines.

.. code-block:: python

    # state point
    dm.add_state_point(
        DStabilityStatePoint(
            layer_id=layer_ids[2],  # HV layer
            point=Point(x=0, z=-2.5),
            stress=DStabilityStress(pop=10.0),
        )
    )

    # state line
    dm.add_state_line(
        points=[Point(x=-50, z=-2), Point(x=50, z=-2)],
        state_points=[
            DStabilityStateLinePoint(
                above=DStabilityStress(pop=5), below=DStabilityStress(pop=10), x=20
            )
        ],
    )

To run the model first the model needs to be serialised. To do that define a 
output file name and call the function :meth:`~geolib.models.dstability.dstability_model.DStabilityModel.serialize`.

.. code-block:: python

    from pathlib import Path
    dm.serialize(Path("tutorial.stix")

Finally the execute function can be called to run the model in D-Stability.

.. code-block:: python

    dm.execute()
