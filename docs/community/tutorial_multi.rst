.. _multi_tut:

Tutorial Multiple Calculations
==============================

You can execute multiple calculations at a time, making use of the batch functionality of the consoles.
We use the :class:`~geolib.models.BaseModelList` that wraps multiple models.

A :class:`~geolib.models.BaseModelList` contains a list of models (*models* attribute) and metadata (*meta* attribute).
Note that the models should be of the same type, so don't mix different models.
A few examples follow to clarify the functionality.


First let's setup a standard model. We duplicate the model two times, to have multiple models.
Note how we set a specific filename for each model. This is required, both for doing the calculation, as keeping track of the models.
On calculation the models are serialized to input files for the console, so they need unique filenames.
Because of the parallel batch calculation, the order of the list of output models isn't guaranteed to be the same as the list of output models.
Only the name part of the filename is used, so any folders or prefixed are ignored.

.. code-block:: python

    import geolib as gl
    from pathlib import Path

    dma = gl.models.DStabilityModel()
    dma.parse(Path("test.stix"))

    dma.filename = Path("testa.stix")
    dmb = dma.copy(deep=True)
    dmb.filename = Path("testb.stix")
    dmc = dmb.copy(deep=True)
    dmc.filename = Path("unusedfolder/testc.stix")

Now that we've got three models, let's create a BaseModelList.
Note how we can also change the metadata of the modellist, in the same way we can do it for an individual model.
This step is only required if you want to override the values from the environment variables and geolib.env.

.. code-block:: python

    bm = gl.BaseModelList(models=[dma, dmb, dmc])
    bm.meta.console_folder = Path("C:/Users/somewhere/consoles/")

Now we're ready to execute. You'd have to set a calculation folder, in which `nprocesses` folders will be created.
On each of these folders, which names are just digits (0, 1, nprocesses, ..), a batch console is executed.

.. code-block:: python
 
    newbm = bm.execute(Path("testmulti"), nprocesses=2)

Similarly, you could execute this remotely, resulting in the same output:

.. code-block:: python

    newbm = bm.execute_remote("http://localhost:8000/")

Finally, check your output files and make sure to check how many models you've got back and their individual names.
If you have missing models, check the errors attribute for more information.

.. code-block:: python

    len(newmb.models)
    newbm.models[0].filename
    newbm.models[0].output
    newbm.errors
