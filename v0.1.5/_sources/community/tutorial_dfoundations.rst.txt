.. tutorialdfoundations:

Tutorial D-Foundations
======================
1. The model data should be set. This can be done by initialasing the class  :class:`~geolib.models.dfoundations.dfoundations_model.DFoundationsModel`.

.. code-block:: python

    df = gl.models.dfoundations.DFoundationsModel()


2. When using the python API for D-Foundations, it is very important to start the project with setting the calculation
options and the model. If this is not done, certain project data can be unintentionally overwritten.

In this tutorial model options are set for bearing piles. The calculation model is in this case
:class:`~geolib.models.dfoundations.dfoundations_model.BearingPilesModel`.

.. code-block:: python

    model_options = gl.models.dfoundations.dfoundations_model.BearingPilesModel(
        is_rigid=False, factor_xi3=9
    )
    calculation_options = gl.models.dfoundations.dfoundations_model.CalculationOptions(
        calculationtype=gl.models.dfoundations.dfoundations_model.CalculationType.VERIFICATION_DESIGN,
        cpt_test_level=-19.0,
    )
    df.set_model(model_options, calculation_options)




3. A CPT must be initialised using the class :class:`~geolib.models.dfoundations.profiles.CPT`.

.. code-block:: python

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
            {"z": -15, "qc": 5.0},
            {"z": -25, "qc": 5.0},
            {"z": -30, "qc": 35.0},
        ],
        timeorder_type=profiles.TimeOrderType.CPT_BEFORE_AND_AFTER_INSTALL,
    )

After inputing the CPT the rest of the inputs for the profiles should be initialised. 
To do that initialise the class :class:`~geolib.models.dfoundations.profiles.Excavation`.

.. code-block:: python

    excavation = profiles.Excavation(excavation_level=1.0)

The location of the CPT should also be defined.

.. code-block:: python

    location_cpt = profiles.Point(x=1.0, y=2.0)

Then the profile can be defined by initialising the class :class:`~geolib.models.dfoundations.profiles.Profile`.
The layers can be input as a list of dicts.

.. code-block:: python

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
        df.add_profile(profile)

4. The soil can be intialised with the :class:`~geolib.soils.Soil` and can be added to the model by using the function
:func:`~geolib.models.dfoundations.dfoundations_model.DFoundationsModel.add_soil`.

.. code-block:: python

    soil = Soil()
    soil.name = "test"
    soil.mohr_coulomb_parameters.friction_angle = 20
    soil.undrained_parameters.undrained_shear_strength = 20

    df.add_soil(soil)

5. The type(s) of pile and its location(s) needs to be defined. The possible combinations for these options can be found in :class:`~geolib.models.dfoundations.piles`.
In this case the class :class:`~geolib.models.dfoundations.piles.BearingRectangularPile` is initialised. In the following code block the location
of the pile is first initialised by calling the class :class:`~geolib.models.dfoundations.piles.BearingPileLocation`.

.. code-block:: python

    # Add Bearing Pile
    location = piles.BearingPileLocation(
        point=Point(x=1.0, y=1.0),
        pile_head_level=1,
        surcharge=1,
        limit_state_str=1,
        limit_state_service=1,
    )

After that two different dictionaries are initialised ``geometry_pile`` represents the geometry input and ``parent_pile`` all 
the inputs that are related to the factors concerning the pile.

.. code-block:: python

    geometry_pile = dict(base_width=1, base_length=1)
    parent_pile = dict(
        pile_name="test",
        pile_type=piles.BasePileType.USER_DEFINED_VIBRATING,
        pile_class_factor_shaft_sand_gravel=1,  # alpha_s
        preset_pile_class_factor_shaft_clay_loam_peat=piles.BasePileTypeForClayLoamPeat.STANDARD,
        pile_class_factor_shaft_clay_loam_peat=1,  # alpha_s
        pile_class_factor_tip=1,  # alpha_p
        load_settlement_curve=piles.LoadSettlementCurve.ONE,
        user_defined_pile_type_as_prefab=False,
        use_manual_reduction_for_qc=False,
        elasticity_modulus=1e7,
        characteristic_adhesion=10,
        overrule_pile_tip_shape_factor=False,
        overrule_pile_tip_cross_section_factors=False,
    )

In that way the dictionaries can be used to initialise the class :class:`~geolib.models.dfoundations.piles.BearingRectangularPile`.

.. code-block:: python

    pile = piles.BearingRectangularPile(**parent_pile, **geometry_pile)

The pile can be finally added to the model using the function  :func:`~geolib.models.dfoundations.dfoundations_model.DFoundationsModel.add_pile_if_unique`.

.. code-block:: python

    df.add_pile_if_unique(pile, location)

6. To run the model first the model needs to be serialised. To do that define a 
output file name and call the function :meth:`geolib.models.dfoundations.dfoundations_model.DFoundationsModel.serialize`.

.. code-block::python

    from pathlib import Path
    input_test_file = Path("Tutorial.foi")
    df.serialize(input_test_file)

7. Finally the ``execute`` function can be called to run the model in D-Foundations

.. code-block::python

    df.filename = input_test_file
    df.execute()
