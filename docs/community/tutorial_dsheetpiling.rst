.. tutorialsheetpiling:

Tutorial D-Sheet Piling
=======================


1. The model data should be set. This can be done by initialasing the class  :class:`~geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel`.

.. code-block:: python

    model = DSheetPilingModel()

2. The type of model should be then defined. There are 4 different types of models that can be implemented in D-Sheetpiling.
The :class:`~geolib.models.dsheetpiling.dsheetpiling_model.SheetModelType`, :class:`~geolib.models.dsheetpiling.dsheetpiling_model.WoodenSheetPileModelType`,
:class:`~geolib.models.dsheetpiling.dsheetpiling_model.SinglePileModelType` and :class:`~geolib.models.dsheetpiling.dsheetpiling_model.DiaphragmModelType`.

Initialise as follows:

.. code-block:: python

    modeltype = SheetModelType(
        check_vertical_balance=False, trildens_calculation=False
    )
    model.set_model(modeltype)

3. After defining we will define the (required) sheet properties.

.. code-block:: python

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

These properties should then be passed into the initialisation of class :class:`~geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel`.
For example

.. code-block:: python

    sheet_element_1 = Sheet(name="AZ 13", sheet_pile_properties=sheet_pile_properties_1)

To define multiple sections of a sheet pile, another sheet element is created in the same way. Notice that the only value that needs to change is the section_bottom_level,
as two sections cannot have the same bottom level.

.. code-block:: python

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
        sheet_element_2 = Sheet(name="AZ 13", sheet_pile_properties=sheet_pile_properties_2)

These two sheet element can finally be added to the construction with the following command.
The elements can be added in a form of a list when the construction is set.

.. code-block:: python

    level_top = 0
    model.set_construction(
        top_level=level_top, elements=[sheet_element_1, sheet_element_2]
    )

4. The stages should be defined after that. To define a stage call the function :meth:`geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel.add_stage`.
The order of stages is defined as the order in which they were added. An example is added below. The user is also advised to store the output of the 
function (the ``stage_id``) in a variable. This ``stage_id`` variable can be used later to define in which stage the surfaces, loads and supports, will be added.

.. code-block:: python

    stage_id = model.add_stage(
        name="New Stage",
        passive_side=PassiveSide.DSHEETPILING_DETERMINED,
        method_left=LateralEarthPressureMethodStage.KA_KO_KP,
        method_right=LateralEarthPressureMethodStage.KA_KO_KP,
        pile_top_displacement=0.01,
    )

5. Then the soils should be defined. In this case three types of soils materials will be defined. 
To define a soil material the class :class:`~geolib.soils.Soil` should be initialised. For more information see the
other :ref:`soil_tut`.

.. code-block:: python

    soil_clay = Soil(name="Clay")

After that all the different parameters can be defined.

.. code-block:: python

    # Set clay material
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
    # These values refer to the settlement by vibration calculation
    soil_clay.soil_classification_parameters.relative_density = 72
    soil_clay.storage_parameters.horizontal_permeability = 8e-11
    soil_clay.soil_type_settlement_by_vibrations = SoilTypeSettlementByVibration.CLAY

The soil can be added to the model by the using the following function.

.. code-block:: python

    model.add_soil(soil_clay)

In the same way all the other materials can be defined and added to the model.

.. code-block:: python

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
    soil_peat.soil_type_settlement_by_vibrations = SoilTypeSettlementByVibration.PEAT
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
    soil_sand.soil_type_settlement_by_vibrations = SoilTypeSettlementByVibration.SAND
    # add soils in model
    for soil in (soil_peat, soil_sand):
        model.add_soil(soil)

6. After defining all the soil materials the profiles can be defined for the D-SheetPing calculation.
A soil profile in GEOLIB is essentially a collection of soil layers. A soil layer can be initialised 
from the class :class:`~geolib.models.dsheetpiling.profiles.SoilLayer` and requires as 
inputs the top position of the layer and the name of the soil material. Note that the soil materials,
should have already been added to the model, these are referred to by name.

.. code-block:: python

    soil_layer_1 = SoilLayer(top_of_layer=0, soil=soil_clay.name)
    soil_layer_2 = SoilLayer(top_of_layer=-4, soil=soil_peat.name)
    soil_layer_3 = SoilLayer(top_of_layer=-6, soil=soil_clay.name)
    soil_layer_4 = SoilLayer(top_of_layer=-13, soil=soil_sand.name)

To define the soil profile initialise class :class:`~geolib.models.dsheetpiling.profiles.SoilProfile`
with the name of a profile and a list of the layers initialised in a top to bottom order.

.. code-block:: python

    profile = SoilProfile(
        name="New Profile",
        layers=[
            soil_layer_1,
            soil_layer_2,
            soil_layer_3,
            soil_layer_4,
        ],
    )
    model.add_profile(profile=profile, side=Side.BOTH, stage_id=stage_id)

7. To add surfaces for the right and left side the class :class:`~geolib.models.dsheetpiling.surface.Surface` 
is used. Two surface are initialised in this case and are added in the first stage on the left and right side.

