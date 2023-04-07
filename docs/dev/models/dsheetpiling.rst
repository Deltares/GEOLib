.. _dsheetpiling:

D-Sheetpiling
========================

D-Sheetpiling model
-------------------

.. automodule:: geolib.models.dsheetpiling.dsheetpiling_model


.. automodule:: geolib.models.dsheetpiling.settings


.. automodule:: geolib.models.dsheetpiling.calculation_options


Constructions
-------------

.. automodule:: geolib.models.dsheetpiling.constructions


Loads
-------------

.. automodule:: geolib.models.dsheetpiling.loads


Supports
-------------

.. automodule:: geolib.models.dsheetpiling.supports


Geometry
--------

.. automodule:: geolib.models.dsheetpiling.profiles


.. automodule:: geolib.models.dsheetpiling.surface


.. automodule:: geolib.models.dsheetpiling.water_level


Output
------

The output structure of D-Sheet Piling is complex and dependent on the chosen calculation options.
Since we can't create helper functions that will fit every users need, we show here how you could
do it yourself, for finding the class :class:`geolib.models.dsheetpiling.internal.MomentsForcesDisplacements`:

The location of the `[MOMENTS FORCES DISPLACEMENTS]` varies per **calculation type**.
Note that the calculation type is a property of the internal D-SheetPiling output structure
(:attr:`~geolib.models.dsheetpiling.internal.DSheetPilingOutputStructure.calculation_type`).
In each step it is assumed you'll provide the stage_id, which is just a list index.

    - For Standard, Kranz and Reliability Analysis, the MomentsForcesDisplacements can be accessed in the following way:

    .. code-block:: python

        datastructure.output.construction_stage[stage_id].moments_forces_displacements


    - For Verify Sheet Piling according to CUR or EC7-NL the following instances can be used to access the data. In this case the five instances represent the 5 different CUR verification steps:

    .. code-block:: python

        datastructure.output.verify_step_6____5_serviceability_limit_state.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.verify_step_6____5_multiplied_by_factor.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.verify_step_6____1_low_modulus_of_subgrade_reaction_and_high_passive_water_level.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.verify_step_6____2_high_modulus_of_subgrade_reaction_and_high_passive_water_level.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.verify_step_6____3_low_modulus_of_subgrade_reaction_and_low_passive_water_level.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.verify_step_6____4_high_modulus_of_subgrade_reaction_and_low_passive_water_level.construction_stage[stage_id].moments_forces_displacements


    - Similarly for Verify Sheet Piling according to EC7-BE:

    .. code-block:: python

        datastructure.output.verify_deformation_serviceability_limit_state.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_belgium_set_1.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_belgium_set_2.construction_stage[stage_id].moments_forces_displacements


    - Similarly for Verify Sheet Piling according to EC7-General:

    .. code-block:: python

        datastructure.output.verify_deformation_serviceability_limit_state.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_1_set_1.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_1_set_2.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_2.construction_stage[stage_id].moments_forces_displacements
        datastructure.output.eurocode_3.construction_stage[stage_id].moments_forces_displacements



Each of the in between datastructures is documented below. It's advised to use these structures instead of just calling .dict(), as your editor
can help with autocompletion and validation.

.. autoclass:: geolib.models.dsheetpiling.internal.DSheetPilingOutputStructure
.. autoclass:: geolib.models.dsheetpiling.internal.OutputConstructionStage
.. autoclass:: geolib.models.dsheetpiling.internal.CurAnchorForceResults
.. autoclass:: geolib.models.dsheetpiling.internal.DesignSheetpileLength
.. autoclass:: geolib.models.dsheetpiling.internal.PointsOnSheetpile
.. autoclass:: geolib.models.dsheetpiling.internal.BaseVerificationStructureProperties
.. autoclass:: geolib.models.dsheetpiling.internal.Resume
.. autoclass:: geolib.models.dsheetpiling.internal.DesignLengthInfo
.. autoclass:: geolib.models.dsheetpiling.internal.DesignLengthCalculation
.. autoclass:: geolib.models.dsheetpiling.internal.SideOutput
.. autoclass:: geolib.models.dsheetpiling.internal.BreukData
.. autoclass:: geolib.models.dsheetpiling.internal.AnchorData
.. autoclass:: geolib.models.dsheetpiling.internal.DesignLengthCalculation
.. autoclass:: geolib.models.dsheetpiling.internal.DesignLengthInfo
.. autoclass:: geolib.models.dsheetpiling.internal.MomentsForcesDisplacements
.. autoclass:: geolib.models.dsheetpiling.internal.Pressures


