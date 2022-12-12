.. _soil_tut:

Tutorial Soils
==============

Soils in GEOlib are added in a generic way, this means that there is one basis soil
class which is meant to be the input for all the separate D-Serie products.
For this reason it is possible that the parameter locations are not as you
are used to in the D-Serie products.

Parameters in the Soil class are clustered based on physical meaning. I.e. cohesion
and friction angle are clustered in the MohrCoulombParameters class; ``reloading_swelling_constant_a``
is stored in the ``IsotacheParameters`` class and permeability parameters are stored in the ``StorageParameters``
class.

Since parameters are clustered in different classes as the Soil class, it is required to
fill in parameters in these respective classes. Below an example is given on how to
to initialise a soil with a friction angle and cohesion.

.. code-block:: python

    from geolib.soils import Soil, MohrCoulombParameters

    mohr_coulomb_parameters = MohrCoulombParameters(cohesion=5, friction_angle=25)
    soil = Soil(mohr_coulomb_parameters=mohr_coulomb_parameters)

Another method is to first initialise the soil and then change the values, for example:

.. code-block:: python

    from geolib.soils import Soil

    soil = Soil()
    soil.mohr_coulomb_parameters.cohesion = 5
    soil.mohr_coulomb_parameters.friction_angle = 25

Lastly, the parameters can be passed as a dictionary, for example:

.. code-block:: python

    from geolib.soils import Soil

    kwargs = {"cohesion": 5,
              "friction_angle": 25}
    soil = Soil(mohr_coulomb_parameters=kwargs)

When initialising the Soil class all values given should be parameters of the class itself.
Otherwise an error is thrown, for example:

.. code-block:: python

    from geolib.soils import Soil
    soil = Soil(name="Peat", cohesion=0.5)

will result in::

    pydantic.error_wrappers.ValidationError: 1 validation error for Soil
    cohesion
        extra fields not permitted (type=value_error.extra)

That is because the cohesion value should be set through the mohr_coulomb_parameters parameter.
Note that when the Soil class is intialised without the user defining the parameters, it will be populated with default values.

Many parameters can be initialised as either a stochastic variable or a float. When the parameter
is filled in as a floating value, the value is automatically translated to a stochastic variable with
a mean of the input float and a standard deviation of 0. This step is required to stay
consistent in sending parameters to the corresponding models

Below three examples are given on how to input a stochastic variable in the soil.

.. code-block:: python

    from geolib.soils import Soil, MohrCoulombParameters, StochasticParameter

    cohesion = StochasticParameter(mean=5, standard_deviation=0.5)
    mohr_coulomb_parameters = MohrCoulombParameters(cohesion=cohesion)
    soil = Soil(mohr_coulomb_parameters=mohr_coulomb_parameters)

.. code-block:: python

    from geolib.soils import Soil

    soil = Soil()
    soil.mohr_coulomb_parameters.cohesion.mean = 5
    soil.mohr_coulomb_parameters.cohesion.mean = 0.5

.. code-block:: python

    from geolib.soils import Soil

    kwargs = {"cohesion":{"mean": 5,
                            "standard_deviation": 0.5}}

    soil = Soil(mohr_coulomb_parameters=kwargs)

When the parameters, required for the corresponding model are set, the soil can be added
to the soil list of the corresponding model. Note that, for non-filled in parameters, the default value is used.
Below an example is given on how to add a soil in D-Settlement. For an overview on how to pass the complete workflow
for each model, see the other :ref:`tutorial`.

.. code-block:: python

    from geolib.soils import Soil, MohrCoulombParameters
    from geolib.models import DSettlementModel

    mohr_coulomb_parameters = MohrCoulombParameters(cohesion=5, friction_angle=25)
    soil = Soil(mohr_coulomb_parameters=mohr_coulomb_parameters)

    dset_model = DSettlementModel()
    dset_model.add_soil(soil)

Certain soil input are enumerations. For example, "soil_type_nl" which is an input for D-Foundations. Below an example
is shown on how to set an enumeration for the soil.

.. code-block:: python

    from geolib.soils import Soil, SoilType

    soil = Soil()
    soil.soil_type_nl = SoilType.CLAY

Note that this "SoilType" enumeration is reused for three different soil parameters: "soil_type_nl", "soil_type_be" and
"soil_type_settlement_by_vibrations". However only "soil_type_nl" accepts SoilType.SANDY_LOAM.