.. code-block:: python

    ground_level_surface = Surface(name="GL", points=[Point(x=0, z=0)])
    ground_level_minus_7_meter_surface = Surface(
        name="GL-7", points=[Point(x=0, z=-7)]
    )
    model.add_surface(
        surface=ground_level_surface, side=Side.RIGHT, stage_id=stage_id
    )
    model.add_surface(
        surface=ground_level_minus_7_meter_surface, side=Side.LEFT, stage_id=stage_id
    )

8. The water level are defined in the same way with initialiasing the class :class:`~geolib.models.dsheetpiling.water_level.WaterLevel`
and then adding it to the model using the function :meth:`~geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel.add_head_line`.

.. code-block:: python

    initial_water_level = WaterLevel(name="WL=GL-2", level=-2)
    model.add_head_line(
        water_level=intial_water_level, side=Side.BOTH, stage_id=stage_id
    )

9. The calculation options also need to be defined. In this section several different available calculation options will be discussed.

- Standard calculation initialised with class :class:`~geolib.models.dsheetpiling.calculation_options.StandardCalculationOptions`.

.. code-block:: python

    calc_options = StandardCalculationOptions()
    model.set_calculation_options(calculation_options=calc_options)

- Verify calculation initialised with class :class:`~geolib.models.dsheetpiling.calculation_options.VerifyCalculationOptions`.

.. code-block:: python

    calc_options = VerifyCalculationOptions(
        input_calculation_type=CalculationType.VERIFY_SHEETPILING,
        verify_type=VerifyType.EC7NL,
        ec7_nl_method=PartialFactorCalculationType.METHODB,
    )
    model.set_calculation_options(calculation_options=calc_options)

When a Verify ``METHOD B`` is selected the class :class:`~geolib.models.dsheetpiling.calculation_options.CalculationOptionsPerStage`
also needs to be initialised and added to the model.

.. code-block:: python

    calc_options_per_stage = CalculationOptionsPerStage(
        anchor_factor=1.5, partial_factor_set=PartialFactorSetEC7NADNL.RC2
    )
    model.add_calculation_options_per_stage(
        calculation_options_per_stage=calc_options_per_stage, stage_id=stage_id
    )

Overal stability calculation are initialised with class :class:`~geolib.models.dsheetpiling.calculation_options.OverallStabilityCalculationOptions`.
Note that the input of the stage refers to the stage numbering as it is defined in D-SheetPing where the numbering of the stage ids begins from 1.

.. code-block:: python

    calc_options = OverallStabilityCalculationOptions(
        cur_stability_stage=1,
        overall_stability_type=DesignType.CUR,
        stability_cur_partial_factor_set=PartialFactorSetCUR.CLASSII,
    )
    model.set_calculation_options(calculation_options=calc_options)   

Kranz anchor strength calculation is initialised with class :class:`~geolib.models.dsheetpiling.calculation_options.KranzAnchorStrengthCalculationOptions`.
Note that the input of the stage refers to the stage numbering as it is defined in D-SheetPing where the numbering of the stage ids begins from 1.

.. code-block:: python

    calc_options =KranzAnchorStrengthCalculationOptions(cur_anchor_force_stage=1)
    model.set_calculation_options(calculation_options=calc_options)   

Design calculation is initialised with class :class:`~geolib.models.dsheetpiling.calculation_options.DesignSheetpilingLengthCalculationOptions`.
Note that the input of the stage refers to the stage numbering as it is defined in D-SheetPing where the numbering of the stage ids begins from 1.

.. code-block:: python  

    calc_options = DesignSheetpilingLengthCalculationOptions(
        design_stage=1,
        design_pile_length_from=10,
        design_pile_length_to=1,
        design_pile_length_decrement=0.1,
        design_type=DesignType.EC7NL,
        design_partial_factor_set_ec7_nad_nl=PartialFactorSetEC7NADNL.RC1,
        design_ec7_nl_method=PartialFactorCalculationType.METHODA,
    )
    model.set_calculation_options(calculation_options=calc_options)

10. After defining these basic inputs the calculation can be run, but won't be so useful. Several loads, supports and anchors can be defined.
The following section list the way they can be initialised. The stage_id input here refers to the Python input which starts from 0.

.. code-block:: python

    # add anchor
    anchor = Anchor(
        name="Grout anchor",
        level=-2,
        side=Side.RIGHT,
        e_modulus=100000,
        C=10,
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
    model.add_anchor_or_strut(support=floor, stage_id=stage_id)

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

11. To run the model first the model needs to be serialised. To do that define a 
output file name and call the function :meth:`geolib.models.dsheetpiling.dsheetpiling_model.DSheetPilingModel.serialize`.

.. code-block:: python

    from pathlib import Path
    input_test_file = Path("Tutorial.shi")
    model.serialize(input_test_file)

12. Finally the execute function can be called to run the model in D-SheetPiling

.. code-block:: python

    model.filename = input_test_file
    model.execute()
